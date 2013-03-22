# -*- coding: utf-8 -*-
import re
from django import forms
from iSM.models import Consorcio, Consorcista, Documento, Comun


class ConsorcioForm(forms.ModelForm):
    name = forms.CharField(label='Nombre')

    class Meta:
        model = Consorcio


class ConsorcistaForm(forms.ModelForm):
    code = forms.IntegerField(label=u'Código')
    name = forms.CharField(label='Nombre')
    active = forms.BooleanField(label='Activo', widget=forms.CheckboxInput(attrs={'checked': 'checked'}))
    consorcio = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'styled_select'}),
        queryset=Consorcio.objects.all())

    class Meta:
        model = Consorcista


class DocumentUploadForm(forms.ModelForm):
    document_file = forms.FileField(label='Archivo de consorcio')

    def clean_document_file(self):
        data = self.cleaned_data['document_file']
        if not re.match(r'.+\.pdf', data.name):
            raise forms.ValidationError(u'Por favor seleccione un archivo de consorcio válido')

        if Documento.objects.filter(document_name=data.name):
            raise forms.ValidationError(u'Archivo ya existente en la base de datos')

        return data


    class Meta:
        model = Documento
        fields = ('document_file',)


class CommonUploadForm(forms.ModelForm):
    common_file = forms.FileField(label=u'Archivo común')

    def clean_common_file(self):
        data = self.cleaned_data['common_file']

        if Comun.objects.filter(common_name=data.name):
            raise forms.ValidationError(u'Archivo ya existente en la base de datos')

        return data

    class Meta:
        model = Comun
        fields = ('common_file',)


class ContactUs(forms.Form):
    name = forms.CharField(label='Su nombre:')
    email = forms.EmailField(label=u'Su dirección de e-mail:')
    message = forms.CharField(widget=forms.Textarea, label='Mensaje:')
