'''
페이지 요청 시 가장 먼저 호출되는 파일: 
요청 url과 view 함수(화면을 보여주는 함수)를 연결해주는 역할
'''
from django.contrib import admin
from django.urls import path, include
from pybo.views import base_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')), #pybo가 config 폴더에 있지 않으므로 pybo/urls 파일을 참고하도록 함
    path('common/', include('common.urls')), #common이 config 폴더에 있지 않으므로 pybo/urls 파일을 참고하도록 함
    path('', base_views.index, name='index'),  # '/' 에 해당되는 path
]
