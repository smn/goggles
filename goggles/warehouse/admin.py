from django.contrib import admin

from goggles.warehouse.models import (
    Session, Message, Interaction, ImportJob, Profile, Conversation)


class InteractionAdmin(admin.ModelAdmin):

    readonly_fields = ('inbound', 'outbound')


admin.site.register(Session)
admin.site.register(Message)
admin.site.register(Interaction, InteractionAdmin)
admin.site.register(ImportJob)
admin.site.register(Profile)
admin.site.register(Conversation)
