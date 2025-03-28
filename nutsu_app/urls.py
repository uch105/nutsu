from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name="home"),
    path('projects/',views.projects,name="projects"),
    path('newsletter/',views.newsletter,name="newsletter"),
    path('newsletter/news/<str:pk>/',views.news,name="news"),
    path('about/',views.about,name="about"),
    path('admin/create/newsletter/',views.create_newsletter,name="create_newsletter"),
    path('admin/create/newsletter/block/',views.create_newsletter_block,name="create_newsletter_block"),
    path('queries/', views.query_list, name='query_list'),
    path('load-more-queries/', views.load_more_queries, name='load_more_queries'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)