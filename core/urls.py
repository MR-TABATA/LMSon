from django.contrib import admin
from django.urls import path, include
from .settings.base import DEBUG

from .settings import base
from django.contrib.staticfiles.urls import static

admin.site.site_header = base.SITE_NAME+'管理サイト'
admin.site.site_title = base.SITE_NAME+'管理サイト'

urlpatterns = [
  path('admin/', admin.site.urls),
  path('accounts/', include('accounts.urls')),
  path('course/', include('course.urls')),
  path('chapter/', include('chapter.urls')),
  path('exam/', include('exam.urls')),
  path('lesson/', include('lesson.urls')),
  path('notification/', include('notification.urls')),
  path('situation/', include('situation.urls')),
  path('', include('home.urls')),
  path('', include('user_sessions.urls', 'user_sessions')),
]
urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)

if DEBUG:
  import debug_toolbar
  urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]