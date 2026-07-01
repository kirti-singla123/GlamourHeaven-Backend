"""Static knowledge the chatbot uses to answer questions about GlamourHaven."""

SALON_NAME = "GlamourHaven"

SERVICES = {
    "Facial Treatments": [
        {"name": "Classic Facial", "price": "₹1,500", "duration": "45 mins"},
        {"name": "Anti-Aging Facial", "price": "₹3,500", "duration": "75 mins"},
        {"name": "Gold Facial", "price": "₹5,000", "duration": "90 mins"},
        {"name": "Fruit Facial", "price": "₹1,200", "duration": "45 mins"},
        {"name": "Hydrafacial", "price": "₹4,500", "duration": "60 mins"},
        {"name": "Brightening Facial", "price": "₹2,000", "duration": "50 mins"},
    ],
    "Hair Services": [
        {"name": "Hair Cut & Style", "price": "₹800", "duration": "60 mins"},
        {"name": "Hair Treatment", "price": "₹1,800", "duration": "90 mins"},
        {"name": "Hair Spa", "price": "₹1,500", "duration": "60 mins"},
        {"name": "Keratin Treatment", "price": "₹5,000", "duration": "120 mins"},
        {"name": "Hair Coloring", "price": "₹3,000", "duration": "90 mins"},
        {"name": "Highlights", "price": "₹4,000", "duration": "120 mins"},
        {"name": "Hair Straightening", "price": "₹4,500", "duration": "150 mins"},
    ],
    "Nail Services": [
        {"name": "Basic Manicure", "price": "₹600", "duration": "45 mins"},
        {"name": "Gel Manicure", "price": "₹1,200", "duration": "60 mins"},
        {"name": "Pedicure Deluxe", "price": "₹1,000", "duration": "75 mins"},
        {"name": "Luxury Gel Manicure", "price": "₹1,200", "duration": "45 mins"},
        {"name": "Gel Pedicure", "price": "₹1,500", "duration": "60 mins"},
        {"name": "Nail Art", "price": "₹800", "duration": "30 mins"},
        {"name": "Nail Extensions", "price": "₹2,000", "duration": "90 mins"},
    ],
    "Makeup Services": [
        {"name": "Party Makeup", "price": "₹2,500", "duration": "90 mins"},
        {"name": "Bridal Makeup", "price": "₹8,000", "duration": "3 hours"},
        {"name": "Engagement Makeup", "price": "₹4,500", "duration": "2 hours"},
        {"name": "Premium Party Makeup", "price": "₹3,000", "duration": "60 mins"},
        {"name": "Elite Engagement Makeup", "price": "₹6,000", "duration": "90 mins"},
        {"name": "Premium Bridal Makeup", "price": "₹15,000", "duration": "180 mins"},
    ],
    "Threading & Waxing": [
        {"name": "Eyebrow Threading", "price": "₹200", "duration": "20 mins"},
        {"name": "Full Face Threading", "price": "₹500", "duration": "45 mins"},
        {"name": "Upper Lip Threading", "price": "₹150", "duration": "15 mins"},
        {"name": "Full Face Waxing", "price": "₹400", "duration": "30 mins"},
        {"name": "Full Arms Waxing", "price": "₹600", "duration": "45 mins"},
    ],
    "Spa Treatments": [
        {"name": "Body Massage", "price": "₹2,000", "duration": "60 mins"},
        {"name": "Hot Stone Massage", "price": "₹3,500", "duration": "90 mins"},
        {"name": "Body Scrub", "price": "₹1,800", "duration": "45 mins"},
        {"name": "Deep Tissue Body Massage", "price": "₹2,500", "duration": "60 mins"},
    ],
}


TOTAL_SERVICES = sum(len(items) for items in SERVICES.values())


def _build_services_text():
    lines = []
    for category, items in SERVICES.items():
        lines.append(f"\n{category}:")
        for item in items:
            lines.append(f"  - {item['name']}: {item['price']} ({item['duration']})")
    return "\n".join(lines)


SYSTEM_PROMPT = f"""You are the friendly virtual assistant for {SALON_NAME}, a beauty salon and spa in India.

You help customers with:
- Information about salon services
- Pricing and duration questions (all prices are in Indian Rupees, INR)
- Booking guidance

{SALON_NAME} offers a total of {TOTAL_SERVICES} services across {len(SERVICES)} categories. If a customer asks how many services you offer, always answer "{TOTAL_SERVICES} services".

Here is the full list of all {TOTAL_SERVICES} services, prices, and durations offered by {SALON_NAME}:
{_build_services_text()}

Guidelines:
- These are the exact prices and durations listed on the {SALON_NAME} website. Quote them as-is.
- Be warm, concise, and professional.
- If a customer wants to book, ask for their preferred service, date, and time, and tell them to submit these details through the GlamourHaven booking form so staff can confirm availability.
- Never invent services, prices, durations, or promotions that are not listed above.
- If a question is unrelated to {SALON_NAME}'s services, politely steer the conversation back to how you can help with salon-related questions.
- Keep answers short unless the customer asks for more detail.
"""
