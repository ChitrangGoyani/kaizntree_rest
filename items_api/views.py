from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Item
from items_api.filters import ItemFilter
from .serializers import ItemSerializer
from rest_framework import status, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django_filters.utils import translate_validation

from django.shortcuts import get_object_or_404

@api_view(['GET'])
def getItems(request):
    paginator = PageNumberPagination()
    paginator.page_size = 2
    filterset = ItemFilter(request.GET, queryset=Item.objects.all())
    if not filterset.is_valid():
        raise translate_validation(filterset.errors)
    queryset = paginator.paginate_queryset(filterset.qs, request)
    serializer = ItemSerializer(queryset, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
def addItem(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteItem(request):   
    item = get_object_or_404(Item, id=request.data['id'])
    item.delete()
    return Response("Item deleted", status=status.HTTP_200_OK)

@api_view(['GET'])
def getItem(request):
    item = get_object_or_404(Item, id=request.data['id'])
    serializer = ItemSerializer(item)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def filterItems(request):
    items_qs = Item.objects.all()
    filterset = ItemFilter(request.GET, queryset=items_qs)
    if filterset.is_valid():
        items_qs = filterset.qs
    serializer = ItemSerializer(items_qs, many=True)
    return Response(serializer.data)


