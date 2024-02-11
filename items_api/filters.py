from django_filters.rest_framework import FilterSet
from django_filters import rest_framework as filters
from django.db.models import Q

from base.models import Item
class ItemFilter(FilterSet):
    in_stock__gte = filters.NumberFilter(field_name="in_stock", lookup_expr='gte', label="In Stock >=")
    available_stock__gte = filters.NumberFilter(field_name="available_stock", lookup_expr='gte', label="Available Stock >=")
    in_stock__lte = filters.NumberFilter(field_name="in_stock", lookup_expr='lte', label="In Stock <=")
    available_stock__lte = filters.NumberFilter(field_name="available_stock", lookup_expr='lte', label="Available Stock <=")
    in_stock__lt = filters.NumberFilter(field_name="in_stock", lookup_expr='lt', label="In Stock <")
    available_stock__lt = filters.NumberFilter(field_name="available_stock", lookup_expr='lt', label="Available Stock <")
    in_stock__gt = filters.NumberFilter(field_name="in_stock", lookup_expr='gt', label="In Stock >")
    available_stock__gt = filters.NumberFilter(field_name="available_stock", lookup_expr='gt', label="Available Stock >")
    createdAt = filters.DateTimeFromToRangeFilter(field_name='createdAt') # generates: createdAt_before & createdAt_after
    updatedAt = filters.DateTimeFromToRangeFilter(field_name='updatedAt')
    search = filters.CharFilter(method='perform_search', label='Search')
    ordering = filters.OrderingFilter(fields=['name','sku','category','in_stock','available_stock','tag'],label='Ordering') # sorting

    def perform_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(sku__icontains=value))

    class Meta:
        model = Item
        fields = ['category', 'tag', 'stock_status', 'in_stock', 'available_stock']