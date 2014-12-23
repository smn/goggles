from celery import chain

from goggles.warehouse import tasks


def update_profile_info_async(profile, username, password):
    return chain(
        tasks.get_session_info.s(profile.pk, username, password),
        tasks.get_conversations.s()).apply_async()
