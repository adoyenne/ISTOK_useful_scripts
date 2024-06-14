from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Appointment
from users.models import User
from datetime import date, timedelta

@login_required
def calendar_view(request):
    """
    Представление для записи на встречу с сотрудником
    """
    work_time_list = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"]
    specialists = User.objects.filter(groups__name__in=['Consultants', 'Designers', 'Measurers'])
    appointments = Appointment.objects.all()
    query = request.GET.get('q')
    specialist_type = request.GET.get('type')

    if query:
        specialists = specialists.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(patronymic__icontains=query))
    if specialist_type:
        specialists = specialists.filter(groups__name__in=[specialist_type])

    if request.method == "POST":
        specialist_id = request.POST.get('specialist')
        appointment_date = request.POST.get('date')
        appointment_time = request.POST.get('time')
        specialist = get_object_or_404(User, id=specialist_id)
        if not Appointment.objects.filter(staff_user=specialist, date=appointment_date, time=appointment_time).exists():
            Appointment.objects.create(client_user=request.user, staff_user=specialist, date=appointment_date, time=appointment_time, is_booked=True)
        return redirect('calendar_view')

    context = {
        'work_time_list': work_time_list,
        'specialists': specialists,
        'appointments': appointments,
        'days': [date.today() + timedelta(days=i) for i in range(30)],  # Next 30 days
    }
    return render(request, 'calendar.html', context=context)