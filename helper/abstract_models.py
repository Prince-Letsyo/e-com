from django.db import models


class CreatedAt(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UpDateAt(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class TimeStamps(CreatedAt,UpDateAt):
    class Meta:
        abstract = True

class CreatedAtWithOrder(CreatedAt):
    class Meta:
        abstract = True
        ordering = ('-created_at',)

class TimeStampsWithOrder(CreatedAt,UpDateAt):
    class Meta:
        abstract = True
        ordering = ('-created_at',)


class TrackingModel(CreatedAt, UpDateAt):
    class Meta:
        abstract = True
        ordering = ('-created_at',)
