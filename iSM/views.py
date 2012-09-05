# -*- coding:utf-8 -*-
import os
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
from iSM.forms import ConsorcioForm, ConsorcistaForm, DocumentUploadForm

@login_required
def home(request):
    if request.is_ajax():
        if request.method == 'GET':
            consorcio_id = request.GET.get('consorcio_id')
            upload = request.GET.get('upload')
            document_form = None
            if upload:
                document_form = DocumentUploadForm()
            if consorcio_id:
                consorcista_list = Consorcista.objects.filter(consorcio=consorcio_id, active=True)
                return render_to_response('iSM/lista_consorcistas.html', {'consorcista_list': consorcista_list,
                                                                          'consorcio_id': consorcio_id,
                                                                          'upload_form': document_form},
                                                                         context_instance=RequestContext(request))
        else:
            return HttpResponseBadRequest()
    consorcio_list = Consorcio.objects.all()
    return render_to_response('iSM/send.html', {'consorcio_list': consorcio_list},
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
def mail_documents(request, consorcista_id):
    if request.method == 'POST':
        documents = None
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        documents_pks = request.POST.get('document_pks')
        if documents_pks:
            documents = Documento.objects.filter(pk__in=documents_pks.split(','))
        try:
            consorcio = Consorcista.objects.get(pk=consorcista_id).consorcio
        except Consorcista.DoesNotExist:
            return Http404
        recipients = [ i[0] for i in consorcio.consorcistas.values_list('email') ]
        if documents and recipients:
            mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipients)
            for document in documents:
                mail.attach(filename=os.path.basename('%s' % document.document_file),
                                content=document.document_file.file.read())
            mail.send()
        return HttpResponseRedirect(reverse('mail-success'))

    consorcista = None
    if consorcista_id:
        consorcista = get_object_or_404(Consorcista, pk=consorcista_id)
        consorcio = consorcista.consorcio
    return render_to_response('iSM/mail_documentos.html', {'consorcista': consorcista, 'consorcio': consorcio},
        context_instance=RequestContext(request))

@login_required
def upload(request):
    if request.method == 'POST':
        document_form = DocumentUploadForm(request.POST, request.FILES)
        if document_form.is_valid():
            document = document_form.save(commit=False)
            document.consorcista = Consorcista.objects.get(pk=request.POST['id_consorcista'])
            document.save()
            return HttpResponseRedirect(reverse('upload'))
    consorcio_list = Consorcio.objects.all()
    return render_to_response('iSM/upload.html', {'consorcio_list': consorcio_list},
        context_instance=RequestContext(request))

@login_required
def about(request):
    return render_to_response('iSM/about.html', context_instance=RequestContext(request))

@login_required
def contact_us(request):
    return render_to_response('iSM/contact_us.html', context_instance=RequestContext(request))

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
def delete_consorcio(request):
    pass

@login_required
def add_consorcista(request, consorcio_id):
    if request.method == 'POST':
        consorcista_form = ConsorcistaForm(request.POST)
        if consorcista_form.is_valid():
            consorcista_form.save()
            return HttpResponseRedirect(reverse('home'))

    consorcista_form = ConsorcistaForm(initial={'consorcio': consorcio_id})
    return render_to_response('iSM/generic_add_form.html', {'form': consorcista_form, 'tipo': 'Consorcista'},
        context_instance=RequestContext(request))

@login_required
def delete_consorcista(request):
    pass

@login_required
def get_documents(request):
    if request.is_ajax():
        if request.method == 'GET':
            consorcista_id = request.GET.get('consorcista_id')
            if consorcista_id:
                documents_list = Documento.objects.filter(consorcista=consorcista_id)
                return render_to_response('iSM/lista_documentos.html', {'documents_list': documents_list,
                                                                        'consorcista_id': consorcista_id},
                    context_instance=RequestContext(request))
    else:
        return HttpResponseBadRequest()
