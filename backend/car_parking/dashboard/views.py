from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from common.helpers import convert_string_date_into_date_format
from . import helpers


class DashBoardAPIView(APIView):
    def get(self, request):
        try:
            from_date = convert_string_date_into_date_format(request.query_params.get('from_date', None))
            to_date = convert_string_date_into_date_format(request.query_params.get('to_date', None))
            dashboard_statics = helpers.get_dashboard_based_on_given_from_to_date(request, from_date, to_date)
            return Response(dashboard_statics)

        except Exception as err:
            return Response({
                'message': f"While fetching data got exception, Please try after sometime {str(err)}",
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR
            })

