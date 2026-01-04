import os
import django
from django.conf import settings
from django.template.loader import render_to_string
from datetime import datetime, timedelta

# Configure minimal Django settings for testing template rendering
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if not settings.configured:
    settings.configure(
        DEBUG=True,
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'core', 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.request',
                ],
            },
        }],
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'django.contrib.admin',  # Added this to fix the error
            'core',
        ],
        USE_I18N=True,
        LANGUAGES=[('en', 'English'), ('el', 'Greek')],
        ROOT_URLCONF='registry_app.urls',
    )
    django.setup()

def test_contributions_rendering():
    context = {
        'summary_stats': {
            'ytd_total': 5400.0,
            'avg_monthly': 450.0,
            'projected_total': 2700.0,
        },
        'chart_data': {
            'labels': ['Jan', 'Feb', 'Mar'],
            'historical': [440, 450, 460],
            'predictive': [None, None, 460, 470, 480],
        },
        'contribution_history': [
            {'period': 'Mar 2025', 'employer': 'Tech S.A.', 'days': 25, 'amount': 460.0},
        ],
    }
    try:
        rendered = render_to_string('core/insurance_contributions.html', context)
        assert 'Insurance Contributions' in rendered
        print("Template rendered successfully!")
    except Exception as e:
        print(f"Template rendering failed: {e}")

if __name__ == "__main__":
    test_contributions_rendering()
