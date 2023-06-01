from rest_framework import serializers

from feed.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "author")
