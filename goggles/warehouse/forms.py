from django.forms import ModelForm

from goggles.warehouse.models import ImportJob, Profile


class ProfileForm(ModelForm):

    class Meta:
        model = Profile


class ImportJobForm(ModelForm):

    class Meta:
        model = ImportJob
