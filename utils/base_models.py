from django.db import models


class LogsMixin(models.Model):
    """Add the generic fields and relevant methods common to support mostly
    models
    """
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,  null=True)

    class Meta:
        """meta class for LogsMixin"""
        abstract = True
