# -*- coding: utf-8 -*
#
# ePoint WebShop
# Copyright (C) 2010 - 2012 ePoint Systems Ltd
# Author: Andrey Martyanov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

from flask import Flask, g, request, make_response
from flaskext.babel import Babel
from flaskext.babel import gettext as _

from epoint.client.document import DocumentSource, Document

import settings
from templates import *

app = Flask(__name__)
i18n = Babel(app)
app.debug = True #if settings.DEBUG == 'true' else False

class Invoice(object):
    def __init__(self, D, B='', F=0, issuer=settings.ISSUER):
        self.certificate_link = ''
        self.message = ''
        self.issuer = issuer
        self.value = 0
        self.D = D
        self.B =  B
        self.F = F


def after_this_request(f):
    if not hasattr(g, 'after_request_callbacks'):
        g.after_request_callbacks = []
    g.after_request_callbacks.append(f)
    return f


@app.after_request
def call_after_request_callbacks(response):
    for callback in getattr(g, 'after_request_callbacks', ()):
        response = callback(response)
    return response


def set_cookie_value(key, value):
    @after_this_request
    def set_cookie(response):
        response.set_cookie(key, value)


def _render_error_page(error_title, error_details, status=500):
    error_page = [render_header()]
    error_page.append(render_error(error_title, error_details))
    error_page.append(render_footer())
    return make_response(error_page, status)


@app.route('/')
def index():
    D = request.args.get('D', None)
    B = request.args.get('B', '')
    F = request.args.get('F', None)
    E = request.args.get('E', None)
    K = request.args.get('K', None)
    L = request.args.get('L', '')
    status_code = 200
    payment_required = False
    if F is not None:
        try:
            F = int(F)
        except ValueError:
            F = 0
    else:
        F = 0
    page = [render_header()]
    if D is None:
        return _render_error_page(_('Missing parameter'),
            _('Parameter D is missing'))
    invoice = Invoice(D, B=B, F=F)
    document_source = DocumentSource(settings.ISSUER, docid=invoice.D)
    document = Document(document_source)
    value = None
    verified = document.verify()
    # document.verify() returns False if verification failed
    # and None upon another error
    if verified != False:
        value = document.get_value()
    if value is not None:
        invoice.value = value
        if value > 0:
            invoice.certificate_link = '<a href="%s/info?ID=%s">%s</a>' % (settings.ISSUER,
                invoice.D, _('GET CERTIFICATE'))
        if (value >= F) and (F is not None) and (F > 0):
            invoice.message = _('The corresponding invoice has been paid')
            page.append(render_invoce(invoice))
            # Email address
            email = ''
            if E is not None:
                set_cookie_value('pfemail', E)
                email = E
            else:
                email = request.cookies.get('pfemail')
            # PGP encryption key ID
            pgpkey = ''
            if K is not None:
                set_cookie_value('pfpgpkey', K)
                pgpkey = K
            else:
                pgpkey = request_cookies_get('pfpgpkey')
            # If mailreceipt application is configured render the email form
            if settings.MAILRECEIPT_URL:
                page.append(render_email_form(email, pgpkey, document.get_sn(),
                    settings.MAILRECEIPT_URL, L))
        else:
            if F > 0:
                payment_required = True
            status_code = 402
            invoice.G = '%s/?D=%s&F=%s' % (settings.REDIRECTION_TARGET, invoice.D,
                str(invoice.F))
            page.append(render_invoce_form(invoice))

    else:
        return self._render_error_page(_('Internal error'),
            _('Sorry for the inconvenience'))

    page.append(render_footer())
    
    response = make_response(page, status_code)
    if payment_required:
        response.headers['Content-Price'] = "%s EPT" % str(F - value)

    return response
    
if __name__ == '__main__':
    app.run()