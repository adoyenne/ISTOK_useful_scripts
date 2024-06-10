from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Specialist, Appointment
from datetime import date, timedelta

@login_required
def calendar_view(request):
    specialists = Specialist.objects.all()
    appointments = Appointment.objects.all()  # Get all appointments
    query = request.GET.get('q')
    specialist_type = request.GET.get('type')

    if query:
        specialists = specialists.filter(last_name__icontains=query)
    if specialist_type:
        specialists = specialists.filter(specialist_type=specialist_type)

    if request.method == "POST":
        specialist_id = request.POST.get('specialist')
        appointment_date = request.POST.get('date')
        appointment_time = request.POST.get('time')
        specialist = Specialist.objects.get(id=specialist_id)
        # Check if the slot is already booked
        if not Appointment.objects.filter(specialist=specialist, date=appointment_date, time=appointment_time).exists():
            Appointment.objects.create(user=request.user, specialist=specialist, date=appointment_date, time=appointment_time, is_booked=True)
        return redirect('calendar_view')

    context = {
        'specialists': specialists,
        'appointments': appointments,
        'days': [date.today() + timedelta(days=i) for i in range(30)],  # Next 30 days
    }
    return render(request, 'scheduler/calendar.html', context)