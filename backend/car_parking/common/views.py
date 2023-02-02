from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from . import constants

RESPONSE_MESSAGE = {
    status.HTTP_200_OK: 'OK',
    status.HTTP_201_CREATED: 'Created',
    status.HTTP_204_NO_CONTENT: 'No Content',
    status.HTTP_400_BAD_REQUEST: 'Bad Request',
    status.HTTP_401_UNAUTHORIZED: 'Unauthorized',
    status.HTTP_403_FORBIDDEN: 'Forbidden',
    status.HTTP_404_NOT_FOUND: 'Not Found'
}


class BaseViewSet(viewsets.ModelViewSet):
    model = None
    filterset_class = None
    view_serializers = {}

    def get_serializer_class(self):
        serializer_dict = self.view_serializers

        if not serializer_dict:
            return self.serializer_class

        request_action = self.action
        retrieve_serializer = serializer_dict[constants.Action.RETRIEVE]
        if request_action == constants.Action.LIST:
            return serializer_dict[request_action]
        elif request_action == constants.Action.PARTIAL_UPDATE:
            partial_update_serializer = serializer_dict.get(request_action, None)
            return partial_update_serializer if partial_update_serializer else retrieve_serializer
        return retrieve_serializer

    @action(methods=[constants.HTTPMethod.GET], detail=True)
    def view(self, *args, **kwargs):
        obj = self.get_object()
        serializer = self.view_serializers[self.action](obj, context={"request": self.request})
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.username, updated_on=datetime.now())
