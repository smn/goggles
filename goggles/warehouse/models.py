from django.db import models


STATUS_CHOICES = (
    ('started', 'Started'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
)


class Profile(models.Model):
    user = models.ForeignKey('auth.User')
    session_id = models.CharField(max_length=255, null=True)
    session_expires = models.IntegerField(null=True)


class ImportJob(models.Model):
    user = models.ForeignKey('auth.User', null=True)
    name = models.TextField(null=True)
    username_token = models.CharField(
        'Username token.', max_length=255, unique=True)
    password_token = models.CharField('Password token.', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES,
                              null=True)

    class Meta:
        ordering = ('-created_at',)

    def __unicode__(self):
        return u':'.join([self.username_token, self.password_token])


class Session(models.Model):
    import_job = models.ForeignKey(ImportJob, null=True)
    session_id = models.CharField('Session Identifier', max_length=255)
    started_at = models.DateTimeField(null=True)
    ended_at = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.session_id


DIRECTION_CHOICES = (
    ('inbound', 'Inbound'),
    ('outbound', 'outbound'),
)


class Message(models.Model):
    import_job = models.ForeignKey(ImportJob, null=True)
    session = models.ForeignKey(Session, null=True)
    message_id = models.CharField(max_length=255, unique=True, null=True)
    in_reply_to = models.CharField(max_length=255, null=True)
    timestamp = models.DateTimeField()
    from_addr = models.CharField('Subscriber address', max_length=255, null=True)
    to_addr = models.CharField('Destination address', max_length=255, null=True)
    tag_pool = models.CharField('Tag pool', null=True, max_length=255)
    tag = models.CharField('Tag', null=True, max_length=255)
    content = models.TextField(null=True)
    direction = models.CharField(choices=DIRECTION_CHOICES, max_length=255)

    class Meta:
        ordering = ('timestamp',)


class Interaction(models.Model):
    import_job = models.ForeignKey(ImportJob, null=True)
    inbound = models.ForeignKey(Message, null=True, related_name='inbound')
    outbound = models.ForeignKey(Message, null=True, related_name='outbound')
    question = models.CharField(null=True, max_length=255)
    response = models.CharField(null=True, max_length=255)
    duration = models.IntegerField(null=True)
