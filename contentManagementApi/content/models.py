import os
from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models
from user.models import User

alphabetic = RegexValidator(r'^[a-zA-Z0-9 ]*$', 'Only alpha-numeric characters are allowed.')


def content_file_name(instance, filename):
    upload_dir = os.path.join("content_files", str(instance.user_id),str(instance.id))
    return os.path.join(upload_dir, filename)


class Contents(models.Model):
    title = models.CharField(default=None, max_length=30, null=False, blank=False, validators=[alphabetic])
    body = models.CharField(default=None, max_length=300, null=False, blank=False, validators=[alphabetic])
    summary = models.CharField(default=None, max_length=60, null=False, blank=False, validators=[alphabetic])
    document = models.FileField(upload_to=content_file_name, max_length=None,
                                validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_user', blank=False,
                             null=False, default=None)
    categories = models.CharField(max_length=255, null=False, blank=False, default=None)

    class Meta:
        db_table = 'contents'  # define your custom name
        verbose_name = 'Content'
        verbose_name_plural = 'Contents'

    def __init__(self, *args, **kwargs):
        super(Contents, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.id is None:
            saved_image = self.document
            self.document = None
            super(Contents, self).save(*args, **kwargs)
            self.document = saved_image
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super(Contents, self).save(*args, **kwargs)
        return self
