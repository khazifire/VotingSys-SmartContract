from django.urls import path
from . import views

app_name = 'votingContract'
urlpatterns = [
    path('login', views.setDefaultAccount.as_view(), name='login'),
    path('dashboard', views.IndexView.as_view(), name='dashboard'),
    path('addCandidate',views.AddCandidates.as_view(), name='addCandidates'),
    path('registerAccount',views.RegisterAccountView.as_view(), name='registerAccount'),
  
]

#   path('displayAccount', views.displayAccount.as_view(), name='displayAccount')