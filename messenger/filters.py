from django_filters import rest_framework as filters

from base.filters import NumberInFilter
from messenger.models import Message


class MessageFilter(filters.FilterSet):
    tags = NumberInFilter(field_name="tags__id", lookup_expr="in", distinct=True)

    class Meta:
        model = Message
        fields = ("user", "tags")
