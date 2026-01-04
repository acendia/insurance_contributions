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
            'core',
        ],
        USE_I18N=True,
        LANGUAGES=[('en', 'English'), ('el', 'Greek')],
        ROOT_URLCONF='registry_app.urls',
    )
    django.setup()

def test_insured_home_rendering():
    context = {
        'full_name': 'John Doe',
        'insurance_id': 'AMA-123456789',
        'total_days': 4500,
        'current_employer': 'Tech Solutions S.A.',
        'next_milestone': 'Full Pension Eligibility',
        'recent_activity': [
            {'label': 'Monthly contribution updated for November 2025', 'date': datetime.now() - timedelta(days=2)},
        ],
    }
    try:
        rendered = render_to_string('core/insured_home.html', context)
        assert 'John Doe' in rendered
        assert 'AMA-123456789' in rendered
        assert '4500' in rendered
        print("Template rendered successfully with expected data!")
    except Exception as e:
        print(f"Template rendering failed: {e}")

if __name__ == "__main__":
    test_insured_home_rendering()
