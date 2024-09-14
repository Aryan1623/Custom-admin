# admindash/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from chartapp.models import UserAttendance
from django.db.models import Count, Q
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@superuser_required
@login_required
def dash(request):
    # Aggregate attendance data by user
    attendance_data = UserAttendance.objects.values('user__username').annotate(
        total_days=Count('status'),
        days_present=Count('status', filter=Q(status='present')),
        days_absent=Count('status', filter=Q(status='absent'))
    )

    # Calculate the attendance percentage for each user
    user_attendance = []
    for record in attendance_data:
        total_days = record['total_days']
        days_present = record['days_present']
        attendance_percent = (days_present / total_days) * 100 if total_days > 0 else 0
        user_attendance.append({
            'user': record['user__username'],
            'attendance_percent': round(attendance_percent, 2)
        })

    context = {
        'user_attendance': user_attendance
    }

    return render(request, 'dash.html', context)

def user_list_view(request):
    # Fetch all users
    users = User.objects.all()
    
    # Pass the user data to the template
    return render(request, 'user.html', {'users': users})





def attendance(request, username):
    user = get_object_or_404(User, username=username)
    # Calculate the attendance percentage for this user
    attendance_records = UserAttendance.objects.filter(user=user)
    total_days = attendance_records.count()
    present_days = attendance_records.filter(status='present').count()
    attendance_percent = (present_days / total_days * 100) if total_days > 0 else 0
    
    context = {
        'user_attendance': attendance_records,
        'attendance_percent': attendance_percent,
    }
    return render(request, 'attendance.html', context)