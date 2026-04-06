import urllib.request
import urllib.parse
import json
import logging
import html

logger = logging.getLogger(__name__)

def send_telegram_notification(booking):
    """
    Sends a formatted notification about a new booking to a Telegram chat.
    """
    from .models import SiteConfiguration
    
    config = SiteConfiguration.objects.first()
    if not config or not config.telegram_bot_token or not config.telegram_chat_id:
        logger.warning("Telegram notification skipped: Missing configuration.")
        return False

    # Escape HTML special characters for the template
    full_name = html.escape(str(booking.full_name))
    expedition_title = html.escape(str(booking.expedition.title))
    travel_date = html.escape(str(booking.travel_date))
    status_display = html.escape(str(booking.get_status_display()))

    # Format the message using HTML for better reliability
    message = (
        "<b>🔔 New Booking Received!</b>\n\n"
        f"<b>👤 Customer:</b> {full_name}\n"
        f"<b>🌍 Expedition:</b> {expedition_title}\n"
        f"<b>📅 Date:</b> {travel_date}\n"
        f"<b>👥 Group Size:</b> {booking.group_size}\n"
        f"<b>💰 Total Price:</b> {booking.total_price} USD\n"
        f"<b>📌 Status:</b> {status_display}\n\n"
        "<i>Go to Admin Panel to manage this booking.</i>"
    )

    url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": config.telegram_chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data)
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req) as response:
            result = response.read().decode('utf-8')
            logger.info(f"Telegram notification sent: {result}")
            return True
    except Exception as e:
        logger.error(f"Failed to send Telegram notification: {e}")
        return False


def send_quick_lead_notification(lead):
    """
    Sends a formatted notification about a new quick lead from the Home page.
    """
    from .models import SiteConfiguration
    
    config = SiteConfiguration.objects.first()
    if not config or not config.telegram_bot_token or not config.telegram_chat_id:
        return False

    full_name = html.escape(str(lead.full_name))
    phone = html.escape(str(lead.phone_number))
    notes = html.escape(str(lead.notes)) if lead.notes else "No specific notes provided."

    message = (
        "<b>⚡️ New Quick Lead from Home!</b>\n\n"
        f"<b>👤 Name:</b> {full_name}\n"
        f"<b>📞 Phone:</b> {phone}\n"
        f"<b>📝 Note/Tour:</b> {notes}\n\n"
        "<i>Follow up as soon as possible!</i>"
    )

    url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": config.telegram_chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data)
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req) as response:
            return True
    except Exception as e:
        logger.error(f"Failed to send lead notification: {e}")
        return False
