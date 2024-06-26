from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ats.models import Candidate
from ats.serializers import CandidateSerializer
from ats.constants import ErrorMessages
class UpdateCandidateStatus(APIView):
    """
    API endpoint to update the status of a candidate.

    Supports PATCH method with 'operation' parameter to either 'shortlist' or 'reject' a candidate.

    - 'shortlist': Sets candidate status to 'Shortlisted'.
    - 'reject': Sets candidate status to 'Rejected'.
    """

    def patch(self, request, pk:int) -> Response:
        """
        Patch method to update candidate status based on 'operation' parameter.

        Parameters:
        - pk (int): Primary key of the candidate.

        Returns:
        - Response: Serialized data of the updated candidate or error response.
        """
        try:
            candidate = Candidate.objects.get(pk=pk)
        except Candidate.DoesNotExist:
            return Response({"error": ErrorMessages.CANDIDATE_NOT_FOUND_ERROR.value}, status=status.HTTP_404_NOT_FOUND)

        operation = request.data.get('operation') or request.query_params.get('operation')
        if not operation:
            return Response({"error": ErrorMessages.OPERATION_REQUIRED_ERROR.value}, status=status.HTTP_400_BAD_REQUEST)

        if operation.lower() == 'shortlist':
            candidate.status = 'Shortlisted'
        elif operation.lower() == 'reject':
            candidate.status = 'Rejected'
        else:
            return Response({"error": ErrorMessages.INVALID_OPERATION_ERROR.value}, status=status.HTTP_400_BAD_REQUEST)

        candidate.save()
        return Response(CandidateSerializer(candidate).data)
