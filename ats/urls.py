from django.urls import path, include
from ats.views import CandidateListCreate, UpdateCandidateStatus, NameSearchView

urlpatterns = [
    path('candidates', CandidateListCreate.as_view(), name='candidate-list-create'),
    path('candidates/<int:pk>', UpdateCandidateStatus.as_view(), name='update-candidate-status'),
    path('candidates/search', NameSearchView.as_view(), name='name-search-candidate'),
]
