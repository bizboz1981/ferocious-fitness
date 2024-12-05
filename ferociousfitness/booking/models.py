from django.conf import settings
from django.db import models


# Create your models here.
class ClassType(models.Model):
    """
    Represents a type of class offered, such as a group class or personal training session.

    Attributes:
        name (str): The name of the class type.
        description (str, optional): A brief description of the class type.
    """

    name = models.CharField(max_length=50)  # E.g., "Group Class" or "PT Session"
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Session(models.Model):
    """
    Represents a fitness session, which can be either a group class or a personal training session.

    Attributes:
        title (str): The title of the session (e.g., "Yoga", "HIIT", "Circuits").
        description (str, optional): A brief description of the session.
        session_type (ClassType): The type of session, linked to the ClassType model.
        date (date): The date on which the session is scheduled.
        time (time): The time at which the session is scheduled.
        location (str, optional): The location where the session will take place.
        max_participants (int): The maximum number of participants allowed in the session. Defaults to 1 for personal training sessions.
        current_participants (int): The current number of participants enrolled in the session. Defaults to 0 and is not editable.

    Methods:
        __str__(): Returns a string representation of the session, including its title, date, and time.
        spots_remaining(): Returns the number of spots remaining in the session.
        is_full(): Checks if the session is fully booked.
    """

    SESSION_TYPES = [
        ("group", "Group Class"),
        ("pt", "Personal Training"),
    ]

    title = models.CharField(max_length=100)  # E.g., "Yoga", "HIIT", "Circuits"
    description = models.TextField(blank=True, null=True)
    session_type = models.ForeignKey(ClassType, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100, blank=True)
    max_participants = models.PositiveIntegerField(
        default=1
    )  # Limit for group classes; default 1 for PT sessions
    current_participants = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return f"{self.title} on {self.date} at {self.time}"

    def spots_remaining(self):
        return self.max_participants - self.current_participants

    def is_full(self):
        return self.current_participants >= self.max_participants


class Booking(models.Model):
    """
    Represents a booking made by a user for a specific session.

    Attributes:
        user (ForeignKey): Reference to the user who made the booking.
        session (ForeignKey): Reference to the session being booked.
        booking_date (DateTimeField): The date and time when the booking was made.

    Meta:
        unique_together (tuple): Ensures that a user cannot book the same session more than once.

    Methods:
        __str__(): Returns a string representation of the booking.
        save(*args, **kwargs): Saves the booking and increments the session's participant count.
        delete(*args, **kwargs): Deletes the booking and decrements the session's participant count.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name="bookings"
    )
    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "user",
            "session",
        )  # Prevents duplicate bookings by the same user for the same session

    def __str__(self):
        return (
            f"{self.user.username} booked {self.session.title} on {self.session.date}"
        )

    def save(self, *args, **kwargs):
        # Check if session has available spots
        if self.session.is_full():
            raise ValueError("This session is already fully booked.")
        super().save(*args, **kwargs)
        # Increment participants after saving the booking
        self.session.current_participants += 1
        self.session.save()

    def delete(self, *args, **kwargs):
        # Decrement participants when a booking is cancelled
        if (
            not self.session.is_full()
        ):  # This check is not logically necessary - refactor
            self.session.current_participants -= 1
            self.session.save()
        super().delete(*args, **kwargs)
