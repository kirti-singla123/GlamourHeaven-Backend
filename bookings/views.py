from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Booking, format_phone_number
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

    def build_message_body(self, booking):
        if booking.status == 'accepted':
            return (
                f"✅ Hi {booking.name}, your booking is confirmed!\n"
                f"Service: {booking.service}\n"
                f"Date: {booking.date}\n"
                f"Time: {booking.time}"
            )
        return (
            f"❌ Hi {booking.name}, sorry this slot is full.\n"
            f"Service: {booking.service}\n"
            f"Please select another date or time."
        )

    def perform_update(self, serializer):
        previous_status = serializer.instance.status
        booking = serializer.save()
        status_changed_to_final = (
            previous_status != booking.status and booking.status in ('accepted', 'rejected')
        )
        if status_changed_to_final:
            print(
                f"[Booking] status changed to {booking.status!r} via generic update "
                f"for booking id={booking.id} phone={booking.phone!r}"
            )
            try:
                self.send_whatsapp_message(booking.phone, self.build_message_body(booking))
            except Exception as e:
                print(f"[WhatsApp] FAILED - {type(e).__name__}: {e}")

    def send_whatsapp_message(self, to_number, message_body):
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        phone_number = os.environ.get('TWILIO_PHONE_NUMBER')

        print(
            "[WhatsApp] env check -> "
            f"SID set={bool(account_sid)} (prefix={account_sid[:4] if account_sid else None}), "
            f"TOKEN set={bool(auth_token)} (len={len(auth_token) if auth_token else 0}), "
            f"FROM_NUMBER={phone_number!r}"
        )

        missing = [name for name, value in (
            ('TWILIO_ACCOUNT_SID', account_sid),
            ('TWILIO_AUTH_TOKEN', auth_token),
            ('TWILIO_PHONE_NUMBER', phone_number),
        ) if not value]
        if missing:
            print(f"[WhatsApp] ABORT - missing env var(s): {', '.join(missing)}")
            raise RuntimeError(
                f"Missing Twilio environment variable(s): {', '.join(missing)}"
            )

        from_number = 'whatsapp:' + phone_number
        formatted_to = format_phone_number(to_number)
        print(f"[WhatsApp] raw to_number={to_number!r} -> formatted={formatted_to!r}")

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_=from_number,
            body=message_body,
            to=f'whatsapp:{formatted_to}'
        )
        print(
            f"[WhatsApp] Twilio response -> sid={message.sid} status={message.status} "
            f"error_code={message.error_code} error_message={message.error_message}"
        )
        return message.sid

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        booking = self.get_object()
        print(f"[Booking] accept() called for booking id={booking.id} phone={booking.phone!r}")
        booking.status = 'accepted'
        booking.save()

        message_body = self.build_message_body(booking)

        try:
            sid = self.send_whatsapp_message(booking.phone, message_body)
        except Exception as e:
            print(f"[WhatsApp] FAILED - {type(e).__name__}: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Booking accepted', 'sid': sid, 'status': booking.status},
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        booking = self.get_object()
        print(f"[Booking] reject() called for booking id={booking.id} phone={booking.phone!r}")
        booking.status = 'rejected'
        booking.save()

        message_body = self.build_message_body(booking)

        try:
            sid = self.send_whatsapp_message(booking.phone, message_body)
        except Exception as e:
            print(f"[WhatsApp] FAILED - {type(e).__name__}: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Booking rejected', 'sid': sid, 'status': booking.status},
                        status=status.HTTP_200_OK)
