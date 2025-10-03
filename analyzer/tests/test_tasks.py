import pytest
from unittest.mock import patch, MagicMock
from analyzer.tasks import analyze_content_task
from analyzer.models import ContentAnalysis

@pytest.mark.django_db
class TestAnalyzeContentTask:
    @patch('analyzer.tasks.ChatOpenAI')
    def test_analyze_content_success(self, mock_openai):
        """Test successful content analysis"""
        # Create test analysis
        analysis = ContentAnalysis.objects.create(
            content="This is sample SEO content for testing." * 20,
            status="pending"
        )
        
        # Mock LangChain response
        mock_openai.return_value.invoke.return_value = {
            'seo_score': '85',
            'recommendations': 'Add more keywords'
        }
        
        # Run task
        result = analyze_content_task(analysis.id)
        
        # Verify
        analysis.refresh_from_db()
        assert analysis.status == 'completed'
        assert analysis.seo_score is not None
        assert analysis.keyword_density is not None
