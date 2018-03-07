from django.db import models
from model_utils.models import TimeStampedModel
from os.path import basename

class LogEntry(TimeStampedModel):
    """Initial, minimal model"""
    name = models.TextField(max_length=255, blank=True)
    data_file = models.FileField(upload_to='uploads/%Y/%m/%d/')

    def __str__(self):
        """minimal, change to name"""
        return self.name

    def save(self, *args, **kwargs):
        """update name..."""
        if not self.id:
            super(LogEntry, self).save(*args, **kwargs)

        self.name = basename(self.datafile.filename)[:100]

        super(LogEntry, self).save(*args, **kwargs)
