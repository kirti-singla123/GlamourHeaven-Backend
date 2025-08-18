from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Booking
from .serializers import BookingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]  # you can restrict later for auth
