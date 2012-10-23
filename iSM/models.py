# -*- coding: utf-8 -*-

from django.db import models

class Consorcio(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Consorcista(models.Model):
    unidad = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    emails = models.CharField(max_length=200)
    consorcio = models.ForeignKey(Consorcio, related_name='consorcistas')
    created = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Documento(models.Model):
    consorcista = models.ForeignKey(Consorcista, related_name="documentos", null=True, blank=True)
    document_name = models.CharField(max_length=255, null=True, blank=True)
    document_file = models.FileField(upload_to='documents/%Y/%m/%d/%H/%M/%S/', max_length=255)
    belongs_to = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.document_name
