from django.urls import path
from . import views

app_name = 'votingContract'
urlpatterns = [
    path('dashboard', views.IndexView.as_view(), name='dashboard'),
    path('', views.setDefaultAccount.as_view(), name='login'),
    path('addCandidate',views.AddCandidates.as_view(), name='AddCandidates')

]
