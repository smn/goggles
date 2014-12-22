from django.db import models


class ImportJob(models.Model):
    username_token = models.CharField(
        'Username token.', max_length=255, unique=True)
    password_token = models.CharField('Password token.', max_length=255)

    def __unicode__(self):
        return u':'.join([self.username_token, self.password_token])

STATUS_CHOICES = (
    ('started', 'Started'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
)


class Session(models.Model):
    import_job = models.ForeignKey(ImportJob, null=True)
    status = models.CharField(
        'Session status', max_length=255, choices=STATUS_CHOICES,
        null=True)
    session_id = models.CharField('Session Identifier', max_length=255)
    from_addr = models.CharField('Subscriber address', max_length=255)
    to_addr = models.CharField('Destination address', max_length=255)
    tag_pool = models.CharField('Tag pool', null=True, max_length=255)
    tag = models.CharField('Tag', null=True, max_length=255)
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
    timestamp = models.DateTimeField()
    direction = models.CharField(choices=DIRECTION_CHOICES, max_length=255)
    content = models.TextField(null=True)


class Interaction(models.Model):
    import_job = models.ForeignKey(ImportJob, null=True)
    inbound = models.ForeignKey(Message, null=True, related_name='inbound')
    outbound = models.ForeignKey(Message, null=True, related_name='outbound')
    question = models.CharField(null=True, max_length=255)
    response = models.CharField(null=True, max_length=255)
    duration = models.IntegerField(null=True)
