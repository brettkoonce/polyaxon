from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from db.models.abstract_jobs import AbstractJob
from db.models.utils import (
    DescribableModel,
    NameableModel,
    NodeSchedulingModel,
    OutputsModel,
    PersistenceModel,
    TagModel
)


class PluginJobBase(AbstractJob,
                    OutputsModel,
                    PersistenceModel,
                    NodeSchedulingModel,
                    NameableModel,
                    DescribableModel,
                    TagModel):
    """A base model for plugin jobs."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='+')
    code_reference = models.ForeignKey(
        'db.CodeReference',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+')
    build_job = models.ForeignKey(
        'db.BuildJob',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+')

    class Meta:
        app_label = 'db'
        abstract = True

    @cached_property
    def secret_refs(self):
        return self.specification.secret_refs

    @cached_property
    def configmap_refs(self):
        return self.specification.configmap_refs
