from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.conf import settings
from datetime import datetime, timedelta
from functools import wraps
import os
from .models import (
    Client, Party, PartyRole, PartyRoleType, PartyIdentifier, PartyIdentifierType, 
    Organization, Address, Person, Account, AccountType, AccountBalance, 
    AccountTransaction, TransactionBalance, TransactionObligation, 
    ObligationBalance, InsuranceContribution, InsuranceContributionBalance, 
    PartyRelationship, PartyRelationshipType
)


def get_user_role_code(user):
    """Helper to get the role code for a user."""
    try:
        client = Client.objects.get(user=user)
        party = Party.objects.filter(client_id=client).first()
        if party:
            party_role = PartyRole.objects.filter(party_id=party, status=1).first()
            if party_role:
                role_type = PartyRoleType.objects.filter(role_type_id=party_role.role_type_id).first()
                return role_type.role_type_code if role_type else None
    except (Client.DoesNotExist, Exception):
        pass
    return None


def role_required(allowed_roles):
    """Decorator to restrict view access based on user's party role."""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            role_code = get_user_role_code(request.user)
            if role_code in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                # Redirect to appropriate home or return 403
                if role_code == 'INS':
                    return redirect('insured_home')
                elif role_code == 'EMP':
                    return redirect('employer_home')
                else:
                    return HttpResponseForbidden("Access Denied: You do not have permission to view this page.")
        return wrapper
    return decorator


@login_required
def login_redirect_view(request):
    """Redirect user to appropriate home based on their role."""
    role_code = get_user_role_code(request.user)
    if role_code == 'EMP':
        return redirect('employer_home')
    elif role_code == 'INS':
        return redirect('insured_home')
    else:
        return redirect('home')


def home(request):
    return render(request, "core/home.html")

# @login_required
def client_home(request):
    
    # user = get_object_or_404(UserProfile, user=request.user)
    # party = Party.objects.get(client_id=user.client)
    
    # Dashboard context data
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

@role_required(['EMP'])
def employer_home(request):
    # Retrieve Employer details from DB
    try:
        # Fetching the default employer record seeded in the database
        employer_org = Organization.objects.get(name='METLEN ENERGY & METALS S.A.')
        party = employer_org.party_id
        
        # Identifiers
        tax_id = "N/A"
        ame = "N/A"
        try:
            afm_type = PartyIdentifierType.objects.filter(identifier_type_code='AFM').first()
            if afm_type:
                afm_ident = PartyIdentifier.objects.filter(party_id=party, identifier_type_id=afm_type.identifier_type_id).last()
                tax_id = afm_ident.identifier_value if afm_ident else "N/A"
        except: pass
        
        try:
            ame_type = PartyIdentifierType.objects.filter(identifier_type_code='AME').first()
            if ame_type:
                ame_ident = PartyIdentifier.objects.filter(party_id=party, identifier_type_id=ame_type.identifier_type_id).first()
                ame = ame_ident.identifier_value if ame_ident else "N/A"
        except: pass
        
        # Address
        full_address = "N/A"
        try:
            addr = Address.objects.filter(party_id=party).first()
            if addr:
                full_address = f"{addr.address_street} {addr.address_number}, {addr.city}, {addr.postal_code}"
        except: pass
        
        # Get Accounts and Balances for the employer role
        debts = {'current': 0.00, 'overdue_keao_settled': 0.00, 'overdue_keao_unsettled': 0.00}
        try:
            role_employer_obj = PartyRole.objects.get(party_id=party, role_type_id=2)
            # Account 1: Current
            acc_current = Account.objects.filter(party_role_id=role_employer_obj, account_id=1).first()
            if acc_current: debts['current'] = float(acc_current.account_balance)
            
            # Account 2: Settled KEAO
            acc_settled = Account.objects.filter(party_role_id=role_employer_obj, account_id=2).first()
            if acc_settled: debts['overdue_keao_settled'] = float(acc_settled.account_balance)
            
            # Account 3: Unsettled KEAO
            acc_unsettled = Account.objects.filter(party_role_id=role_employer_obj, account_id=3).first()
            if acc_unsettled: debts['overdue_keao_unsettled'] = float(acc_unsettled.account_balance)
            
            unpaid_contributions_total = debts['current']
        except (PartyRole.DoesNotExist):
            unpaid_contributions_total = 0.00
            
        company_name = employer_org.name
    except Organization.DoesNotExist:
        company_name = "Employer Not Found"
        tax_id = "N/A"
        ame = "N/A"
        full_address = "N/A"
        unpaid_contributions_total = 0.00
        debts = {'current': 0.00, 'overdue_keao_settled': 0.00, 'overdue_keao_unsettled': 0.00}

    context = {
        'company_name': company_name,
        'tax_id': tax_id,
        'ame': ame,
        'address': full_address,
        'current_period': datetime.now().strftime('%B %Y'),
        'pending_apd_count': 2,
        'next_apd_deadline': datetime.now() + timedelta(days=15),
        'unpaid_contributions_total': unpaid_contributions_total,
        'last_payroll_run': {
            'period': datetime.now().strftime('%m/%Y'),
            'run_date': datetime.now() - timedelta(days=5),
            'employee_count': 25,
        },
        'recent_actions': [
            {'label': 'Payroll run completed for November 2025', 'date': datetime.now() - timedelta(days=5)},
            {'label': 'APD submitted for October 2025', 'date': datetime.now() - timedelta(days=12)},
            {'label': 'New employee added: Ioannis Papadopoulos', 'date': datetime.now() - timedelta(days=18)},
        ],
        'debts': debts,
    }
    
    return render(request, "core/employer_home.html", context)


