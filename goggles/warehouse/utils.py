from celery import chain
import string
import random

from goggles.warehouse import tasks


def update_profile_info_async(profile, username, password):
    return chain(
        tasks.get_session_info.s(profile.pk, username, password),
        tasks.get_conversations.s()).apply_async()


def generate_token(size=10):
    population = string.ascii_letters + ''.join(map(str, range(10)))
    return ''.join(random.sample(population, size))
