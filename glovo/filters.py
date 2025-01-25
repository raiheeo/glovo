from django_filters import FilterSet, NumberFilter
from .models import *
from django_filters import rest_framework as filters


class ReviewFilter(FilterSet):
    review_min = NumberFilter(field_name='store_rating', lookup_expr='gte', label='Min rating')
    review_max = NumberFilter(field_name='store_rating', lookup_expr='lte', label='Max rating')

    class Meta:
        model = Review
        fields = ['store_rating']

class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = {
            'category_name': ['exact']
        }


class DiscountFilter(filters.FilterSet):
    store = filters.ModelMultipleChoiceFilter(
        field_name='store__store_name',
        to_field_name='store_name',
        queryset=Store.objects.all()
    )

    class Meta:
        model = Discount
        fields = ['active', 'discount_type', 'store']
