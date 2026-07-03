from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer
from twilio.rest import Client
import os

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]  # default

    def get_permissions(self):
        # Allow public users to create bookings
        if self.action == 'create':
            return [AllowAny()]
        # All other actions (list, update, delete, accept, reject) require login
        return [IsAuthenticated()]

    def send_whatsapp_message(self, to_number, message_body):
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        phone_number = os.environ.get('TWILIO_PHONE_NUMBER')

        missing = [name for name, value in (
            ('TWILIO_ACCOUNT_SID', account_sid),
            ('TWILIO_AUTH_TOKEN', auth_token),
            ('TWILIO_PHONE_NUMBER', phone_number),
        ) if not value]
        if missing:
            raise RuntimeError(
                f"Missing Twilio environment variable(s): {', '.join(missing)}"
            )

        from_number = 'whatsapp:' + phone_number
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_=from_number,
            body=message_body,
            to=f'whatsapp:{to_number}'
        )
        return message.sid

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        booking = self.get_object()
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
            print("Twilio error:", e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Booking accepted', 'sid': sid, 'status': booking.status},
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        booking = self.get_object()
        booking.status = 'rejected'
        booking.save()

        message_body = (
            f"❌ Hi {booking.name}, sorry this slot is full.\n"
            f"Service: {booking.service}\n"
            f"Please select another date or time."
        )

        try:
            sid = self.send_whatsapp_message(booking.phone, message_body)
        except Exception as e:
            print("Twilio error:", e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Booking rejected', 'sid': sid, 'status': booking.status},
                        status=status.HTTP_200_OK)
