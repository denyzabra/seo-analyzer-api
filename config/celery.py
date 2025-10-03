import os 
from celery import Celery

#set django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

#creae celery app
app = Celery('seo_analyzer')

#load config from djanog settings
app.config_from_object('django.conf:settings', namespace='CELERY')


##auto dsicover taskas in all installed apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    