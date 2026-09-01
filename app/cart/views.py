from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.models import MoviesModel

from .models import Cart, CartItem
from payment.models import Coupon, CouponUsage
from .serializers import CartItemSerializer, ApplyCouponSerializer


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
        discount_amount = 0
        coupon_data = None

        if cart.coupon and cart.coupon.is_active:
            discount_amount = (total_price * cart.coupon.discount) // 100
            coupon_data = {
                'code': cart.coupon.code,
                'discount': cart.coupon.discount,
            }

        final_price = total_price - discount_amount


        return Response({
            'items': serializer.data,
            'total_price': total_price,
            'discount_amount': discount_amount,
            'final_price': final_price,
            'coupon': coupon_data,
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

        return Response(CartItemSerializer(cart_item, context={'request': request}).data,
                        status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, movie_id=pk)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApplyCouponAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ApplyCouponSerializer

    @transaction.atomic
    def post(self, request):
        serializer = ApplyCouponSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code'].strip().upper()
        cart = (Cart.objects.select_for_update().prefetch_related('items__movie').get(user=request.user))
        coupon = Coupon.objects.filter(code=code, is_active=True).first()

        if not coupon:
            return Response({'detail': 'کد تخفیف معتبر نیست.'}, status=status.HTTP_400_BAD_REQUEST)

        if not coupon.is_valid:
            return Response({'detail': 'این کد تخفیف قابل استفاده نیست.'}, status=status.HTTP_400_BAD_REQUEST)

        if CouponUsage.objects.filter(coupon=coupon,user=request.user).exists():
            return Response(
                {'detail': 'شما قبلاً از این کد تخفیف استفاده کرده‌اید.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not cart.items.exists():
            return Response({'detail': 'سبد خرید خالی است.'}, status=status.HTTP_400_BAD_REQUEST)

        cart.coupon = coupon
        cart.save(update_fields=['coupon', 'updated_at'])

        return Response(
            {
                'detail': 'کد تخفیف با موفقیت اعمال شد.',
                'code': coupon.code,
                'discount': coupon.discount,
            }, status=status.HTTP_200_OK)
