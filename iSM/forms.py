# -*- coding: utf-8 -*-
import re
from django import forms
from iSM.models import Consorcio, Consorcista, Documento


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
    consorcio = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'styled_select'}),
        queryset=Consorcio.objects.all())
    document_file = forms.FileField(label='Archivo de consorcio')
    belongs_to = forms.CharField(widget=forms.TextInput(attrs={'class': 'datefield'}),
        label=u'Correspondiente a mes/año')

    def clean_document_file(self):
        data = self.cleaned_data['document_file']
        if not re.match(r'\d+_.+.pdf', data.name):
            raise forms.ValidationError(u'Por favor seleccione un archivo de consorcio válido')

        return data

    def clean_belongs_to(self):
        data = self.cleaned_data['belongs_to']
        if not re.match(r'(\d+){2}\/(\d+){4}', data):
            raise forms.ValidationError(u'Por favor seleccione un mes/año válido')

        data_split = data.split('/')
        data = '%s-%s-01' % (data_split[1], data_split[0])

        return data

    class Meta:
        model = Documento
