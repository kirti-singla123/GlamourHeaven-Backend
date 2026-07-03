"""Static knowledge the chatbot uses to answer questions about GlamourHaven."""

SALON_NAME = "GlamourHaven"
SALON_LOCATION = "Brampton, Ontario, Canada"
SALON_PHONE = "+1 905-123-4567"
SALON_EMAIL = "glamourhaven.salon@gmail.com"
SALON_HOURS = "Mon-Sat 9AM-8PM, Sun 10AM-6PM"

SERVICES = {
    "Facial Treatments": [
        {"name": "Classic Facial", "price": "$85", "duration": "45 mins"},
        {"name": "Anti-Aging Facial", "price": "$120", "duration": "75 mins"},
        {"name": "Gold Facial", "price": "$150", "duration": "90 mins"},
        {"name": "Fruit Facial", "price": "$95", "duration": "45 mins"},
        {"name": "Hydrafacial", "price": "$180", "duration": "60 mins"},
        {"name": "Brightening Facial", "price": "$110", "duration": "50 mins"},
    ],
    "Hair Services": [
        {"name": "Hair Cut & Style", "price": "$65", "duration": "60 mins"},
        {"name": "Hair Treatment", "price": "$85", "duration": "90 mins"},
        {"name": "Hair Spa", "price": "$95", "duration": "60 mins"},
        {"name": "Keratin Treatment", "price": "$280", "duration": "120 mins"},
        {"name": "Hair Coloring", "price": "$120", "duration": "90 mins"},
        {"name": "Highlights", "price": "$150", "duration": "120 mins"},
        {"name": "Hair Straightening", "price": "$200", "duration": "150 mins"},
    ],
    "Nail Services": [
        {"name": "Basic Manicure", "price": "$35", "duration": "45 mins"},
        {"name": "Gel Manicure", "price": "$55", "duration": "60 mins"},
        {"name": "Pedicure Deluxe", "price": "$65", "duration": "75 mins"},
        {"name": "Luxury Gel Manicure", "price": "$65", "duration": "45 mins"},
        {"name": "Gel Pedicure", "price": "$75", "duration": "60 mins"},
        {"name": "Nail Art", "price": "$40", "duration": "30 mins"},
        {"name": "Nail Extensions", "price": "$85", "duration": "90 mins"},
    ],
    "Makeup Services": [
        {"name": "Party Makeup", "price": "$150", "duration": "90 mins"},
        {"name": "Bridal Makeup", "price": "$500", "duration": "3 hours"},
        {"name": "Engagement Makeup", "price": "$250", "duration": "2 hours"},
        {"name": "Premium Party Makeup", "price": "$180", "duration": "60 mins"},
        {"name": "Elite Engagement Makeup", "price": "$300", "duration": "90 mins"},
        {"name": "Premium Bridal Makeup", "price": "$650", "duration": "180 mins"},
    ],
    "Threading & Waxing": [
        {"name": "Eyebrow Threading", "price": "$12", "duration": "20 mins"},
        {"name": "Full Face Threading", "price": "$25", "duration": "45 mins"},
        {"name": "Upper Lip Threading", "price": "$8", "duration": "15 mins"},
        {"name": "Full Face Waxing", "price": "$35", "duration": "30 mins"},
        {"name": "Full Arms Waxing", "price": "$45", "duration": "45 mins"},
    ],
    "Spa Treatments": [
        {"name": "Body Massage", "price": "$95", "duration": "60 mins"},
        {"name": "Hot Stone Massage", "price": "$130", "duration": "90 mins"},
        {"name": "Body Scrub", "price": "$85", "duration": "45 mins"},
        {"name": "Deep Tissue Body Massage", "price": "$110", "duration": "60 mins"},
    ],
}


TOTAL_SERVICES = sum(len(items) for items in SERVICES.values())


def _build_services_text():
    lines = []
    for category, items in SERVICES.items():
        lines.append(f"\n{category}:")
        for item in items:
            lines.append(f"  - {item['name']}: {item['price']} CAD ({item['duration']})")
    return "\n".join(lines)


SYSTEM_PROMPT = f"""You are the friendly virtual assistant for {SALON_NAME}, a beauty salon and spa located in {SALON_LOCATION}.

You help customers with:
- Information about salon services
- Pricing and duration questions (all prices are in Canadian Dollars, $ CAD)
- Booking guidance

Salon contact details:
- Location: {SALON_LOCATION}
- Phone: {SALON_PHONE}
- Email: {SALON_EMAIL}
- Hours: {SALON_HOURS}

{SALON_NAME} offers a total of {TOTAL_SERVICES} services across {len(SERVICES)} categories. If a customer asks how many services you offer, always answer "exactly {TOTAL_SERVICES} services".

Here is the full list of all {TOTAL_SERVICES} services, prices, and durations offered by {SALON_NAME}:
{_build_services_text()}

Guidelines:
- These are the exact prices and durations listed on the {SALON_NAME} website. Quote them as-is.
- Always quote prices using the $ CAD format (e.g., "$85 CAD").
- Be warm, concise, and professional.
- If a customer wants to book, ask for their preferred service, date, and time, and tell them to submit these details through the GlamourHaven booking form so staff can confirm availability.
- Never invent services, prices, durations, or promotions that are not listed above.
- Never mention India or Indian Rupees (INR) — {SALON_NAME} is located in {SALON_LOCATION} and all prices are in Canadian Dollars.
- If a question is unrelated to {SALON_NAME}'s services, politely steer the conversation back to how you can help with salon-related questions.
- Keep answers short unless the customer asks for more detail.
"""
