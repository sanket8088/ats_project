from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from ats.models import Candidate
from ats.serializers import CandidateSerializer
import django_filters

class CandidateFilter(django_filters.FilterSet):
    min_expected_salary = django_filters.NumberFilter(field_name="expected_salary", lookup_expr='gte')
    max_expected_salary = django_filters.NumberFilter(field_name="expected_salary", lookup_expr='lte')
    min_age = django_filters.NumberFilter(field_name="age", lookup_expr='gte')
    max_age = django_filters.NumberFilter(field_name="age", lookup_expr='lte')
    min_years_of_exp = django_filters.NumberFilter(field_name="years_of_exp", lookup_expr='gte')
    phone_number = django_filters.CharFilter(field_name='phone_number', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    status = django_filters.CharFilter(field_name='status',  lookup_expr='icontains')

    class Meta:
        model = Candidate
        fields = ['min_expected_salary', 'max_expected_salary', 'min_age', 'max_age', 'min_years_of_exp', 'phone_number', 'email', 'name', 'status']

class CandidateListCreate(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CandidateFilter
    search_fields = ['phone_number', 'email', 'name']