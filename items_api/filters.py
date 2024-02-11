from django_filters.rest_framework import FilterSet

from base.models import Item
class ItemFilter(FilterSet):
    class Meta:
        model = Item
        fields = ['category', 'tag']