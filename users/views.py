from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User
from users.serializer import UserSerializer
from users.permissions import IsUserOwner
from rest_framework.permissions import IsAuthenticated


class UsersView(APIView):

    def get_permissions(self):
        if self.request.method == "POST":
            return []
        return [IsAuthenticated(), IsUserOwner()]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request, user_id: int = None):
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                self.check_object_permissions(request, user)
            except User.DoesNotExist:
                return Response({"details": "User not found"}, status=404)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)

    def patch(self, request, user_id: int):
        if user_id:
            try:
                user_to_update = User.objects.get(id=user_id)
                self.check_object_permissions(request, user_to_update)
            except User.DoesNotExist:
                return Response({"details": "User not found"}, status=404)

        serializer = UserSerializer(user_to_update, data=request.data, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=200)
