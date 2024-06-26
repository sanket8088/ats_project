from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ats.models import Candidate
from ats.serializers import CandidateSerializer
from django.db.models import Q, Value, CharField
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
            
        # Create a SQL query similar to the following:
        # SELECT id, name, LENGTH(name) AS matching_character_count
        # FROM ats_candidate
        # WHERE (
        #     LOWER(name) LIKE '%token1%' OR
        #     LOWER(name) LIKE '%token2%' OR
        #     ...
        #     LOWER(name) LIKE '%tokenN%'
        # )
        # ORDER BY matching_character_count DESC;
        sorted_matched_candidates =  Candidate.objects.filter(query_filter).annotate(
            matching_character_count=Length('name')
        ).order_by('-matching_character_count')

       
        # Serialize sorted candidates with matching score and character match count
        serializer = CandidateSerializer(sorted_matched_candidates, many=True)
        serialized_candidates = serializer.data

        return Response(serialized_candidates)