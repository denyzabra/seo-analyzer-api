import pytest
from analyzer.models import ContentAnalysis

@pytest.mark.django_db
class TestContentAnalysisModel:
    def test_create_analysis(self):
        """Test creating a content analysis"""
        analysis = ContentAnalysis.objects.create(
            content = "this is test content for SEO analysis." * 10,
            url="https://example.com",
            status="pending"
        )

        assert analysis.id is not None
        assert analysis.status == "pending"
        assert analysis.seo_score is None
        assert str(analysis) == f"Analysis {analysis.id} - pending"

    def test_analysis_ordering(self):
        """Test analyses are ordered by creation date"""
        analysis1 = ContentAnalysis.objects.create(
            content="First analysis content" * 10
        )
        analysis2 = ContentAnalysis.objects.create(
            content="Second analysis content" * 10
        )
        
        analyses = ContentAnalysis.objects.all()
        assert analyses[0].id == analysis2.id