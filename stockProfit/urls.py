from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^historyData$', views.historyData), 
    url(r'^ethical$', views.ethicalStrategy),
    url(r'^growth$', views.growthStrategy),
    url(r'^indexInvesting$', views.indexStrategy),
    url(r'^quality$', views.qualityStrategy),
    url(r'^value$', views.valueStrategy),
    url(r'^livePortFolio$', views.livePortFolio),
]
