from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Item
from items_api.filters import ItemFilter
from .serializers import ItemSerializer
from rest_framework import status
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django_filters.utils import translate_validation
from django.shortcuts import get_object_or_404

from django.core.cache import cache
import time
import redis
from rest_framework.response import Response

@api_view(['GET'])
def getItems(request):
    paginator = PageNumberPagination()
    paginator.page_size = request.GET['pagesize']
    filterset = ItemFilter(request.GET, queryset=Item.objects.all())
    if not filterset.is_valid():
        raise translate_validation(filterset.errors)
    queryset = paginator.paginate_queryset(filterset.qs, request)
    serializer = ItemSerializer(queryset, many=True)
    paginated = paginator.get_paginated_response(serializer.data)
    return paginated

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
    id = request.GET['id']
    cache_key = f'item:{id}'
    if cache_key in cache:
        return Response(cache.get(cache_key), status=status.HTTP_200_OK)
    item = get_object_or_404(Item, id=id)
    serializer = ItemSerializer(item)
    cache.set(cache_key, serializer.data, timeout=(60*5))
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def filterItems(request):
    items_qs = Item.objects.all()
    filterset = ItemFilter(request.GET, queryset=items_qs)
    cache_key = f'filters:{filterset.data}'
    if cache_key in cache:
        return Response(cache.get(cache_key), status=status.HTTP_200_OK)
    if filterset.is_valid():
        items_qs = filterset.qs
    else:
        return Response("Incorrect filterset.", status=status.HTTP_400_BAD_REQUEST)
    serializer = ItemSerializer(items_qs, many=True)
    cache.set(cache_key, serializer.data, timeout=(60*5))
    return Response(serializer.data, status=status.HTTP_200_OK)

