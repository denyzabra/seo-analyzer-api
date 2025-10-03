from rest_framework import serializers
from .models import ContentAnalysis

class ContentAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentAnalysis
        fields = [
            'id', 'content', 'url', 'status', 'seo_score', 'keyword_density', 'readability_score', 'recommendations', 'created_at', 'updated_at', 'task_id'
        ]
        read_only_fields = [
            'id', 'status', 'seo_score', 'keyword_density', 'readability_score', 'recommendations', 'created_at', 'updated_at', 'task_id'
        ]

class ContentSubmissionSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=10000, required=True)
    url = serializers.URLField(required=False, allow_blank=True)

    def validate_content(self, value):
        if len(value.strip()) < 100:
            raise serializers.ValidationError(
                "Content must be at least 100 characters long."
            )
        return value
