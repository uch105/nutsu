from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from decouple import config

maintainance_mode = True if config('MAINTAINANCE_MODE') == 'YES' else False

if maintainance_mode:
    urlpatterns = [
        path('', views.maintainance_view, name='maintenance_page'),
        path('<path:path>', views.maintainance_view_all, name='maintenance_page_catchall')
    ] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
else:
    urlpatterns = [
        path('',views.home,name="home"),
        path('terms-and-conditions-and-privacy-policy/', views.terms_privacy, name='terms_privacy'),
        path('projects/',views.projects,name="projects"),
        path('checkout/',views.checkout,name="checkout"),
        path('create_payment/<str:pk0>/<str:pk1>/<str:pk2>/<str:pk3>/',views.create_payment,name="payment"),
        path('newsletter/',views.newsletter,name="newsletter"),
        path('newsletter/news/<str:pk>/',views.news,name="news"),
        path('about/',views.about,name="about"),
        path('admin/create/newsletter/',views.create_newsletter,name="create_newsletter"),
        path('admin/create/newsletter/block/',views.create_newsletter_block,name="create_newsletter_block"),
        path('queries/', views.query_list, name='query_list'),
        path('load-more-queries/', views.load_more_queries, name='load_more_queries'),
        path('download-today-log/',views.download_today_log,name="download-today-log"),
    ] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)