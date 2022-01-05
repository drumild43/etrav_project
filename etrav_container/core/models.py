from django.db import models
from django.db.models import Avg, Count
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class EtravUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user
        
class EtravUser(AbstractBaseUser):
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    logged_in = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)

    objects = EtravUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Hotel(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    city = models.ForeignKey('City', on_delete=models.PROTECT)
    standard_room_price = models.PositiveIntegerField()
    suite_price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def get_img_name(self):
        return "store/images/" + self.name + ".jpg"

    def get_avg_rating(self):
        avg_rating = Review.objects.filter(
                hotel__pk=self.id
            ).aggregate(
                Avg('rating')
            )['rating__avg']

        return avg_rating
    
    def get_review_count(self):
        review_count = Hotel.objects.filter(
                pk=self.id
            ).annotate(
                Count('review')
            )[0].review__count

        return review_count

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Booking(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT)
    user = models.ForeignKey(EtravUser, on_delete=models.CASCADE)
    
    booked_on = models.DateTimeField()
    total_price = models.PositiveIntegerField()
    checkin_time = models.DateTimeField()
    checkout_time = models.DateTimeField()
    adult_count = models.PositiveIntegerField()
    child_count = models.PositiveIntegerField()

    CONFIRMED = 'C'
    ACTIVE = 'A'
    COMPLETE = 'K'
    CANCELLED = 'X'
    STATUS_CHOICES = [
        (CONFIRMED, 'Confirmed'),
        (ACTIVE, 'Stay Ongoing'),
        (COMPLETE, 'Stay Complete'),
        (CANCELLED, 'Cancelled')
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=CONFIRMED)

    def get_updated_status(self):
        # if booking not cancelled or complete, update status
        if self.status != 'X' and self.status != 'K':
            if timezone.now() < self.checkin_time:
                self.status = 'C'

            elif timezone.now() < self.checkout_time:
                self.status = 'A'

            else:
                self.status = 'K'

            self.save()

        return self.get_status_display()

class Review(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user = models.ForeignKey(EtravUser, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField()

    def is_verified(self):
        # list of user's bookings with given hotel
        bookings = Booking.objects.filter(
            user__pk=self.user.id, 
            hotel__pk=self.hotel.id
        )

        for booking in bookings:
            # verified if there is a completed stay
            if booking.get_updated_status() == 'Stay Complete':
                return True

        return False