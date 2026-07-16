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
        "🏢 *BudTech Enterprise*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Invoice: *{invoice.invoice_number}*\n"
        f"Customer: {customer.first_name} {customer.last_name}\n\n"
        "*Purchased Items*\n"
    )

    total = 0

    for item in invoice.items.all():
        subtotal = item.quantity * item.price
        total += subtotal

        message += (
            f"• {item.product.name}\n"
            f"  Qty: {item.quantity}\n"
            f"  Price: KSh {item.price:,.2f}\n"
            f"  Subtotal: KSh {subtotal:,.2f}\n\n"
        )

    message += (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"*TOTAL: KSh {total:,.2f}*\n\n"
        "Thank you for shopping with us.\n"
        "We appreciate your business.\n\n"
        "BudTech Enterprise Management System"
    )

    encoded_message = urllib.parse.quote(message)

    whatsapp_url = (
        f"https://wa.me/{phone}?text={encoded_message}"
    )

    webbrowser.open(whatsapp_url)