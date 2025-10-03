from django.db import models
from django.utils import timezone

class ContentAnalysis(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    content = models.TextField(help_text="Content to analyze")
    url = models.URLField(blank=True, null=True, help_text="Optional URL source")
    
    # analysis results
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    seo_score = models.IntegerField(null=True, blank=True, help_text="SEO score 0-100")
    keyword_density = models.JSONField(null=True, blank=True, help_text="Top keywords")
    readability_score = models.FloatField(null=True, blank=True)
    recommendations = models.TextField(blank=True, help_text="AI recommendations")
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    task_id = models.CharField(max_length=255, blank=True, help_text="Celery task ID")
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Analysis {self.id} - {self.status}"
