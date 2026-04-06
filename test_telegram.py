import urllib.request
import json
import sys

def test_bot():
    token = '8630179609:AAEhe0ljTpD9l6wRgyxWE8wqQRa8eQWvmPw'
    chat_id = '6404415447'
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    
    message = (
        "✅ <b>ბოტი წარმატებით დაუკავშირდა საიტს!</b>\n\n"
        "ეს არის სატესტო შეტყობინება. "
        "ახლა, როცა ვინმე საიტზე ტურს დაჯავშნის, თქვენ აქ მიიღებთ სრულ ინფორმაციას."
    )
    
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data)
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('ok'):
                print("✅ შეტყობინება წარმატებით გაიგზავნა ტელეგრამზე!")
            else:
                print(f"❌ შეცდომა: {result}")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"❌ ტელეგრამის შეცდომა (400): {error_body}")
    except Exception as e:
        print(f"❌ მოხდა სხვა ტიპის შეცდომა: {e}")

if __name__ == "__main__":
    test_bot()
