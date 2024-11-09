from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
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
        try:
            Booking.objects.create(user=request.user, session=session)
            messages.success(
                request, f"You have successfully booked this {session.title} session."
            )
        except IntegrityError:
            messages.error(
                request, f"You have already booked this {session.title} session."
            )
    else:
        messages.error(request, f"This {session.title} session is fully booked.")
    return redirect("booking_page")
