# -*- coding: utf-8 -*-

from django.db import models

class Consorcio(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Consorcista(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=True)
    consorcio = models.ForeignKey(Consorcio, related_name='consorcistas')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Documento(models.Model):
    consorcio = models.ForeignKey(Consorcio, related_name="document", null=True, blank=True)
    document_file = models.FileField(upload_to='documents/%Y/%m/%d/%H/%M/%S/', max_length=255)
    belongs_to = models.DateField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s -- %s' % (self.consorcio, self.document_file)
