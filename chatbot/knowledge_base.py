"""Static knowledge the chatbot uses to answer questions about GlamourHaven."""

SALON_NAME = "GlamourHaven"

SERVICES = {
    "Facial Treatments": [
        {"name": "Classic Facial", "price": "₹800 - ₹1,200"},
        {"name": "Fruit Facial", "price": "₹700 - ₹1,000"},
        {"name": "Gold Facial", "price": "₹1,500 - ₹2,500"},
        {"name": "Anti-Ageing Facial", "price": "₹2,000 - ₹3,500"},
        {"name": "Hydrafacial", "price": "₹3,000 - ₹5,000"},
    ],
    "Hair Services": [
        {"name": "Haircut & Styling", "price": "₹300 - ₹800"},
        {"name": "Hair Spa", "price": "₹800 - ₹1,500"},
        {"name": "Hair Coloring / Highlights", "price": "₹1,500 - ₹4,000"},
        {"name": "Keratin Treatment", "price": "₹3,000 - ₹6,000"},
        {"name": "Hair Straightening / Smoothening", "price": "₹2,500 - ₹6,000"},
    ],
    "Nail Services": [
        {"name": "Manicure", "price": "₹400 - ₹700"},
        {"name": "Pedicure", "price": "₹500 - ₹900"},
        {"name": "Gel Nail Extension", "price": "₹1,200 - ₹2,000"},
        {"name": "Nail Art (add-on)", "price": "₹200 - ₹800"},
    ],
    "Makeup": [
        {"name": "Party Makeup", "price": "₹1,500 - ₹3,000"},
        {"name": "Engagement Makeup", "price": "₹4,000 - ₹8,000"},
        {"name": "HD / Airbrush Makeup", "price": "₹5,000 - ₹12,000"},
        {"name": "Bridal Makeup", "price": "₹8,000 - ₹25,000"},
    ],
    "Threading & Waxing": [
        {"name": "Eyebrow Threading", "price": "₹50 - ₹100"},
        {"name": "Upper Lip Threading", "price": "₹30 - ₹50"},
        {"name": "Full Face Waxing", "price": "₹300 - ₹500"},
        {"name": "Full Arms & Legs Waxing", "price": "₹600 - ₹1,200"},
        {"name": "Full Body Waxing", "price": "₹1,500 - ₹2,500"},
    ],
    "Spa Treatments": [
        {"name": "Head & Shoulder Massage", "price": "₹500 - ₹900"},
        {"name": "Body Massage (60 min)", "price": "₹1,500 - ₹2,500"},
        {"name": "Aromatherapy", "price": "₹2,000 - ₹3,000"},
        {"name": "Body Polishing", "price": "₹2,500 - ₹4,000"},
    ],
}


def _build_services_text():
    lines = []
    for category, items in SERVICES.items():
        lines.append(f"\n{category}:")
        for item in items:
            lines.append(f"  - {item['name']}: {item['price']}")
    return "\n".join(lines)


SYSTEM_PROMPT = f"""You are the friendly virtual assistant for {SALON_NAME}, a beauty salon and spa in India.

You help customers with:
- Information about salon services
- Pricing questions (all prices are in Indian Rupees, INR)
- Booking guidance

Here is the full list of services and indicative pricing offered by {SALON_NAME}:
{_build_services_text()}

Guidelines:
- Prices are approximate starting ranges and can vary based on hair/skin condition, products used, and stylist. Mention this when quoting a price.
- Be warm, concise, and professional.
- If a customer wants to book, ask for their preferred service, date, and time, and tell them to submit these details through the GlamourHaven booking form so staff can confirm availability.
- Never invent services, prices, or promotions that are not listed above.
- If a question is unrelated to {SALON_NAME}'s services, politely steer the conversation back to how you can help with salon-related questions.
- Keep answers short unless the customer asks for more detail.
"""
