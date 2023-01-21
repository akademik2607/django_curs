from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins, status
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer, ChangePasswordSerializer


class UserListView(ListAPIView, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserMeView(GenericAPIView, mixins.UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        obj = self.request.user
        return obj


class UserRetrieveView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get_object(self):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            if not instance.check_password(serializer.data.get('current_password')):
                return Response({'current_password':'wrong password'}, status=status.HTTP_400_BAD_REQUEST)
            instance.set_password(serializer.data.get('new_password'))
            instance.save()

            return Response({'new_password':serializer.data.get('new_password'),
                             'current_password':serializer.data.get('new_password')
                             }, status=status.HTTP_201_CREATED)
        Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


