from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Booking, Session


# Create your views here.
def booking_page(request):
    sessions = Session.objects.all()
    return render(request, "booking/booking.html", {"sessions": sessions})


@login_required
def book_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    if not session.is_full():
        Booking.objects.create(user=request.user, session=session)
    return redirect("booking_page")
