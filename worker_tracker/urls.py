from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import workers.views

# Examples:
# url(r'^$', 'worker_tracker.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', workers.views.index, name='index'),
]
