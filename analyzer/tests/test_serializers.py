import pytest
from analyzer.serializers import ContentSubmissionSerializer

class TestContentSubmissionSerializer:
    def test_valid_submission(self):
        """Test valid content submission"""
        data = {
            'content': 'This is a valid content for SEO analysis. ' * 10,
            'url': 'https://example.com'
        }
        serializer = ContentSubmissionSerializer(data=data)
        assert serializer.is_valid()
    
    def test_short_content_fails(self):
        """Test content too short fails validation"""
        data = {'content': 'Too short'}
        serializer = ContentSubmissionSerializer(data=data)
        assert not serializer.is_valid()
        assert 'content' in serializer.errors
