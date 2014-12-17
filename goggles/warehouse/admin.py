from django.contrib import admin

from goggles.warehouse.models import Session, Message, Interaction, ImportJob


admin.site.register(Session)
admin.site.register(Message)
admin.site.register(Interaction)
admin.site.register(ImportJob)
