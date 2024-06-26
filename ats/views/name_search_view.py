from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ats.models import Candidate
from ats.serializers import CandidateSerializer
from django.db.models import Q
from ats.constants import ErrorMessages

class NameSearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip()
        if not query:
            return Response({"error": ErrorMessages.QUERY_PARAMS_NOT_FOUND.value}, status=status.HTTP_400_BAD_REQUEST)

        query_tokens = query.lower().split()

        # Initialize a Q object for dynamic query construction
        query_filter = Q()

        # Dynamically construct query to match any of the query tokens in name
        for token in query_tokens:
            query_filter |= Q(name__icontains=token)

        # Get all candidates and filter matched candidates
        all_candidates = Candidate.objects.all()
        matched_candidates = all_candidates.filter(query_filter)

        # Exclude matched candidates to get unmatched candidates
        unmatched_candidates = all_candidates.exclude(id__in=matched_candidates.values_list('id', flat=True))

        # Sort matched candidates by relevance score and character match count
        sorted_matched_candidates = sorted(
            matched_candidates,
            key=lambda candidate: (
                -self._relevance_score(candidate.name.lower(), query_tokens),  # Reverse sort by relevance score
                -self._matching_character_count(candidate.name.lower(), query.lower())  # Reverse sort by character match count
            )
        )

        # Sort unmatched candidates by relevance score and character match count
        sorted_unmatched_candidates = sorted(
            unmatched_candidates,
            key=lambda candidate: (
                -self._relevance_score(candidate.name.lower(), query_tokens),  # Reverse sort by relevance score
                -self._matching_character_count(candidate.name.lower(), query.lower())  # Reverse sort by character match count
            )
        )

        # Combine sorted matched and unmatched candidates
        sorted_candidates = sorted_matched_candidates + sorted_unmatched_candidates

        # Serialize sorted candidates with matching score and character match count
        serializer = CandidateSerializer(sorted_candidates, many=True)
        serialized_candidates = serializer.data

        # Add matching score and character count to serialized data
        for serialized_data in serialized_candidates:
            serialized_data['matching_score'] = self._relevance_score(serialized_data['name'].lower(), query_tokens)
            serialized_data['matching_character_count'] = self._matching_character_count(serialized_data['name'].lower(), query.lower())

        return Response(serialized_candidates)

    def _relevance_score(self, name:str, query_tokens:list)->int:
        """
        Calculate the relevance score between a candidate's name and a search query.

        Args:
        - name (str): The candidate's name to compare.
        - query_tokens (list): A list of tokens extracted from the search query.

        Returns:
        int: The relevance score based on the number of matched tokens.
        """
        name_tokens = set(name.split())

        # Count the number of common words between name_tokens and query_tokens
        word_overlap = len(name_tokens & set(query_tokens))
        return word_overlap

    def _matching_character_count(self, name:str, query:str)->int:
        """
        Calculate the number of characters matching between candidate's name and search query.

        Args:
        - name (str): The candidate's name to compare.
        - query (str): The search query.

        Returns:
        int: The number of characters in the candidate's name that match the query.
        """
        # Convert both name and query to lowercase for case-insensitive comparison
        name_lower = name.lower()
        query_lower = query.lower()

        # Initialize pointers for both name and query
        name_index = 0
        query_index = 0
        matching_count = 0

        while name_index < len(name_lower) and query_index < len(query_lower):
            if name_lower[name_index] == query_lower[query_index]:
                matching_count += 1
                query_index += 1
            name_index += 1

        return matching_count