@role_required(['INS'])
def profile_update(request):
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        messages.error(request, "Client record not found.")
        return redirect('insured_home')

    if request.method == 'POST':
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')

        if phone and email and address:
            client.phone = phone
            client.email = email
            client.address = address
            client.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile_update')
        else:
            messages.error(request, "All fields are required.")

    context = {
        'client': client
    }
    return render(request, "core/profile_update.html", context)


@role_required(['INS'])
def insured_home(request):
    # Retrieve data from database
    full_name = "User Not Found"
    insurance_id = "N/A"
    address_display = "N/A"
    total_days = 0
    current_employer = "Not Available"
    next_milestone = "N/A"
    recent_activity = []

    # Try to get the client and party associated with the user
    # In a real scenario, we'd use request.user. In this seed case, we'll look for 'seed_user' 
    # if the user is not authenticated or as a fallback for demonstration.
    try:
        if request.user.is_authenticated:
            user = request.user
        else:
            from django.contrib.auth.models import User
            user = User.objects.get(username='seed_user')

        client = Client.objects.get(user=user)
        
        # Find the party associated with this client that has the 'INS' role
        ins_role_type = PartyRoleType.objects.get(role_type_code='INS')
        party_role = PartyRole.objects.get(role_type_id=ins_role_type.role_type_id, party_id__client_id=client)
        party = party_role.party_id
        full_name = party.display_name
        
        # Get Identifiers
        amka = "N/A"
        adt = "N/A"
        try:
            ama_type = PartyIdentifierType.objects.filter(identifier_type_code='AMA').first()
            if ama_type:
                ama_ident = PartyIdentifier.objects.filter(party_id=party, identifier_type_id=ama_type.identifier_type_id).first()
                insurance_id = ama_ident.identifier_value if ama_ident else "N/A"
            
            amka_type = PartyIdentifierType.objects.filter(identifier_type_code='AMKA').first()
            if amka_type:
                amka_ident = PartyIdentifier.objects.filter(party_id=party, identifier_type_id=amka_type.identifier_type_id).first()
                amka = amka_ident.identifier_value if amka_ident else "N/A"

            adt_type = PartyIdentifierType.objects.filter(identifier_type_code='ADT').first()
            if adt_type:
                adt_ident = PartyIdentifier.objects.filter(party_id=party, identifier_type_id=adt_type.identifier_type_id).first()
                adt = adt_ident.identifier_value if adt_ident else "N/A"
        except Exception as id_e:
            print(f"Error fetching insured identifiers: {id_e}")

        # Get Address
        try:
            addr = Address.objects.filter(party_id=party).first()
            if addr:
                address_display = f"{addr.address_street} {addr.address_number}, {addr.city}"
            else:
                address_display = "N/A"
        except:
            address_display = "N/A"

        # Additional fields can be populated from contribution records
        # Fetch current employer through PartyRelationship
        try:
            # Look for active employment relationship (relation_to is the insured)
            emp_relationship = PartyRelationship.objects.filter(
                relation_to=party_role,
                relationship_type_id=1, # EMPLOYMENT type seeded earlier
                status=1
            ).first()
            
            if emp_relationship:
                employer_party = emp_relationship.relation_from.party_id
                org = Organization.objects.filter(party_id=employer_party).first()
                current_employer = org.name if org else "Unknown Employer"
            else:
                current_employer = "No Active Employer"
        except Exception as e:
            current_employer = "Not Available"

        next_milestone = "Full Pension Eligibility"
        recent_activity = [
            {'label': 'Monthly contribution updated for November 2025', 'date': datetime.now() - timedelta(days=2)},
            {'label': 'Insurance record downloaded', 'date': datetime.now() - timedelta(days=10)},
            {'label': 'Profile information updated', 'date': datetime.now() - timedelta(days=25)},
        ]
    except (Client.DoesNotExist, Party.DoesNotExist, Exception) as e:
        print(f"Error fetching insured data: {e}")

    context = {
        'full_name': full_name,
        'insurance_id': insurance_id,
        'amka': amka,
        'adt': adt,
        'address': address_display,
        'total_days': total_days,
        'current_employer': current_employer,
        'next_milestone': next_milestone,
        'recent_activity': recent_activity,
    }
    
    return render(request, "core/insured_home.html", context)


