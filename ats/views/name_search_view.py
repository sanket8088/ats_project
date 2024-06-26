from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ats.models import Candidate
from ats.serializers import CandidateSerializer
from django.db.models import Q, Value, CharField, IntegerField
from ats.constants import ErrorMessages
from django.db.models.functions import Length

class NameSearchView(APIView):
    def get(self, request, *args, **kwargs)->Response:
        query = request.GET.get('q', '').strip()
        if not query:
            return Response({"error": ErrorMessages.QUERY_PARAMS_NOT_FOUND.value}, status=status.HTTP_400_BAD_REQUEST)

        query_tokens = query.lower().split()

        # Initialize a Q object for dynamic query construction
        query_filter = Q()
        for token in query_tokens:
            query_filter |= Q(name__icontains=token)

        # Find exact match candidates
        exact_match_candidates = Candidate.objects.filter(name__iexact=query).annotate(
            matching_character_count=Value(len(query), output_field=IntegerField())
        ).order_by('-matching_character_count')

        # Find partial match candidates, excluding exact matches, and annotate matching_character_count
        partial_match_candidates = Candidate.objects.filter(query_filter).annotate(
            matching_character_count=Length('name')
        ).exclude(
            id__in=exact_match_candidates.values_list('id', flat=True)
        ).order_by("-matching_character_count")
        combined_candidates = list(exact_match_candidates) + list(partial_match_candidates)
        serializer = CandidateSerializer(combined_candidates, many=True)
        serialized_candidates = serializer.data

        return Response(serialized_candidates)