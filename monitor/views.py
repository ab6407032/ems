import json
import operator
from functools import reduce
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from filters import DynamicSearchFilter, Filter
from paginator import CustomPagination
from common.serializers import EmptySerializer
from monitor.models import Node
from monitor.serializers import NodeSerializer
from common.views import UUIDAltModelViewSet
from rest_framework.parsers import (MultiPartParser, JSONParser)

class NodeMonitorViewset(UUIDAltModelViewSet):
    queryset = Node.objects.all().filter(active=True)
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    serializer_class = EmptySerializer
    pagination_class = CustomPagination
    filter_backends = (DynamicSearchFilter,)
    parser_classes = (MultiPartParser, JSONParser)

    serializer_classes = {
        'list': NodeSerializer,
        'retrieve': NodeSerializer
    }

    search_parameters = (
        'node_name', 'user__id', 'user__email'
    )

    def get_object(self, id):
        try:
            return Node.objects.filter(id=id).filter(user=self.request.user).first()
        except Node.DoesNotExist:
            return None

    def get_queryset(self):
        """ allow rest api to filter by submissions """
        queryset = Node.objects.filter(user=self.request.user).order_by('-created_on')
        return queryset

    def retrieve(self, request, version, id=None):
        node = self.get_object(id)
        serializer = self.get_serializer(node, context={'request': request})
        return Response(serializer.data)

    