@role_required(['INS'])
def insurance_contributions(request):
    import json # Moved import here as it's only used in this function

    labels = []
    historical_values = []
    predictive_values = []
    ytd_total = 0.0
    projected_total = 0.0
    history = []
    avg_contribution = 0.0 # Initialize for fallback context

    try:
        # 1. Identify User and Party
        if request.user.is_authenticated:
            user = request.user
        else:
            from django.contrib.auth.models import User
            user = User.objects.get(username='insured_user') # Fallback for demonstration

        client = Client.objects.get(user=user)
        ins_role_type = PartyRoleType.objects.get(role_type_code='INS')
        party_role = PartyRole.objects.get(role_type_id=ins_role_type.role_type_id, party_id__client_id=client)
        party = party_role.party_id
        
        # 2. Fetch Contributions from DB
        contributions = InsuranceContribution.objects.filter(party_id=party).order_by('start_date')
        
        if not contributions.exists():
            raise Exception("No contributions found for user")

        historical_contributions = []
        historical_gross = []
        
        # 3. Process Data for Chart
        # Filter by year if provided
        selected_year = request.GET.get('year')
        current_year = datetime.now().year
        
        # Get distinct years from contributions for the filter dropdown
        available_years = contributions.dates('start_date', 'year').distinct().order_by('-start_date')
        years_list = [d.year for d in available_years]
        if current_year not in years_list and not contributions.exists():
             years_list = [current_year] # Default if no data
        
        if selected_year and selected_year != 'all':
            try:
                selected_year_int = int(selected_year)
                contributions = contributions.filter(start_date__year=selected_year_int)
            except ValueError:
                selected_year = current_year
                contributions = contributions.filter(start_date__year=selected_year)
        elif selected_year == 'all':
            # No filtering by year
            pass
        else:
             # Default to current year
             selected_year = str(current_year)
             contributions = contributions.filter(start_date__year=current_year)
        
        # 3. Chart Data (Chronological)
        # Re-sort for chart after filtering
        chart_contributions = contributions.order_by('start_date')
        
        for ic in chart_contributions:
            labels.append(ic.start_date.strftime('%b %Y'))
            historical_contributions.append(float(ic.total_contribution))
            historical_gross.append(float(ic.gross_earnings))
        
        # 4. Summary Stats
        # If 'all' is selected, these are "Total to Date" rather than "Year to Date"
        ytd_total_contributions = sum(historical_contributions)
        ytd_total_gross = sum(historical_gross)

        # 5. History Table Data (Reverse chronological)
        for ic in contributions.order_by('-start_date'):
            # Find employer name through relationship
            emp_name = "N/A"
            emp_ame = "N/A"
            try:
                # Lookup Employer Party (employer_id in IC is the party_id)
                employer_party = Party.objects.filter(party_id=ic.employer_id).first()
                if employer_party:
                    # Find name
                    org = Organization.objects.filter(party_id=employer_party).first()
                    emp_name = org.name if org else "Unknown Employer"
                    
                    # Find AME (type 5)
                    ame_type = PartyIdentifierType.objects.filter(identifier_type_code='AME').first()
                    if ame_type:
                        ame_id = PartyIdentifier.objects.filter(
                            party_id=employer_party, 
                            identifier_type_id=ame_type.identifier_type_id
                        ).first()
                        if ame_id:
                            emp_ame = ame_id.identifier_value
            except Exception as lookup_e:
                print(f"Error looking up employer details: {lookup_e}")
                pass

            history.append({
                'from': ic.start_date.strftime('%d/%m/%Y'),
                'to': ic.end_date.strftime('%d/%m/%Y'),
                'year': ic.start_date.year,
                'month': ic.start_date.month,
                'days': ic.insurance_days,
                'earnings_type': f"{ic.earning_type_id:02d}",
                'coverage_package': str(ic.coverage_package_id),
                'gross_earnings': float(ic.gross_earnings),
                'total_contributions': float(ic.total_contribution),
                'employer_name': emp_name,
                'employer_ame': emp_ame
            })

    except Exception as e:
        print(f"Error in insurance_contributions view: {e}")
        # Fallback to demonstration data if no database records are available
        # TODO: Integrate with real-time analytics once available
        ytd_total_contributions = 0
        ytd_total_gross = 0
        selected_year = datetime.now().year
        years_list = [selected_year]

    context = {
        'summary_stats': {
            'ytd_total': ytd_total_contributions,
            'ytd_gross': ytd_total_gross,
        },
        'chart_data': {
            'labels': json.dumps(labels),
            'contributions': json.dumps(historical_contributions),
            'gross': json.dumps(historical_gross),
        },
        'contribution_history': history,
        'selected_year': selected_year,
        'available_years': sorted(list(set(years_list)), reverse=True),
    }
    
    return render(request, "core/insurance_contributions.html", context)

