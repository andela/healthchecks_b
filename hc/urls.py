from django.conf.urls import include, url
from django.contrib import admin
<<<<<<< HEAD
from django.conf import settings
from django.contrib.staticfiles import views
=======
>>>>>>> d244a1918ad9631574b6a4e9021a3ea45f4d8359

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('hc.accounts.urls')),
    url(r'^', include('hc.api.urls')),
    url(r'^', include('hc.front.urls')),
    url(r'^', include('hc.payments.urls'))
]

# if settings.DEBUG:
urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
    ]
