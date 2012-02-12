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

from flaskext.babel import gettext as _

__all__ = ['render_header', 'render_footer', 'render_invoce', 'render_invoce_form',
    'render_email_form', 'render_error']

def render_header():
    return """
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
    <html>

    <head>
      <title>%(title)s</title>
      <meta http-equiv="Content-type" content="text/html;charset=UTF-8">
      <link rel="stylesheet" type="text/css" href="static/style.css">
      <link rel="icon" type="image/x-icon" href="static/epoint.ico">
    </head>

    <body>

      <div id="header">
      </div>
    """ % {'title': _('WebShop Invoice')}


def render_footer():
    return """
      <div id="footer">
        <p>ePoint Systems Ltd.</p>
      </div>

    </body>

    </html>
    """


def render_invoce(invoice):
    return """
      <div class="content">
        <h1>%(message)s</h1>
        <p>%(certificate_link)s</p>
        <p>%(Total ePoints uploaded in this session:)s </p>
        <div id="counter"><p>%(value)s EPT</p></div>
      </div>
    """ % {
       'message': invoice.message, 
       'certificate_link': invoice.certificate_link,
       'value': invoice.value,
       'Total ePoints uploaded in this session:': _('Total ePoints uploaded in this session:')
    }


def render_invoce_form(invoice):  
    return """
      <div class="content">
        <p>%(certificate_link)s</p>
        <p>%(Total ePoints uploaded in this session:)s </p>
        <div id="counter"><p>%(value)s EPT</p></div>
        <form method="POST" action="%(action)s">
          <p>%(Enter ePoint RAND:)s</p>
          <p><input type="text" name="B" value="%(B)s"></p>
          <input type="hidden" name="D" value="%(D)s">
          <input type="hidden" name="G" value="%(G)s">
        </form>
      </div>
    """ % {
        'certificate_link': invoice.certificate_link,
        'value': invoice.value,
        'action': invoice.issuer + '/action',
        'B': invoice.B, 'D': invoice.D, 'G': invoice.G,
        'Enter ePoint RAND:': _('Enter ePoint RAND:'),
        'Total ePoints uploaded in this session:': _('Total ePoints uploaded in this session:')
    }


def render_email_form(E, K, sn, action, L):
    return """
      <div class="content">
        <form method="POST" action="%(action)s">
          <p>%(Enter email address:)s</p>
          <p><input type="text" name="email" value="%(E)s"></p>
          <p>%(Enter pgp encyption key ID (optional):)s</p>
          <p><input type="text" name="pgp" value="%(K)s"></p>
          <p>%(Enable PGP/MIME:)s</p>
          <p><input type="checkbox" name="mime" checked="checked"></p>
          <input type="hidden" name="sn" value="%(sn)s">
          <input type="hidden" name="L" value="%(L)s">
          <input type="submit" value="%(Send)s">
        </form>
      </div>
    """ % {
       'action': action,
       'E': E, 'K': K, 'sn': sn, 'L': L,
       'Enter email address:': _('Enter email address:'),
       'Enter pgp encyption key ID (optional):': _('Enter pgp encyption key ID (optional):'),
       'Enable PGP/MIME:': _('Enable PGP/MIME:'),
       'Send': _('Send')
    }


def render_error(error_title, error_details):
    return """
      <div class="content">
        <h1>%(error_title)s</h1>
        <p>%(error_details)s</p>
      </div>
    """ % {
        'error_title': error_title,
        'error_details': error_details
    }
