from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validates_date):
            user = User.objects.create_user(**validates_date)
            return user


class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, date):
        user = authenticate(**date)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhotos
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = Rating
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')


    class Meta:
        model = Rating
        fields = ['first_name', 'last_name']


class ReviewSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer()
    ratings = RatingSerializer(many=True, read_only=True, )
    reviews = ReviewSerializer(many=True, read_only=True)
    product = ProductPhotosSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    date = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = Product
        fields = ['product_name', 'description', 'category', 'price', 'product',
                  'product_video', 'active', 'date', 'average_rating', 'ratings', 'reviews']

    def get_average_rating(self, obj):
        return obj.get_average_rating()