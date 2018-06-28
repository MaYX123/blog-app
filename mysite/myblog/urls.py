from django.urls import path

from . import views

app_name = 'myblog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # 不要使用<slug:slugtitle>，因为slug在django2.0.6中不支持中文。
    path('post/<str:slugtitle>/', views.detail, name='detail'),
    # path('archive/<int:year>/<int:month>/', views.archive, name='archive'),
    path('archive/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archive'),
    path('category/<int:pk>', views.CategoryView.as_view(), name='category'),
    path('tag/<int:pk>', views.TagView.as_view(), name='tag'),
    path('about', views.about, name='about'),
    path('signin', views.signin, name='signin'),
    path('register', views.register, name='register'),
]
