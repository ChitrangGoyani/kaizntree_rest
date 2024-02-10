from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Item
from .serializers import ItemSerializer
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

@api_view(['GET'])
def getItems(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

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
    standard_filters = ['category','tag']
    request_filters = request.GET
    print(request_filters)
    
    # queryset = Item.objects.filter(**filter_query)
    # serializer = ItemSerializer(queryset, many=True)
    # return Response(serializer.data)
    return Response(status=status.HTTP_200_OK)


