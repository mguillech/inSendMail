# -*- coding:utf-8 -*-
import os
import re
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (login as login_function,
                                 logout as logout_function, authenticate)
from django.contrib.auth.views import logout_then_login
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.conf import settings
from iSM.models import Consorcio, Consorcista, Documento
from iSM.forms import ConsorcioForm, ConsorcistaForm, DocumentUploadForm, ContactUs

from iSM.functions import process_document

@login_required
def home(request):
    consorcio_list = Consorcio.objects.all()
    consorcista_list = Consorcista.objects.all()
    return render_to_response('iSM/send.html', {'consorcio_list': consorcio_list,
                                                'consorcista_list': consorcista_list},
        context_instance=RequestContext(request))

def login(request):
    msg = ''
    if request.user and request.user.is_authenticated():
        logout_function(request)
    if request.REQUEST.has_key('next') and request.REQUEST['next']:
        next_url = request.REQUEST['next']
    else:
        next_url = reverse('home')
    username, password = request.POST.get('username'), request.POST.get('password')
    if username and password:
        user = authenticate(username=username, password=password)
        if user:
            login_function(request, user)
            return HttpResponseRedirect(next_url)
        else:
            msg = u'Usuario/contraseña inexistente'
    return render_to_response('iSM/login.html', {'msg': msg}, context_instance=RequestContext(request))

def logout(request):
    if request.user and request.user.is_authenticated:
        return logout_then_login(request)
    else:
        return HttpResponseRedirect(reverse('login'))

@login_required
def mail_documents(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message_area')
        documents_pks = request.POST.get('document_pks')
        if not all([subject, message, documents_pks]):
            return HttpResponseRedirect(reverse('mail-failed'))
        documents = Documento.objects.filter(pk__in=documents_pks.split(','))
        for document in documents:
            document_name = document.document_name
            recipients = [ i.strip() for i in document.consorcista.emails.split('/') ]
            for recipient in recipients:
                mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient)
                mail.attach(filename=document_name, content=document.document_file.file.read())
                mail.send()
        return HttpResponseRedirect(reverse('mail-success'))

    return render_to_response('iSM/mail_documentos.html', context_instance=RequestContext(request))

@login_required
def upload(request):
    if request.method == 'POST':
        document_form = DocumentUploadForm(request.POST, request.FILES)
        if document_form.is_valid():
            document = document_form.save(commit=False)
            try:
                processed = process_document(document.document_file.file)
                consorcista, belongs_to = processed
                document.consorcista = consorcista
                document.document_name = document.document_file.name
                document.belongs_to = belongs_to
                document.save()
                return HttpResponseRedirect(reverse('upload'))
            except:
                document_form._errors['document_file'] = u'\nDocumento inv&aacute;lido'
    else:
        document_form = DocumentUploadForm()
    return render_to_response('iSM/upload.html', {'upload_form': document_form},
        context_instance=RequestContext(request))

@login_required
def about(request):
    return render_to_response('iSM/about.html', context_instance=RequestContext(request))

@login_required
def contact_us(request):
    if request.method == 'POST':
        contact_us_form = ContactUs(request.POST)
        if contact_us_form.is_valid():
            name = contact_us_form.cleaned_data['name']
            email = contact_us_form.cleaned_data['email']
            message = contact_us_form.cleaned_data['message']
            subject = u'Mail enviado desde la web por %s (%s)' % (name, email)
    #        mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, settings.EMAIL_HOST_USER)
    #        mail.send()
    else:
        contact_us_form = ContactUs()
    return render_to_response('iSM/contact_us.html', {'form': contact_us_form},
                                                      context_instance=RequestContext(request))

@login_required
def add_consorcio(request):
    if request.method == 'POST':
        consorcio_form = ConsorcioForm(request.POST)
        if consorcio_form.is_valid():
            consorcio_form.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        consorcio_form = ConsorcioForm()
    return render_to_response('iSM/generic_add_form.html', {'form': consorcio_form, 'tipo': 'Consorcio'},
        context_instance=RequestContext(request))

@login_required
def edit_consorcio(request, consorcio_id):
    consorcio = get_object_or_404(Consorcio, pk=consorcio_id)
    if request.method == 'POST':
        consorcio_form = ConsorcioForm(request.POST, instance=consorcio)
        if consorcio_form.is_valid():
            consorcio_form.save()
            return HttpResponseRedirect(reverse('list-consorcios'))
    else:
        consorcio_form = ConsorcioForm(instance=consorcio)
    return render_to_response('iSM/generic_edit_form.html', {'form': consorcio_form, 'tipo': 'Consorcio'},
        context_instance=RequestContext(request))

@login_required
def delete_consorcio(request, consorcio_id):
    consorcio = get_object_or_404(Consorcio, pk=consorcio_id)
    consorcio.delete()
    return HttpResponseRedirect(reverse('list-consorcio'))

@login_required
def add_consorcista(request):
    if request.method == 'POST':
        consorcista_form = ConsorcistaForm(request.POST)
        if consorcista_form.is_valid():
            consorcista_form.save()
            return HttpResponseRedirect(reverse('home'))

    consorcista_form = ConsorcistaForm()
    return render_to_response('iSM/generic_add_form.html', {'form': consorcista_form, 'tipo': 'Consorcista'},
        context_instance=RequestContext(request))

@login_required
def edit_consorcista(request, consorcista_id):
    consorcista = get_object_or_404(Consorcista, pk=consorcista_id)
    if request.method == 'POST':
        consorcista_form = ConsorcistaForm(request.POST, instance=consorcista)
        if consorcista_form.is_valid():
            consorcista_form.save()
            return HttpResponseRedirect(reverse('list-consorcistas'))

    consorcista_form = ConsorcistaForm(instance=consorcista)
    return render_to_response('iSM/generic_edit_form.html', {'form': consorcista_form, 'tipo': 'Consorcista'},
        context_instance=RequestContext(request))

@login_required
def delete_consorcista(request, consorcista_id):
    consorcista = get_object_or_404(Consorcista, pk=consorcista_id)
    consorcista.delete()
    return HttpResponseRedirect(reverse('list-consorcistas'))

@login_required
def get_documents(request):
    if request.is_ajax():
        if request.method == 'GET':
            consorcio_id = request.GET.get('consorcio_id')
            consorcista_id = request.GET.get('consorcista_id')
            date = request.GET.get('date')
            documents_list = Documento.objects.all()
            if consorcio_id:
                documents_list = documents_list.filter(consorcista__consorcio=consorcio_id)
            if consorcista_id:
                documents_list = documents_list.filter(consorcista=consorcista_id)
            if date:
                if not re.match(r'(\d+){2}\/(\d+){4}', date):
                    return HttpResponseBadRequest
                date_split = date.split('/')
                date = '%s-%s-01' % (date_split[1], date_split[0])
                documents_list = documents_list.filter(belongs_to=date)
            return render_to_response('iSM/lista_documentos.html', {'documents_list': documents_list},
                                        context_instance=RequestContext(request))
    else:
        return HttpResponseBadRequest