@role_required(['INS'])
def print_insurance_history(request):
    try:
        # Get user
        user = request.user
        # Get insured client
        client = Client.objects.get(user=user)
        # Get insured party
        party = Party.objects.get(client_id=client, party_type='PERSON')
        
        # Always fetch all contributions for the print view
        contributions = InsuranceContribution.objects.filter(party_id=party)
        
        # Provide history list
        history = []
        for ic in contributions.order_by('-start_date'):
            # Fetch Employer details (simplified for print view consistency)
             # Find employer name through relationship
            emp_name = "N/A"
            emp_ame = "N/A"
            try:
                employer_party = Party.objects.filter(party_id=ic.employer_id).first()
                if employer_party:
                    org = Organization.objects.filter(party_id=employer_party).first()
                    emp_name = org.name if org else "Unknown Employer"
                    
                    ame_type = PartyIdentifierType.objects.filter(identifier_type_code='AME').first()
                    if ame_type:
                        ame_id = PartyIdentifier.objects.filter(party_id=employer_party, identifier_type_id=ame_type.identifier_type_id).first()
                        if ame_id:
                            emp_ame = ame_id.identifier_value
            except: pass

            history.append({
                'from': ic.start_date.strftime('%d/%m/%Y'),
                'to': ic.end_date.strftime('%d/%m/%Y'),
                'year': ic.start_date.year,
                'month': ic.start_date.month,
                'days': ic.insurance_days,
                'earnings_type': f"{ic.earning_type_id:02d}",
                'coverage_package': str(ic.coverage_package_id),
                'gross_earnings': float(ic.gross_earnings),
                'total_contributions': float(ic.total_contribution),
                'employer_name': emp_name,
                'employer_ame': emp_ame
            })
            
        context = {
            'contribution_history': history,
            'selected_year': "All Time",
            'insured_name': party.display_name,
            'insured_id': party.distinct_value, # AMKA
            'print_date': datetime.now().strftime('%d/%m/%Y')
        }
        return render(request, "core/print_contributions.html", context)

    except Exception as e:
        print(f"Error in print_history: {e}")
        return render(request, "core/print_contributions.html", {'error': 'Could not generate report'})

