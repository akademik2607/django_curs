from rest_framework import serializers
from ads.models import Ad, Comment


class CommentSerializer(serializers.ModelSerializer):
    author_id = serializers.SerializerMethodField()
    author_first_name = serializers.SerializerMethodField()
    author_last_name = serializers.SerializerMethodField()
    ad_id = serializers.SerializerMethodField()
    author_image = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['pk',
                  'text',
                  'author_id',
                  'created_at',
                  'author_first_name',
                  'author_last_name',
                  'ad_id',
                  'author_image']

    def get_author_id(self, obj):
        return obj.author.pk

    def get_author_first_name(self, obj):
        return obj.author.first_name

    def get_author_last_name(self, obj):
        return obj.author.last_name

    def get_author_image(self, obj):
        return str(obj.author.image)

    def get_ad_id(self, obj):
        return obj.ad.pk

    def create(self, validated_data):
        request = self.context.get("request")
        if hasattr(request, "user"):
            if request.user.__str__() != "AnonymousUser":
                validated_data["author"] = request.user
        _pk = request.parser_context.get('kwargs').get('ad_pk')
        validated_data['ad'] = Ad.objects.get(pk=_pk)

        return super().create(validated_data)


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get("request")
        if hasattr(request, "user"):
            if request.user.__str__() != "AnonymousUser":
                validated_data["author"] = request.user
        return super().create(validated_data)


class AdDetailSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField()
    author_first_name = serializers.SerializerMethodField()
    author_last_name = serializers.SerializerMethodField()
    author_id = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = ['pk',
                  'image',
                  'title',
                  'price',
                  'phone',
                  'description',
                  'author_first_name',
                  'author_last_name',
                  'author_id']

    def get_phone(self, obj, *args, **kwargs):
        return str(obj.author.phone)

    def get_author_first_name(self, obj, *args, **kwargs):
        return obj.author.first_name

    def get_author_last_name(self, obj, *args, **kwargs):
        return obj.author.last_name

    def get_author_id(self, obj):
        return obj.author.pk


class AdUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = ['image', 'title', 'price', 'description']
