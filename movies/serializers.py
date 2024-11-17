from rest_framework import serializers
from .models import Movie, RatingChoices


class MovieSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, required=False, allow_blank=True, default="")
    rating = serializers.ChoiceField(
        choices=RatingChoices.choices,
        default=RatingChoices.G,
    )
    synopsis = serializers.CharField(required=False, allow_blank=True, default="")

    added_by = serializers.EmailField(source="user.email", read_only=True)

    def save(self, **kwargs):
        if 'request' in self.context:
            user = self.context['request'].user

        if user and user.is_authenticated:
            self.validated_data['user'] = user

        return super().save(**kwargs)

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'duration', 'rating', 'synopsis', 'added_by']
