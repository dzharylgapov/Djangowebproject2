from django.urls import path

from . import views
from DjangoWebProject2 import settings


urlpatterns = [
    path('clients/', views.ClientView.as_view()),
    path('clients/<str:pk>', views.SingleClientView.as_view()),
    path('mailing/', views.MailingView.as_view()),
    path('mailing/<str:pk>', views.SingleMailingView.as_view()),

]
