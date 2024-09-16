from django.urls import path
from recruitment.views import CandidateView

urlpatterns = [
    path('candidate/', CandidateView.as_view()),
    path('candidate/<int:pk>/', CandidateView.as_view())
]
