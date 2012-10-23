from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'inSendMail.views.home', name='home'),
    # url(r'^inSendMail/', include('inSendMail.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # inMailSend urls
    url(r'^$', 'iSM.views.home', name='home'),
    url(r'^login/$', 'iSM.views.login', name='login'),
    url(r'^logout/$', 'iSM.views.logout', name='logout'),
    url(r'^upload/$', 'iSM.views.upload', name='upload'),
    url(r'^about/$', 'iSM.views.about', name='about'),
    url(r'^contact_us/$', 'iSM.views.contact_us', name='contact-us'),
    url(r'^consorcio/', include('iSM.urls')),
    url(r'^mail_documents/$', 'iSM.views.mail_documents', name='mail-documents'),
    url(r'^mail_sucess/$', direct_to_template, {'template': 'iSM/mail_success.html'}, name='mail-success'),
    url(r'^mail_failed/$', direct_to_template, {'template': 'iSM/mail_failed.html'}, name='mail-failed'),
)
