from rest_framework import pagination, mixins
from rest_framework.generics import RetrieveAPIView, ListAPIView

from ads.models import Ad, Comment
from ads.permissions import EditPermission
from ads.serializers import AdDetailSerializer, AdSerializer, AdUpdateSerializer, CommentSerializer


class AdListView(ListAPIView, mixins.CreateModelMixin):
    queryset = Ad.objects.all()
    pagination_class = pagination.PageNumberPagination
    serializer_class = AdDetailSerializer

    def get(self, request, *args, **kwargs):
        title = request.query_params.get('title', None)
        if title:
            self.queryset = self.get_queryset().filter(title__icontains=title)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AdUserListView(ListAPIView):
    queryset = Ad.objects.all()
    pagination_class = pagination.PageNumberPagination
    serializer_class = AdSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        self.queryset = self.get_queryset().select_related("author").filter(author=user)
        return self.list(request, *args, **kwargs)


class AdView(RetrieveAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Ad.objects.select_related('author').all()
    serializer_class = AdDetailSerializer
    permission_classes = [EditPermission]

    def put(self, request, *args, **kwargs):
        self.change_serializer(AdUpdateSerializer)
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.change_serializer(AdUpdateSerializer)
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def change_serializer(self, serializer):
        self.serializer_class = serializer


class CommentListView(ListAPIView, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        _pk = request.parser_context.get('kwargs').get('ad_pk')
        self.queryset = self.get_queryset().filter(ad_id=_pk)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommentView(RetrieveAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Comment.objects.select_related('author').select_related('ad').all()
    serializer_class = CommentSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)







