from django.urls import path

from link import views

urlpatterns = [
    path('reset/', views.ResetView.as_view(), name='reset'),
    path('reset_2020/', views.Reset2020View.as_view(), name='reset_2020'),
    path('reset_mp4/', views.ResetMP4View.as_view(), name='reset_mp4'),
    path('reset_tmuf/', views.ResetTMUFView.as_view(), name='reset_tmuf')
]