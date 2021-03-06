from __future__ import absolute_import

from datetime import datetime
from itertools import tee, izip

import cookielib
import mechanize
import requests
import pytz

from celery import shared_task

from django.conf import settings

from goggles.warehouse.models import (
    Profile, Conversation, ImportJob, Interaction, Message)


def window(iterable, size):
    iters = tee(iterable, size)
    for i in xrange(1, size):
        for each in iters[i:]:
            next(each, None)
    return izip(*iters)


@shared_task
def get_session_info(profile_pk, username, password):
    br = mechanize.Browser()
    profile_query = Profile.objects.filter(pk=profile_pk)
    profile_query.update(status='connecting')
    try:
        br.open("https://go.vumi.org/accounts/login/")
        br.select_form(nr=0)
        br.form['username'] = username
        br.form['password'] = password

        resp = br.submit()
        if not 200 < int(resp.code) < 300:
            jar = br._ua_handlers['_cookies'].cookiejar
            [cookie] = [cookie for cookie in jar if cookie.name == 'sessionid']
            profile_query.update(
                session_name=cookie.name,
                session_value=cookie.value,
                session_expires=cookie.expires,
                expires_on=datetime.fromtimestamp(cookie.expires, tz=pytz.UTC),
                status='connected')
        return profile_pk
    except Exception:
        profile_query.update(status='failed')


@shared_task
def get_conversations(profile_pk):
    profile = Profile.objects.get(pk=profile_pk)

    jar = cookielib.CookieJar()

    cookie = cookielib.Cookie(
        version=0,
        name=profile.session_name,
        value=profile.session_value,
        expires=profile.session_expires,
        port=None,
        port_specified=False,
        domain='go.vumi.org',
        domain_specified=True,
        domain_initial_dot=False,
        path='/',
        path_specified=True,
        secure=True,
        discard=False,
        comment=None,
        comment_url=None,
        rest={'HttpOnly': False},
        rfc2109=False)
    jar.set_cookie(cookie)

    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Goggles/0.1.1 (Mechanize)')]
    br.set_cookiejar(jar)

    conversations = []

    def extract_conversation_links(br):
        for link in br.links(url_regex='/conversations/[a-zA-Z0-9]{32}/$'):
            conversations.append(
                (link.text, filter(None, link.url.split('/'))[-1]))

    br.open("https://go.vumi.org/conversations/")
    extract_conversation_links(br)
    for link in br.links(url_regex='\?p=\d+$'):
        br.follow_link(link)
        extract_conversation_links(br)
        br.back()

    for name, conversation_key in conversations:
        conv, _ = Conversation.objects.get_or_create(
            conversation_key=conversation_key,
            user=profile.user,
            profile=profile)
        conv.name = name
        conv.save()


@shared_task
def schedule_import_conversation(conversation_pk):
    from goggles.warehouse.utils import generate_token
    conv = Conversation.objects.get(pk=conversation_pk)
    job = ImportJob.objects.create(
        user=conv.user,
        profile=conv.profile,
        conversation=conv,
        name='Importing %s.' % (conv.name,),
        status='started',
        username_token=generate_token(),
        password_token=generate_token())

    try:
        urls = [
            '%s/download/inbound' % settings.GOGGLE_SERVER_URL,
            '%s/download/outbound' % settings.GOGGLE_SERVER_URL,
        ]
        for url in urls:
            print url
            job.status = 'in_progress'
            job.save()
            requests.get(
                url,
                auth=(job.username_token, job.password_token),
                stream=True)
        job.status = 'completed'
        job.save()
    except Exception:
        job.status = 'failed'
        job.save()


@shared_task
def link_interactions(pk):
    job = ImportJob.objects.get(pk=pk)

    outbounds = job.message_set.filter(direction='outbound')
    for outbound in outbounds:
        ix, _ = Interaction.objects.get_or_create(
            import_job=job,
            outbound=outbound)

    inbounds = job.message_set.filter(direction='inbound')
    for inbound in inbounds:
        outbound = Message.objects.filter(
            timestamp__lte=inbound.timestamp,
            import_job=job,
            from_addr=inbound.to_addr,
            to_addr=inbound.from_addr,
            direction='outbound').order_by('-timestamp').first()

        if outbound is None:
            continue

        reply_to = Message.objects.filter(
            direction='inbound',
            message_id=outbound.in_reply_to).first()

        if reply_to and reply_to.session_event == 'new':
            continue

        try:
            ix = Interaction.objects.get(outbound=outbound)
            ix.outbound = outbound
            ix.inbound = inbound
            ix.question = outbound.content
            ix.response = inbound.content
            ix.duration = (inbound.timestamp - outbound.timestamp).seconds
            print 'Reply to %r was %r and took %r' % (
                ix.outbound.content, ix.inbound.content, ix.duration)
            ix.save()
        except Interaction.DoesNotExist:
            pass
