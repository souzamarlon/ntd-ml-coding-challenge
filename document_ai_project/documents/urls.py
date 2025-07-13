from documents.views import DocumentUploadView
from django.urls import path

urlpatterns = [
    path('upload/', DocumentUploadView.as_view(), name='upload-document'),
]