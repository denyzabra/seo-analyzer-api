from rest_framework import viewsets, status
from rest_framework.decorators import action 
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import ContentAnalysis
from .serializers import ContentAnalysisSerializer, ContentSubmissionSerializer
from .tasks import analyze_content_task

class ContentAnalysisViewSet(viewsets.ModelViewSet):
    queryset = ContentAnalysis.objects.all()
    serializer_class = ContentAnalysisSerializer

    def get_queryset(self):
        """Query optimization with select_related and prefetch_related"""
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset.order_by('-created_at')


    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        """List all analysis with caching"""
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['post'], url_path='submit')
    def submit_for_analysis(self, request):
        """Submit content for SEO analysis"""
        serializer = ContentSubmissionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        #create analysis record
        analysis =  ContentAnalysis.objects.create(
            content=serializer.validated_data['content'],
            url=serializer.validated_data.get('url', ''),
            status = 'pending'
        )

        #queue celery task
        task = analyze_content_task.delay(analysis.id)
        analysis.task_id = task.id
        analysis.save()

        return Response(
            {
                'id': analysis.id,
                'task_id': task.id,
                'status': 'pending',
                'message': 'Analysis queued successfully'
            },
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['get'], url_path='status')
    def check_status(self, request, pk=None):
        """Check analysis status"""
        analysis = self.get_object()
        serializer = self.get_serializer(analysis)
        return Response(serializer.data)
