import africastalking
from django.conf import settings


def send_invoice_sms(invoice):

    try:
        africastalking.initialize(
            settings.AT_USERNAME,
            settings.AT_API_KEY
        )

        sms = africastalking.SMS

        customer = invoice.customer

        # Convert Kenyan phone numbers to international format
        phone = customer.phone.replace(" ", "").strip()

        if phone.startswith("0"):
            phone = "+254" + phone[1:]

        elif phone.startswith("254"):
            phone = "+" + phone

        elif not phone.startswith("+254"):
            phone = "+254" + phone

        message = (
            f"Hello {customer.first_name}, "
            f"Thank you for shopping with Budtech. "
            f"Invoice Number: {invoice.invoice_number}. "
            f"Your purchase has been received successfully."
        )

        response = sms.send(
            message,
            [phone]
        )

        print("SMS RESPONSE:", response)

        return response

    except Exception as e:
        print("SMS ERROR:", e)
        return None