from rest_framework import serializers

from styles.models import Style, StyleImage, StyleFile


class StyleImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = StyleImage
        fields = ["id", "image"]

class StyleSerializer(serializers.ModelSerializer):

    images = StyleImageSerializer(many=True, read_only=True)
    files = serializers.SerializerMethodField()

    likes = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField(read_only=True)
    downloads = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Style
        fields = '__all__'

    def get_files(self,obj):
        return [
            {
                "id": f.id,
                "file": f.file.url
            }
            for f in obj.files.all()
        ]

    def get_likes(self, obj):
        return obj.likes.count()

    def get_views(self, obj):
        return obj.views

    def get_downloads(self, obj):
        return obj.downloads

    def update(self,instance,validated_data):
        request = self.context['request']

        images = request.FILES.getlist("image")
        files = request.FILES.getlist("files")
        thumbnail = request.FILES.get("thumbnail")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        for img in images:
            StyleImage.objects.create(style=instance, image=img)


        if instance.requires_custom_file and files:
            for f in files:
                StyleFile.objects.create(style=instance, file=f)


        instance.thumbnail = self._resolve_thumbnail_update(
            instance,
            thumbnail,
            images
        )

        instance.save()
        return instance

    def _resolve_thumbnail_update(self, instance, explicit, new_images):

        if explicit:
            return explicit
        if new_images:
            return new_images[0]
        return instance.thumbnail

class StyleCreateSerializer(serializers.ModelSerializer):

    images = StyleImageSerializer(many=True, read_only=True)

    class Meta:
        model = Style
        fields = [
            "id",
            "title",
            "description",
            "game_class",
            "can_be_saved",
            "requires_custom_file"
        ]

    def create(self,validated_data):
        request = self.context['request']

        images = request.FILES.getlist('image')
        files = request.FILES.getlist('files')
        thumbnail = request.FILES.getlist('thumbnails')

        style = Style.objects.create(user=request.user, **validated_data)

        for img in images:
            StyleImage.objects.create(style=style, image=img)

        for f in files:
            StyleFile.objects.create(style=style, file=f)

        style.thumbnail = self._resolve_thumbnail(thumbnail,images)
        style.save()

        return style

    def _resolve_thumbnail(self,explicit_thumbnail,images):
        if explicit_thumbnail:
            return explicit_thumbnail
        if images:
            return images[0]

        return None


class StyleListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Style

        fields = [
            "id",
            "title",
            "thumbnail",
            "views"
        ]

class StyleDetailSerializer(serializers.ModelSerializer):
    images = StyleImageSerializer(many=True,read_only=True)
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Style
        fields = "__all__"