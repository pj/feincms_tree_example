from django.db import models
from mptt.models import MPTTModel
from feincms.models import create_base_model

class Page(MPTTModel):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=100)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')

    def __unicode__(self):
        return self.title
