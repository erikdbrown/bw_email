from django.conf import settings
from django.db import models


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
