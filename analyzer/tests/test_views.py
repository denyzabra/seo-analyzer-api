import pytest
from rest_framework.test import APIClient
from analyzer.models import ContentAnalysis
from unittest.mock import patch, MagicMock

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_analysis():
    return ContentAnalysis.objects.create(
        content="Sample SEO content for testing purposes." * 10,
        url="https://test.com",
        status="completed",
        seo_score=75
    )

@pytest.mark.django_db
class TestContentAnalysisViewSet:
    def test_list_analyses(self, api_client, sample_analysis):
        """Test listing all analyses"""
        response = api_client.get('/api/analyses/')
        assert response.status_code == 200
        assert len(response.data) >= 1
    
    def test_retrieve_analysis(self, api_client, sample_analysis):
        """Test retrieving single analysis"""
        response = api_client.get(f'/api/analyses/{sample_analysis.id}/')
        assert response.status_code == 200
        assert response.data['id'] == sample_analysis.id
    
    @patch('analyzer.views.analyze_content_task.delay')
    def test_submit_content(self, mock_task, api_client):
        """Test submitting content for analysis"""
        mock_task.return_value = MagicMock(id='test-task-id')
        
        data = {
            'content': 'This is test content for SEO analysis. ' * 10,
            'url': 'https://example.com'
        }
        
        response = api_client.post('/api/analyses/submit/', data, format='json')
        
        assert response.status_code == 201
        assert 'id' in response.data
        assert 'task_id' in response.data
        assert response.data['status'] == 'pending'
        mock_task.assert_called_once()