@role_required(['EMP'])
def apd_submission(request):
    # Context data for APD submission page
    now = datetime.now()
    submission_history = [
        {
            'period': (now - timedelta(days=30)).strftime('%m/%Y'),
            'submission_date': (now - timedelta(days=5)).strftime('%d/%m/%Y %H:%M'),
            'receipt_number': 'APD-99887766',
            'status': 'Accepted',
            'employee_count': 25,
            'total_contributions': 1250.50,
        },
        {
            'period': (now - timedelta(days=60)).strftime('%m/%Y'),
            'submission_date': (now - timedelta(days=35)).strftime('%d/%m/%Y %H:%M'),
            'receipt_number': 'APD-99887700',
            'status': 'Accepted',
            'employee_count': 24,
            'total_contributions': 1200.00,
        },
        {
            'period': (now - timedelta(days=90)).strftime('%m/%Y'),
            'submission_date': (now - timedelta(days=65)).strftime('%d/%m/%Y %H:%M'),
            'receipt_number': 'APD-99887655',
            'status': 'Accepted',
            'employee_count': 24,
            'total_contributions': 1180.20,
        },
    ]
    
    # Fetch Employer details from DB
    try:
        employer_org = Organization.objects.get(name='METLEN ENERGY & METALS S.A.')
        party = employer_org.party_id
        
        tax_id = "N/A"
        ame = "N/A"
        try:
            afm_type = PartyIdentifierType.objects.get(identifier_type_code='AFM')
            # Use filter().first() to avoid MultipleObjectsReturned
            tax_id_obj = PartyIdentifier.objects.filter(party_id=party, identifier_type_id=afm_type.identifier_type_id).first()
            if tax_id_obj:
                tax_id = tax_id_obj.identifier_value
        except: pass
        
        try:
            ame_type = PartyIdentifierType.objects.get(identifier_type_code='AME')
            # Use filter().first() to avoid MultipleObjectsReturned
            ame_obj = PartyIdentifier.objects.filter(party_id=party, identifier_type_id=ame_type.identifier_type_id).first()
            if ame_obj:
                ame = ame_obj.identifier_value
        except: pass
        
        full_address = "N/A"
        try:
            addr = Address.objects.filter(party_id=party).first()
            if addr:
                full_address = f"{addr.address_street} {addr.address_number}, {addr.city}, {addr.postal_code}"
        except: pass
        
        company_name = employer_org.name
    except:
        company_name = "METLEN ENERGY & METALS S.A."
        full_address = "8 Artemidos Str., Maroussi, Athens, 15125"
        tax_id = "998877665"
        ame = "1234567890"

    context = {
        'company_name': company_name,
        'company_address': full_address,
        'tax_id': tax_id,
        'ame': ame,
        'current_period': now.strftime('%B %Y'),
        'submission_history': submission_history,
    }
    return render(request, "core/apd_submission.html", context)

