from django.contrib.auth import get_user_model
from rest_framework import generics, mixins, viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.serializers import (
    UserCreateSerializer,
    UserManageSerializer,
    UserDetailSerializer,
    UserListSerializer,
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserManageSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = get_user_model().objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer

        return UserListSerializer

    @action(
        detail=True,
        methods=["GET"],
        permission_classes=[IsAuthenticated],
        authentication_classes=[JWTAuthentication],
        url_path="follow"
    )
    def follow_unfollow(self, request, pk=None) -> Response:
        user_to_follow = self.get_object()

        if user_to_follow == request.user:
            return Response(
                {"error": "You cannot follow/unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST)

        is_following = request.user in user_to_follow.subscribers.all()

        if is_following:
            user_to_follow.subscribers.remove(request.user)
        else:
            user_to_follow.subscribers.add(request.user)

        serializer = UserDetailSerializer(user_to_follow)

        return Response(
            {"is_following": not is_following, "user": serializer.data}
        )
