from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "username",
            "is_staff",
        )
        read_only_fields = ("id", "is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class UserDetailSerializer(serializers.ModelSerializer):
    subscribed_to = serializers.SlugRelatedField(
        slug_field="username",
        many=True,
        read_only=True
    )
    subscribers = serializers.SlugRelatedField(
        slug_field="username",
        many=True,
        read_only=True
    )

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "bio",
            "avatar",
            "subscribed_to",
            "subscribers",
            "is_staff"
        )


class UserManageSerializer(UserDetailSerializer):
    class Meta(UserDetailSerializer.Meta):
        read_only_fields = ("id", "is_staff", "subscribed_to")

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserListSerializer(serializers.ModelSerializer):
    subscribers_number = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "username",
            "subscribers_number",
            "is_staff"
        )

    def get_subscribers_number(self, obj):
        return obj.subscribers.count()
