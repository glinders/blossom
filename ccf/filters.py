from django.db.models import (
    Q,
)
import django_filters
from ccf.models import Client


# see https://stackoverflow.com/a/52820205/4459346
class ClientFilter(django_filters.FilterSet):
    multi_name_fields = django_filters.CharFilter(
        label='Search',
        method='filter_all_name_fields',
    )

    class Meta:
        model = Client
        fields = []

    def filter_all_name_fields(self, queryset, name, value):
        return queryset.filter(
            Q(display_name__icontains=value) | Q(full_name__icontains=value)
        )
