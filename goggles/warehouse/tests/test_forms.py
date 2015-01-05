from django.test import TestCase
from django.contrib.auth.models import User
# from django.core.management import call_command

from goggles.warehouse.forms import ConversationActionForm

import mock


class TestForms(TestCase):

    def mk_user(self, username='username',
                email_address='username@example.org',
                password='password'):
        return User.objects.create_user(username, email_address, password)

    def mk_profile(self, user=None, status='disconnected'):
        user = user or self.mk_user()
        return user.profile_set.create(status=status)

    def mk_conversation(self, profile=None, name='name',
                        conversation_key='key'):
        profile = profile or self.mk_profile()
        return profile.conversation_set.create(
            name=name, conversation_key=conversation_key)

    def test_form_actions(self):
        form = ConversationActionForm({'action': 'import_job'})
        self.assertTrue(form.is_valid())
        form.do_import_job = mock.Mock()
        form.handle_action('fake conversation')
        form.do_import_job.assert_called_with('fake conversation')

    @mock.patch('goggles.warehouse.tasks.schedule_import_conversation.delay')
    def test_do_import_job(self, mock_task):
        # NOTE: For some reason Django 1.7 needs this.
        # call_command('migrate')
        conversation = self.mk_conversation()
        form = ConversationActionForm()
        self.assertEqual(
            form.do_import_job(conversation),
            'Starting an import job for %s' % (conversation.name,))
        mock_task.assert_called_with(conversation.pk)
