from rest_framework import serializers

from feeds.models import Post

class PostSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(slug_field='username', read_only=True)


    class Meta:
        model = Post
        fields = ('author', 'content', 'created_at')

    def create(self, validated_data):
        return Post.objects.create(author=self.context['request'].user, **validated_data)

class FeedSerializer(serializers.Serializer):
    
    posts = PostSerializer(many=True)