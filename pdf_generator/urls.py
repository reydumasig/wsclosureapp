from django.urls import path
from . import views

urlpatterns = [
    path('', views.template_list, name='template_list'),
    path('upload/', views.upload_template, name='upload_template'),
    path('generate/<int:template_id>/', views.generate_pdf, name='generate_pdf'),
    path('generated/', views.generated_pdf_list, name='generated_pdf_list'),
]