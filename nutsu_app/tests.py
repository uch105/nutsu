import os
import sys
import django
from decouple import config

project_root = config("PROJECT_ROOT")
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutsu.settings')
django.setup()

from nutsu_app.models import Newsletter

news = Newsletter.objects.all()
news[0].delete()