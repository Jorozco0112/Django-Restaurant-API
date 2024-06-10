from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import MenuItem, Category
from .serializers import CategorySerializer, MenuItemSerializer
from django.core.paginator import Paginator, EmptyPage


# Create your views here.


class MenuItemView(APIView):

    def get(self, request):

        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        page = request.query_params.get('page', default=1)
        perpage = request.query_params.get('perpage', default=10)

        if category_name:
            items = items.filter(category__title=category_name)

        if to_price:
            items = items.filter(price__lte=to_price)

        if search:
            items = items.filter(title__startswith=search)

        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)

        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []

        item_serialized = MenuItemSerializer(items, many=True)

        return Response(item_serialized.data)

    def post(self, request):
        serializer = MenuItemSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class MenuItemDetail(APIView):

    def get_one_item(self, request, pk):
        try:
            item = MenuItem.objects.get(pk=pk)
        except MenuItem.DoesNotExist:
            raise Http404

        item_serialized = MenuItemSerializer(item)

        return Response(item_serialized.data)

    def put(self, request, pk):
        try:
            item = MenuItem.objects.get(pk=pk)
        except MenuItem.DoesNotExist:
            raise Http404

        item_serialized = MenuItemSerializer(item, data=request.data)

        if item_serialized.is_valid(raise_exception=True):
            item_serialized.save()

            return Response(item_serialized.data, status.HTTP_200_OK)

        return Response(item_serialized.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            item = MenuItem.objects.get(pk=pk)
        except MenuItem.DoesNotExist:
            raise Http404

        item.delete()

        return Response(status.HTTP_204_NO_CONTENT)
