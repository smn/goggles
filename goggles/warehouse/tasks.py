from __future__ import absolute_import

import mechanize

from celery import shared_task


@shared_task
def get_session_info(username, password):
    br = mechanize.Browser()
    br.open("https://go.vumi.org/accounts/login/")
    br.select_form(nr=0)
    br.form['username'] = username
    br.form['password'] = password
    resp = br.submit()
    if not 200 < int(resp.code) < 300:
        jar = br._ua_handlers['_cookies'].cookiejar
        [cookie] = [cookie for cookie in jar if cookie.name == 'sessionid']
        return cookie.name, cookie.value, cookie.expires
