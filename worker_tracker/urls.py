from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

from workers.views import *

# Examples:
# url(r'^$', 'worker_tracker.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^data', workerData, name='worker_data'),
    url(r'^hit', hitData, name='hit_data'),
    url(r'^worker', workerView, name='worker_view'),
]
