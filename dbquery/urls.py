from django.conf.urls import patterns, url
from dbquery import views

urlpatterns = patterns('',
    
    # ex: /search/
    url(r'^$', views.search, name='search'),
    
    # ex: /search/hsa-let-7a-5p/  --shows details about the search
    url(r'^(?P<search_id>[a-zA-Z0-9\-]+)/$', views.detail, name ='detail'),
    
    # ex: /search/hsa-let-7a-5p/mirnaresults/ --shows response from the search
    # ex: /search/ENSG00000186575/generesults/
    url(r'^(?P<search_id>[a-zA-Z0-9\-]+)/mirnaresults/$', views.mirna_results, name ='mirnaresults'),
    url(r'^(?P<search_id>[a-zA-Z0-9\-\(\)\_]+)/generesults/$', views.gene_results, name ='generesults'),
)
