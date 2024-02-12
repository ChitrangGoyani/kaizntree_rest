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
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiParameter, OpenApiExample, OpenApiTypes
from django.core.cache import cache
from rest_framework.response import Response

sortByExamples = [
    OpenApiExample("Category", value="category"),
    OpenApiExample("SKU", value="sku"),
    OpenApiExample("Descending Name", value="-name"),
    OpenApiExample("Ascending Name", value="name")
]

def length_checks(category, tag, sku):
    return len(str(category)) <= 30 and len(str(tag)) <= 10 and len(str(sku)) <= 12

@extend_schema(
    request=ItemSerializer,
    responses=ItemSerializer,
    description="Get items with pagination"
)
@api_view(['GET'])
def getItems(request):
    paginator = PageNumberPagination()
    paginator.page_size = 5
    filterset = ItemFilter(request.GET, queryset=Item.objects.all())
    if not filterset.is_valid():
        raise translate_validation(filterset.errors)
    queryset = paginator.paginate_queryset(filterset.qs, request)
    serializer = ItemSerializer(queryset, many=True)
    paginated = paginator.get_paginated_response(serializer.data)
    return paginated

@extend_schema(
    request=ItemSerializer,
    responses=ItemSerializer,
    description="Add a single item"
)
@api_view(['POST'])
def addItem(request):
    if request.data:
        if request.data['available_stock'] < request.data['in_stock']:
            return Response("Available Stock should be > In Stock", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif not length_checks(request.data['category'], request.data['tag'], request.data['sku']):
            return Response("Incorrect length for category, tag or sku", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response("Failed to add item, please check request body format.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response("Empty or malformed request body", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    parameters=[OpenApiParameter(name="id", description="Item Id", examples=[OpenApiExample("Id", "2")])],
    request=ItemSerializer,
    responses=ItemSerializer,
    description="Delete an item"
)
@api_view(['DELETE'])
def deleteItem(request):
    item = get_object_or_404(Item, id=request.GET['id'])
    item.delete()
    return Response("Item deleted.", status=status.HTTP_200_OK)

@extend_schema(
    parameters=[OpenApiParameter(name="id", description="Item Id", examples=[OpenApiExample("Id", "2")])],
    request=ItemSerializer,
    responses=ItemSerializer,
    description="Get a single item"
)
@api_view(['GET'])
def getItem(request):
    if request.GET:
        id = request.GET['id']
        cache_key = f'item:{id}'
        if cache_key in cache:
            return Response(cache.get(cache_key), status=status.HTTP_200_OK)
        item = get_object_or_404(Item, id=id)
        serializer = ItemSerializer(item)
        cache.set(cache_key, serializer.data, timeout=(60*5))
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response("Missing item id in query.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    parameters=[OpenApiParameter(name="id", description="Item Id", examples=[OpenApiExample("Id", "2")])],
    request=ItemSerializer,
    responses=ItemSerializer,
    description="Update an item"
)
@api_view(['PUT'])
def updateItem(request):
    if request.data and request.GET:
        if request.data['available_stock'] < request.data['in_stock']:
            return Response("Available Stock should be > In Stock", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif not length_checks(request.data['category'], request.data['tag'], request.data['sku']):
            return Response("Incorrect length for category, tag or sku", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            item = get_object_or_404(Item, id=request.GET['id'])
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response("Failed to update item, please check request body format.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response("Empty or malformed request body and/or item id not specified.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    parameters=[
        OpenApiParameter(name="category", description="Category of the item", examples=[OpenApiExample("Raw Material", value="Raw"), OpenApiExample("Finished Material", value="Finished")]),
        OpenApiParameter(name="tag", description="Tag of the item", examples=[OpenApiExample("Etsy.com", value="ETSY"), OpenApiExample("Shopify", value="SHOPIFY")]),
        OpenApiParameter(name="stock_status", description="Stock Status", examples=[OpenApiExample("True", value="True")]),
        OpenApiParameter(name="in_stock", description="In Stock count", examples=[OpenApiExample("Count", value="10")]),
        OpenApiParameter(name="in_stock__gte", description="In Stock count >=", examples=[OpenApiExample("Count", value="10")]),
        OpenApiParameter(name="in_stock__lte", description="In Stock count <=", examples=[OpenApiExample("Count", value="10")]),
        OpenApiParameter(name="in_stock__lt", description="In Stock count <", examples=[OpenApiExample("Count", value="10")]),
        OpenApiParameter(name="in_stock__gt", description="In Stock count >", examples=[OpenApiExample("Count", value="10")]),
        OpenApiParameter(name="available_stock__gte", description="Available Stock count >=", examples=[OpenApiExample("Count", value="10")]),
        OpenApiParameter(name="available_stock__lte", description="Available Stock count <=", examples=[OpenApiExample("Count", value="10")]),
        OpenApiParameter(name="available_stock__lt", description="Available Stock count <", examples=[OpenApiExample("Count", value="10")]),
        OpenApiParameter(name="available_stock__gt", description="Available Stock count >", examples=[OpenApiExample("Count", value="10")]),
        OpenApiParameter(name="createdAt_before", description="Created At range", type=OpenApiTypes.DATETIME, examples=[OpenApiExample("before", value="2024-12-31T23:59:59")]),
        OpenApiParameter(name="createdAt_after", description="Created At range", type=OpenApiTypes.DATETIME, examples=[OpenApiExample("after", value="2022-01-01T00:00:00")]),
        OpenApiParameter(name="updatedAt_before", description="Updated At range", type=OpenApiTypes.DATETIME, examples=[OpenApiExample("before", value="2024-12-31T23:59:59")]),
        OpenApiParameter(name="updatedAt_after", description="Updated At range", type=OpenApiTypes.DATETIME, examples=[OpenApiExample("after", value="2022-01-01T00:00:00")]),
        OpenApiParameter(name="search", description="Item Search", examples=[OpenApiExample("Item", value="HairProduct")]),
        OpenApiParameter(name="order", description="Sort by", examples=sortByExamples),
    ],
    request=ItemSerializer,
    responses=ItemSerializer,
    description="Filter, Search and Sort"
)
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