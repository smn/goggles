from django import forms

from goggles.warehouse.models import ImportJob, Profile
from goggles.warehouse.tasks import schedule_import_conversation


class ProfileForm(forms.ModelForm):
    password = forms.CharField(label='Password', max_length=255)
    update_session_info = forms.BooleanField(
        label='Update login session information?')

    class Meta:
        model = Profile
        exclude = (
            'user',
            'status',
            'session_name',
            'session_value',
            'session_expires',
            'expires_on',
        )


class ImportJobForm(forms.ModelForm):

    class Meta:
        model = ImportJob
        exclude = ('user', 'status')


class ConversationActionForm(forms.Form):
    action = forms.ChoiceField(choices=[
        ('import_job', 'Schedule an Import Job for this conversation')
    ])

    def handle_action(self, conversation):
        handler = getattr(self, 'do_%(action)s' % self.cleaned_data)
        return handler(conversation)

    def do_import_job(self, conversation):
        schedule_import_conversation.delay(conversation.pk)
        return 'Starting a import job for %s' % (conversation.name,)
