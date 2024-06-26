from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ats.models import Candidate
from ats.serializers import CandidateSerializer
from django.db.models import Q, Value, CharField, IntegerField, Count
from ats.constants import ErrorMessages
from django.db.models.functions import Length
from django.db import connection


class NameSearchView(APIView):
    def get(self, request, *args, **kwargs)->Response:
        query = request.GET.get('q', '').strip()
        if not query:
            return Response({"error": ErrorMessages.QUERY_PARAMS_NOT_FOUND.value}, status=status.HTTP_400_BAD_REQUEST)

        get_query_data = self._get_query_data(query)

        return Response(get_query_data)
    
    def _get_query_data(self, query :str)->list:
        all_columns = ",".join([field.name for field in Candidate._meta.get_fields()])
        with connection.cursor() as cursor:
            sql_query = f"""SELECT {all_columns}, COUNT(*) AS match_count
            FROM {Candidate._meta.db_table}
            CROSS JOIN unnest(string_to_array('{query}', ' ')) AS word
            WHERE name ILIKE '%' || word || '%'
            GROUP BY {all_columns}
            ORDER BY match_count DESC;"""
            cursor.execute(sql_query)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            results = [dict(zip(columns, row)) for row in rows]
        cursor.close()
        return results