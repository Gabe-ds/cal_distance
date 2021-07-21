from django.urls import path
from . import views

app_name = "isbs"

urlpatterns = [
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('upload_list/', views.UploadListView.as_view(), name='upload_list'),
    path('upload_list/<int:pk>/delete/', views.DeleteView.as_view(), name="delete"),
]