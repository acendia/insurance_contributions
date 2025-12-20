from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from datetime import datetime, timedelta
# from .models import UserProfile, Party


def home(request):
    return render(request, "core/home.html")

# @login_required
def client_home(request):
    
    # user = get_object_or_404(UserProfile, user=request.user)
    # party = Party.objects.get(client_id=user.client)
    
    # Sample data for the dashboard
    context = {
        'company_name': 'Company Name',
        'current_period': datetime.now().strftime('%B %Y'),
        'pending_apd_count': 2,
        'next_apd_deadline': datetime.now() + timedelta(days=15),
        'unpaid_contributions_total': 1250.50,
        'last_payroll_run': {
            'period': datetime.now().strftime('%m/%Y'),
            'run_date': datetime.now() - timedelta(days=5),
            'employee_count': 25,
        },
        'recent_actions': [
            {'label': 'Payroll run completed for November 2025', 'date': datetime.now() - timedelta(days=5)},
            {'label': 'APD submitted for October 2025', 'date': datetime.now() - timedelta(days=12)},
            {'label': 'New employee added: John Doe', 'date': datetime.now() - timedelta(days=18)},
        ],
    }
    
    return render(request, "core/client_home.html", context)
