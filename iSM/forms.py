__author__ = 'mguillech'
from django import forms
from iSM.models import Consorcio, Consorcista, Documento


class ConsorcioForm(forms.ModelForm):
    class Meta:
        model = Consorcio


class ConsorcistaForm(forms.ModelForm):
    class Meta:
        model = Consorcista


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Documento
        exclude = ('consorcista',)
