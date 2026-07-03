from django.db import migrations


def format_phone_number(phone):
    # Normalize to E.164 for Canada/US (+1)
    cleaned = phone.replace(' ', '').replace('-', '')

    if cleaned.startswith('+'):
        return cleaned
    if cleaned.startswith('1'):
        return f'+{cleaned}'
    if len(cleaned) == 10 and cleaned.isdigit():
        return f'+1{cleaned}'
    return cleaned


def fix_phone_numbers(apps, schema_editor):
    Booking = apps.get_model('bookings', 'Booking')
    for booking in Booking.objects.all():
        # Undo the old +91 (India) prefix before re-normalizing to +1 (Canada)
        phone = booking.phone
        if phone.startswith('+91'):
            phone = phone[3:]
        formatted = format_phone_number(phone)
        if formatted != booking.phone:
            booking.phone = formatted
            booking.save(update_fields=['phone'])


def reverse_noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0002_booking_status"),
    ]

    operations = [
        migrations.RunPython(fix_phone_numbers, reverse_noop),
    ]
