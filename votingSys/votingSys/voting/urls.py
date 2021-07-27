from django.urls import path
from . import views

app_name = 'voting'
urlpatterns = [
    path('', views.setDefaultAccount.as_view(), name='login'),
    path('dashboard', views.IndexView.as_view(), name='dashboard'),
    path('voteCandidate',views.voteCandidate.as_view(), name='voteCandidate'),

  
]

#   path('displayAccount', views.displayAccount.as_view(), name='displayAccount')