def code_info(request):
    info_type = request.GET.get('type', 'kad')
    kad_filter = request.GET.get('kad', '')
    eid_filter = request.GET.get('eid', '')
    kpk_filter = request.GET.get('kpk', '')
    
    file_map = {
        'kad': 'dn_kad.txt',
        'eid': 'dn_eid.txt',
        'kpk': 'dn_kpk.txt'
    }
    
    filename = file_map.get(info_type, 'dn_kad.txt')
    filepath = os.path.join(settings.BASE_DIR, 'core', 'static', 'core', 'texts', filename)
    
    codes = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.split('|')
                if len(parts) >= 2:
                    codes.append({
                        'code': parts[0].strip(),
                        'description': parts[1].strip(),
                        'is_appropriate': True # Default
                    })
    except Exception as e:
        print(f"Error reading {filename}: {e}")

    # Triple mapping for green/red logic
    mapping_path = os.path.join(settings.BASE_DIR, 'core', 'static', 'core', 'texts', 'dn_kadeidkpk.txt')
    appropriate_codes = set()
    has_filter = False

    try:
        with open(mapping_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.split('|')
                if len(parts) >= 3:
                    m_kad = parts[0].strip()
                    m_eid = parts[1].strip()
                    m_kpk = parts[2].strip()
                    
                    match = True
                    if kad_filter and m_kad != kad_filter: match = False
                    if eid_filter and m_eid != eid_filter: match = False
                    if kpk_filter and m_kpk != kpk_filter: match = False
                    
                    if match:
                        if info_type == 'kad': appropriate_codes.add(m_kad)
                        elif info_type == 'eid': appropriate_codes.add(m_eid)
                        elif info_type == 'kpk': appropriate_codes.add(m_kpk)
                        
        if kad_filter or eid_filter or kpk_filter:
            has_filter = True
    except Exception as e:
        print(f"Error reading mapping: {e}")

    if has_filter:
        for c in codes:
            c['is_appropriate'] = c['code'] in appropriate_codes

    context = {
        'info_type': info_type,
        'codes': codes,
        'has_filter': has_filter,
        'kad_filter': kad_filter,
        'eid_filter': eid_filter,
        'kpk_filter': kpk_filter,
    }
    return render(request, "core/code_info.html", context)


@role_required(['EMP'])
def current_obligations(request):
    # Retrieve organization details for the context
    try:
        employer_org = Organization.objects.get(name='METLEN ENERGY & METALS S.A.')
        party = employer_org.party_id
        
        # Get Account for the employer role (Current Contributions account id=1)
        role_employer = PartyRole.objects.get(party_id=party, role_type_id=2)
        account = Account.objects.filter(party_role_id=role_employer, account_id=1).first()
        
        if not account:
            raise Account.DoesNotExist("Current Contributions account not found")
        
        # Fetch obligations through transactions
        transactions = AccountTransaction.objects.filter(account_id=account).order_by('-transaction_date')
        
        obligations_list = []
        total_debt = 0
        
        for tx in transactions:
            # For each transaction, find associated obligations that have a non-zero balance
            tx_obligations = TransactionObligation.objects.filter(
                transaction_id=tx,
                obligationbalance__balance__gt=0
            ).select_related('transaction_id')
            
            for obl in tx_obligations:
                # Use actual balance from ObligationBalance
                try:
                    obl_bal = ObligationBalance.objects.get(obligation_id=obl)
                    amount = obl_bal.balance
                    
                    total_debt += amount
                    
                    obligations_list.append({
                        'period': f"{obl.month:02d}/{obl.year}",
                        'description': obl.obligation_description,
                        'type': obl.obligation_type,
                        'amount': amount,
                        'rf_code': obl.rf_code,
                        'due_date': datetime(obl.year, obl.month, 28) + timedelta(days=32)
                    })
                except ObligationBalance.DoesNotExist:
                    continue
        
        company_name = employer_org.name
    except (Organization.DoesNotExist, PartyRole.DoesNotExist, Account.DoesNotExist) as e:
        company_name = "METLEN ENERGY & METALS S.A."
        obligations_list = [
            {'period': '11/2025', 'description': 'Social Security Contribution - Nov 2025', 'type': 'CONTRIBUTION', 'amount': 452.40, 'due_date': datetime(2025, 12, 31)},
        ]
        total_debt = 452.40

    context = {
        'company_name': company_name,
        'obligations': obligations_list,
        'total_debt': total_debt,
        'next_due_date': obligations_list[0]['due_date'] if obligations_list else None,
        'current_period': datetime.now().strftime('%B %Y'),
    }
    return render(request, "core/current_obligations.html", context)


@role_required(['EMP'])
def unsettled_overdue(request):
    try:
        employer_org = Organization.objects.get(name='METLEN ENERGY & METALS S.A.')
        party = employer_org.party_id
        role_employer = PartyRole.objects.get(party_id=party, role_type_id=2)
        
        # Account 3: Unsettled Overdue (KEAO)
        account = Account.objects.filter(party_role_id=role_employer, account_id=3).first()
        
        if not account:
            raise Account.DoesNotExist("Unsettled Overdue account not found")

        transactions = AccountTransaction.objects.filter(account_id=account).order_by('-transaction_date')
        debts_list = []
        total_unsettled = 0
        
        for tx in transactions:
            tx_obligations = TransactionObligation.objects.filter(transaction_id=tx).select_related('transaction_id')
            for obl in tx_obligations:
                try:
                    obl_bal = ObligationBalance.objects.get(obligation_id=obl)
                    amount = obl_bal.balance
                    if amount > 0:
                        total_unsettled += amount
                        debts_list.append({
                            'period': f"{obl.month:02d}/{obl.year}",
                            'description': obl.obligation_description,
                            'type': obl.obligation_type,
                            'amount': amount,
                            'reference': obl.rf_code or 'N/A'
                        })
                except ObligationBalance.DoesNotExist:
                    continue
                    
        company_name = employer_org.name
    except Exception as e:
        company_name = "METLEN ENERGY & METALS S.A."
        debts_list = []
        total_unsettled = 0.00

    context = {
        'company_name': company_name,
        'debts': debts_list,
        'total_unsettled': total_unsettled,
        'current_period': datetime.now().strftime('%B %Y'),
    }
    return render(request, "core/unsettled_overdue.html", context)


@role_required(['EMP'])
def settled_overdue(request):
    debts_list = []
    total_settled = 0
    try:
        # Get current employer (seeded default)
        employer_org = Organization.objects.filter(name='METLEN ENERGY & METALS S.A.').first()
        employer_party = employer_org.party_id
        role_employer = PartyRole.objects.get(party_id=employer_party, role_type_id=2)
        
        # Account 2: Settled Overdue (KEAO)
        account = Account.objects.filter(party_role_id=role_employer, account_id=2).first()
        
        if account:
            transactions = AccountTransaction.objects.filter(account_id=account).order_by('-transaction_date')
            
            for tx in transactions:
                tx_obligations = TransactionObligation.objects.filter(transaction_id=tx)
                for obl in tx_obligations:
                    try:
                        obl_bal = ObligationBalance.objects.get(obligation_id=obl)
                        amount = obl_bal.balance
                        if amount > 0:
                            total_settled += amount
                            debts_list.append({
                                'period': f"{obl.month:02d}/{obl.year}",
                                'description': obl.obligation_description,
                                'type': obl.obligation_type,
                                'amount': amount,
                                'rf_code': obl.rf_code or 'N/A'
                            })
                    except ObligationBalance.DoesNotExist:
                        pass

    except Exception as e:
        print(f"Error in settled_overdue view: {e}")

    context = {
        'total_settled': total_settled,
        'debts': debts_list,
        'company_name': employer_org.name if 'employer_org' in locals() and employer_org else "Employer"
    }
    return render(request, "core/settled_overdue.html", context)


@role_required(['EMP'])
def employees_list(request):
    employees = []
    try:
        # Get current employer (seeded default)
        employer_org = Organization.objects.filter(name='METLEN ENERGY & METALS S.A.').first()
        if not employer_org:
            return render(request, "core/employees_list.html", {'employees': [], 'error': 'Employer not found'})
            
        employer_party = employer_org.party_id
        
        # Employer role_type_id=2
        employer_role = PartyRole.objects.filter(party_id=employer_party, role_type_id=2).first()
        if not employer_role:
             return render(request, "core/employees_list.html", {'employees': [], 'error': 'Employer role not found'})

        # relationship_type_id=1 is EMPLOYMENT
        # relation_from is employer, relation_to is insured (employee)
        relationships = PartyRelationship.objects.filter(
            relation_from=employer_role,
            relationship_type_id=1,
            status=1
        ).select_related('relation_to__party_id')

        for rel in relationships:
            employee_party = rel.relation_to.party_id
            
            # Name from Person
            person = Person.objects.filter(party_id=employee_party).first()
            if person:
                name = f"{person.first_name} {person.last_name}"
            else:
                name = employee_party.display_name
            
            # AMKA from PartyIdentifier (type 2)
            amka = "N/A"
            amka_ident = PartyIdentifier.objects.filter(party_id=employee_party, identifier_type_id=2).first()
            if amka_ident:
                amka = amka_ident.identifier_value

            employees.append({
                'name': name,
                'amka': amka,
                'start_date': rel.active_date_from,
                'status': 'Active' if rel.status == 1 else 'Inactive',
                'id': employee_party.party_id
            })

    except Exception as e:
        print(f"Error in employees_list view: {e}")

    context = {
        'employees': employees,
        'company_name': employer_org.name if 'employer_org' in locals() and employer_org else "Employer"
    }
    return render(request, "core/employees_list.html", context)


from django.http import JsonResponse

@role_required(['EMP'])
def get_last_contribution(request):
    ama = request.GET.get('ama')
    if not ama:
        return JsonResponse({'error': 'AMA is required'}, status=400)

    try:
        # 1. Find the Party Identifier Type for AMA
        ama_type = PartyIdentifierType.objects.filter(identifier_type_code='AMA').first()
        if not ama_type:
            return JsonResponse({'error': 'AMA type not found'}, status=500)

        # 2. Find the Party Identifier with this AMA
        identifier = PartyIdentifier.objects.filter(
            identifier_type_id=ama_type.identifier_type_id,
            identifier_value=ama
        ).first()

        if not identifier:
            return JsonResponse({'error': 'Employee not found'}, status=404)

        party = identifier.party_id

        # 3. Find the most recent Insurance Contribution for this Party
        # We order by end_date descending to get the latest coverage
        last_contribution = InsuranceContribution.objects.filter(party_id=party).order_by('-end_date').first()

        if not last_contribution:
            return JsonResponse({'error': 'No previous contributions found for this employee'}, status=404)

        data = {
            'coverage_package_id': last_contribution.coverage_package_id,
            'earning_type_id': last_contribution.earning_type_id,
            'insurance_days': last_contribution.insurance_days,
            'gross_earnings': str(last_contribution.gross_earnings), # Decimal to string
            'total_contribution': str(last_contribution.total_contribution),
        }
        
        return JsonResponse(data)

    except Exception as e:
        print(f"Error in get_last_contribution: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)


@role_required(['EMP'])
def payments_screen(request):
    """
    View for the Payment Screen dashboard.
    """
    # Mock data for current obligations
    debts = {
        'current': 1250.45,
        'overdue_keao_settled': 450.00,
        'overdue_keao_unsettled': 153.50,
        'total': 1853.95
    }

    # Mock data for transaction history
    payment_history = [
        {
            'date': '2023-12-01',
            'amount': 300.00,
            'reference': 'RF912023120000001',
            'status': 'Completed',
            'type': 'Current Obligations'
        },
        {
            'date': '2023-11-15',
            'amount': 75.13,
            'reference': 'RF912023119999991',
            'status': 'Completed',
            'type': 'Settled Overdue'
        },
        {
            'date': '2023-10-30',
            'amount': 500.00,
            'reference': 'RF912023100000002',
            'status': 'Completed',
            'type': 'Current Obligations'
        },
    ]

    context = {
        'debts': debts,
        'payment_history': payment_history,
        'company_name': "METLEN ENERGY & METALS S.A."  # Using primary organization for development
    }
    return render(request, "core/payments.html", context)
