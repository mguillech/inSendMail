from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # inMailSend urls
    url(r'^add/$', 'iSM.views.add_consorcio', name='add-consorcio'),
    url(r'^delete/$', 'iSM.views.delete_consorcio', name='delete-consorcio'),
    url(r'^consorcista/add/(\d+)/$', 'iSM.views.add_consorcista', name='add-consorcista'),
    url(r'^consorcista/delete/$', 'iSM.views.delete_consorcista', name='delete-consorcista'),
    url(r'^consorcista/get-documents/$', 'iSM.views.get_documents', name='get-documents'),
)
