import urllib.parse
import webbrowser


def send_invoice_whatsapp(invoice):

    customer = invoice.customer

    phone = customer.phone.replace(" ", "").strip()

    if phone.startswith("0"):
        phone = "254" + phone[1:]

    elif phone.startswith("+254"):
        phone = phone.replace("+", "")

    message = (
        f"Hello {customer.first_name},\n\n"
        f"Thank you for shopping with Budtech.\n"
        f"Invoice Number: {invoice.invoice_number}\n"
        f"Your invoice has been created successfully."
    )

    encoded_message = urllib.parse.quote(message)

    whatsapp_url = (
        f"https://wa.me/{phone}?text={encoded_message}"
    )

    webbrowser.open(whatsapp_url)