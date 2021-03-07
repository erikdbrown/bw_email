from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db import transaction
from django.db.models.signals import post_save

from email_server.services import (
    SnailgunProvider,
    SpendgridProvider,
)


class EmailProviders():
    SPENDGRID = 'spendgrid'
    SNAILGUN = 'snailgun'


class Email(models.Model):
    to_email = models.TextField()
    to_name = models.TextField()
    from_email = models.TextField()
    from_name = models.TextField()
    subject = models.TextField()
    body = models.TextField()

    status = models.TextField()
    external_id = models.TextField()
    provider = models.TextField(
        choices=(
            (EmailProviders.SPENDGRID, EmailProviders.SPENDGRID),
            (EmailProviders.SNAILGUN, EmailProviders.SNAILGUN)
        )
    )

    def save(self, *args, **kwargs):
        if not self.provider:
            self.provider = settings.EMAIL_PROVIDER

        super(Email, self).save(*args, **kwargs)


@receiver(post_save, sender=Email)
def send_to_email_provider(sender, instance, created, *args, **kwargs):
    if not created:
        return

    if instance.provider == EmailProviders.SPENDGRID:
        email_service = SpendgridProvider()
    elif instance.provider == EmailProviders.SNAILGUN:
        email_service = SnailgunProvider()
    else:
        return

    # TODO: connect this to async queue
    transaction.on_commit(lambda: email_service.send_request(instance.pk))
