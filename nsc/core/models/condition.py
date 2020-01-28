from django.urls import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel
from model_utils import Choices
from simple_history.models import HistoricalRecords

from nsc.core.fields import ChoiceArrayField


class Condition(TimeStampedModel):

    AGE_GROUPS = Choices(
        ('antenatal', _('Antenatal')),
        ('newborn', _('Newborn')),
        ('child', _('Child')),
        ('adult', _('Adult')),
        ('all', _('All ages')),
    )

    name = models.CharField(verbose_name=_('name'), max_length=256)
    slug = models.SlugField(verbose_name=_('slug'), max_length=256, unique=True)

    ages = ChoiceArrayField(models.CharField(
        verbose_name=_('age groups'), choices=AGE_GROUPS, max_length=50))

    description = models.TextField(verbose_name=_('description'))
    markup = models.TextField(verbose_name=_('markup'))

    history = HistoricalRecords()

    class Meta:
        ordering = ('name', 'pk', )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('core:condition:detail', args=[str(self.id)])
