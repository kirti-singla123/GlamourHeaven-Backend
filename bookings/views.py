from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Booking
from .serializers import BookingSerializer
from twilio.rest import Client
import os

class BookingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def send_whatsapp_message(self, to_number, message_body):
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        from_number = 'whatsapp:' + os.environ['TWILIO_PHONE_NUMBER']
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_=from_number,
            body=message_body,
            to=f'whatsapp:{to_number}'
        )
        return message.sid

    # List all bookings
    def list(self, request):
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    # Retrieve a single booking
    def retrieve(self, request, pk=None):
        booking = Booking.objects.get(pk=pk)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    # Create a booking
    def create(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Update a booking
    def update(self, request, pk=None):
        booking = Booking.objects.get(pk=pk)
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Partially update a booking
    def partial_update(self, request, pk=None):
        booking = Booking.objects.get(pk=pk)
        serializer = BookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete a booking
    def destroy(self, request, pk=None):
        booking = Booking.objects.get(pk=pk)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Custom actions
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        booking = Booking.objects.get(pk=pk)
        booking.status = 'accepted'
        booking.save()
        message_body = (
            f"✅ Hi {booking.name}, your booking is confirmed!\n"
            f"Service: {booking.service}\n"
            f"Date: {booking.date}\n"
            f"Time: {booking.time}"
        )
        try:
            sid = self.send_whatsapp_message(booking.phone, message_body)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message': 'Booking accepted', 'sid': sid, 'status': booking.status})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        booking = Booking.objects.get(pk=pk)
        booking.status = 'rejected'
        booking.save()
        message_body = (
            f"❌ Hi {booking.name}, sorry this slot is full.\n"
            f"Service: {booking.service}\n"
            f"Please select another date or time."
        )
        sid = self.send_whatsapp_message(booking.phone, message_body)
        return Response({'message': 'Booking rejected', 'sid': sid, 'status': booking.status})
