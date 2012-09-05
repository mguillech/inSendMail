from django.db import models

class Consorcio(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre Consorcio')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Consorcista(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre Consorcista')
    email = models.EmailField(max_length=200)
    active = models.BooleanField(default=True, verbose_name='Activo')
    consorcio = models.ForeignKey(Consorcio, related_name='consorcistas')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Documento(models.Model):
    consorcista = models.ForeignKey(Consorcista, related_name="document", null=True, blank=True)
    document_file = models.FileField(upload_to='documents/%Y/%m/%d/%H/%M/%S/', max_length=255,
        verbose_name='Archivo de documento')
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s -- %s' % (self.consorcista, self.document_file)
