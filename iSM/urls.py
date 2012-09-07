from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from iSM.models import Consorcio, Consorcista

urlpatterns = patterns('',
    # inMailSend urls
    url(r'^$', ListView.as_view(model=Consorcio, context_object_name='consorcios',
        template_name='iSM/lista_consorcios.html'), name='list-consorcios'),
    url(r'^add/$', 'iSM.views.add_consorcio', name='add-consorcio'),
    url(r'^edit/(\d+)/$', 'iSM.views.edit_consorcio', name='edit-consorcio'),
    url(r'^delete/(\d+)/$', 'iSM.views.delete_consorcio', name='delete-consorcio'),
    url(r'^consorcista/$', ListView.as_view(model=Consorcista, context_object_name='consorcistas',
        template_name='iSM/lista_consorcistas.html'), name='list-consorcistas'),
    url(r'^consorcista/add/$', 'iSM.views.add_consorcista', name='add-consorcista'),
    url(r'^consorcista/edit/(\d+)/$', 'iSM.views.edit_consorcista', name='edit-consorcista'),
    url(r'^consorcista/delete/(\d+)/$', 'iSM.views.delete_consorcista', name='delete-consorcista'),
    url(r'^consorcista/get-documents/$', 'iSM.views.get_documents', name='get-documents'),
)
