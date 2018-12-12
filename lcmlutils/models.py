import uuid
import logging

from datetime import datetime


from django.db import models
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


logger = logging.getLogger("lcmlutils")

class XSDValidator(models.Model):
    LINK_TYPE_CHOICES = (
        ('django_orm', 'django orm'),
        ('existdb', 'existdb collection resource'),
    )
    """Model for storing validators.
    """
    name = models.CharField(_('validator name'), max_length=255, unique=True)
    xsd_text = models.TextField(_('XSD text'), null=True, blank=True)
    active = models.BooleanField(_('active'), default = False)
    link_type = models.CharField(_('link type'), max_length=64, null=True)
    link = models.CharField(_('link'), max_length=128, null=True, blank=True)
    
    def __str__(self):
        return "%s" % self.name.encode('utf-8')

    class Meta:
        db_table = 'lcmlutils_xsdvalidators'
        app_label = 'lcmlutils'


class LCCS3Class(models.Model):

    """Model for storing LCCS3 classes.

    """
    name = models.CharField(_('class name'), max_length=255, unique=True)
    description = models.TextField(_('description'), null = True, blank = True)
    xml_text = models.TextField(_('XML text'), null=False)
    active = models.BooleanField(_('active'), default = False)

    legend = models.ForeignKey('LCCS3Legend', on_delete = models.CASCADE, default = None)
    validator = models.ForeignKey('XSDValidator', on_delete = models.CASCADE)

    def __str__(self):
        return "%s" % self.name.encode('utf-8')

    class Meta:
        db_table = 'lcmlutils_lccs3classes'
        app_label = 'lcmlutils'
        verbose_name = 'lccs3 class'
        verbose_name_plural = 'lccs3 classes'



class LCCS3Legend(models.Model):

    """Model for storing LCCS3 classes.

    """
    LINK_TYPE_CHOICES = (
        ('django_orm', 'django orm'),
        ('existdb', 'existdb collection resource'),
    )
    
    name = models.CharField(_('legend name'), max_length=255, unique=True)
    description = models.TextField(_('description'), null = True, blank = True)
    xml_text = models.TextField(_('XML text'), null=False, default = '')
    active = models.BooleanField(_('active'), default = False)
    link_type = models.CharField(_('link type'), max_length=64, null=True)
    link = models.CharField(_('link'), max_length=128, null=True, blank=True)

    def __str__(self):
        return "%s" % self.name.encode('utf-8')

    class Meta:
        db_table = 'lcmlutils_lccs3legends'
        app_label = 'lcmlutils'
        verbose_name = 'lccs3 legend'
        verbose_name_plural = 'lccs3 legends'

