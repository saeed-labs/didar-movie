from rest_framework import serializers

from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    movie_id = serializers.IntegerField(source='movie.id', read_only=True)
    title = serializers.CharField(source='movie.title', read_only=True)
    slug = serializers.CharField(source='movie.slug', read_only=True)
    image = serializers.ImageField(source='movie.image', read_only=True)
    price = serializers.IntegerField(source='movie.price', read_only=True)

    class Meta:
        model = CartItem
        fields = ('movie_id', 'title', 'slug', 'image', 'price', 'created_at',)



class AddCartItemSerializer(serializers.Serializer):
    movie_id = serializers.IntegerField()