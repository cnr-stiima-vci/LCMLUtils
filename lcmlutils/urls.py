from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView
from django.contrib import admin
from rest_framework import routers
from lcmlutils.views import LegendViewSet
router = routers.DefaultRouter()
router.register(r'legends', LegendViewSet)

admin.autodiscover()

urlpatterns = patterns(
    'lcmlutils.views',
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^$', 'index', name='index'),
    url(r'^rest/', include(router.urls)),
    url(r'^services/list-basic-elements', 'list_basic_elements', name='list-basic-elements'),
    url(r'^services/basic-element-schema/(?P<basic_element_name>\w{0,50})', 'basic_element_schema', name='basic-element-schema'),
    url(r'^services/derived-classes-list/(?P<basename>\w{0,50})', 'derived_classes_list', name='derived-classes-list'),
    url(r'^services/similarity-assessment', 'similarity_assessment', name='similarity-assessment'),
    url(r'^admin/', include(admin.site.urls)),
)