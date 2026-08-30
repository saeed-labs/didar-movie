from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.models import MoviesModel

from .models import Cart, CartItem
from .serializers import AddCartItemSerializer, CartItemSerializer


class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = cart.items.select_related('movie')

        serializer = CartItemSerializer(items, many=True, context={'request': request})

        # total_price = 0
        # for item in items:
        #     total_price += item.movie.price

        total_price = sum(item.movie.price for item in items)

        return Response({
            'items': serializer.data,
            'total_price': total_price,
        }, status=status.HTTP_200_OK)


class AddCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # serializer = AddCartItemSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # movie = get_object_or_404(MoviesModel, is_active=True, id=serializer.validated_data['movie_id'])

        movie = get_object_or_404(MoviesModel, is_active=True, id=pk)

        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(movie=movie, cart=cart)

        if not created:
            return Response({'message': 'این فیلم قبلا در سبدخرید شما وجود دارد'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(CartItemSerializer(cart_item, context={'request': request}).data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, movie_id=pk)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

