from django.shortcuts import render, redirect
from .models import Product, UserAttendance
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.db import models

from django.contrib.auth import logout

# Create your views here.
def index(request):
    products = Product.objects.all()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProductForm()        

    context = {
        "products": products,
        "form": form
    }

    return render(request, 'chartapp/index.html', context)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email format!')
            return render(request, 'chartapp/register.html')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'chartapp/register.html')

        # Create user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'User registered successfully!')
            return redirect('login')  # Redirect to login page
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return render(request, 'chartapp/register.html')
    else:
        return render(request, 'chartapp/register.html')
    

@login_required
def attendance_list(request):
    # Fetch attendance records for the logged-in user
    user_attendance_records = UserAttendance.objects.filter(user=request.user).order_by('-date')
    
    # Implement pagination: 5 records per page
    paginator = Paginator(user_attendance_records, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    present_days = user_attendance_records.filter(status='present').count()
    absent_days = user_attendance_records.filter(status='absent').count()
    
    monthly_data = (
        user_attendance_records.filter(date__year=now().year)  # Current year
        .values('date__month')  # Group by month
        .annotate(days_present=Count('id', filter=models.Q(status='present')))  # Count days present
        .order_by('date__month')
    )
    
    labels = []
    data = []
    for entry in monthly_data:
        month_name = entry['date__month']  # Month number (1-12)
        labels.append(month_name)
        data.append(entry['days_present'])

    monthly_attendance_data = {
        'labels': labels,
        'data': data
    }
    
    context = {
        'user': request.user,
        'page_obj': page_obj,  # Pass the paginated records
        'present_days': present_days,
        'absent_days': absent_days,
        'monthly_attendance_data': monthly_attendance_data,
    }
    
    return render(request, 'chartapp/attendence_list.html', context)

@login_required
def user_attendance_view(request):
    # Fetch all attendance records
    attendance_records = UserAttendance.objects.all()
    
    # Calculate attendance percentage for each user
    user_attendance_data = []
    for record in attendance_records:
        total_days = record.present + record.absent
        attendance_percentage = (record.present / total_days) * 100 if total_days > 0 else 0
        user_attendance_data.append({
            'user': record.user,
            'attendance_percentage': attendance_percentage
        })
    
    # Render the data in a template
    return render(request, 'admin/user_attendance.html', {'user_attendance_data': user_attendance_data})


def custom_logout_view(request):
    logout(request)
    return redirect('index')  # Redirect to the home page after logging out

def custom_login_view(request):
    
    return redirect('index')