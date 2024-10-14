from flask import Flask, request, jsonify
from dotenv import load_dotenv
from supabase import create_client, Client
import requests
import json
import os

load_dotenv()
app = Flask(__name__)

url: str = "https://volvagvupzbzchijpcfc.supabase.co"
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)
# BINOLLA_ID = 2742
BINOLLA_ID = 2546
POCKET_OPTION_ID = "Xp7RRXNbbaz1OD"
QUOTEX_ID_1 = "539064"
QUOTEX_ID_2 = "769967"
# DB_URL = "https://sheetdb.io/api/v1/elplwx89ccqc5"
BOT_TOKEN = "6342751531:AAHX2JqysafKfM00OHkjLeoguEUSLZWLHZc"
USR_PLATFORM = None
TABLE = "VerificationTable"
INVITE_LINKS = {
    # "Quotex": -1002152323652,
    "PocketOption": -1002215318957,
    "Binolla": -1002041096139,
}
# https://0e93-149-102-244-103.ngrok-free.app
#  reload
def update_user(id, platform, dep_amount, used, conf):
    global supabase

    # data = {"deposited": dep_amount, "used": used}
    try:
        resp = supabase.rpc(
            "update_user",
            {
                "p_trader_id": id,
                "p_used": used,
                "p_deposited": dep_amount,
                "p_conf": conf,
                "p_table_name": TABLE,
            },
        ).execute()
    except Exception as e:
        # send_message("Invalid Message, press `/start` to retry")
        print(e)
    print("Updated", resp)

# reload
def check_user(id):
    global supabase, USR_PLATFORM
    result, data = supabase.table(TABLE).select("*").eq("trader_id", int(id)).execute()
    if len(result[1]) == 0 or result[1][0]["site_name"] != USR_PLATFORM:
        return "notfnd"
    elif not result[1][0]["conf"]:
        return "confreq"
    elif result[1][0]["used"]:
        return "usd"
    USR_PLATFORM = result[1][0]["site_name"]
    update_user(id, USR_PLATFORM, dep_amount=result[1][0]["deposited"], used=True)
    return "pass"


# reload11
def check_redunduncy(uid, site_name, deposit, conf):
    global supabase
    # Define the parameters
    try:

        result, count = (
            supabase.table(TABLE).select("*").eq("trader_id", int(uid)).execute()
        )
    except Exception as e:
        # send_message("Invalid Message, press `/start` to retry")
        print(e)
    if len(result[1]) == 0:
        return True
    prev_dep = float(result[1][0]["deposited"])
    new_dep = float(deposit) if ((deposit != "") and deposit != None) else 0
    summed = prev_dep + new_dep
    if not result[1][0]["conf"] and conf:
        update_user(uid, site_name, summed, bool(result[1][0]["used"]), True)
    else:
        update_user(uid, site_name, summed, bool(result[1][0]["used"]), result[1][0]["conf"])
    return False

    

def add_user(uid, site_name, deposit, conf):
    global supabases
    """Adds user to database"""
    if check_redunduncy(uid, site_name, deposit, conf):
        data = {
            # "serial_number": "INCREMENT",
            "site_name": site_name,
            "trader_id": uid,
            "used": False,
            "deposited": float(deposit) if ((deposit != "") and deposit != None) else 0,
            "conf": conf,
        }
        try:
            resp = supabase.table(TABLE).insert(data).execute()
        except Exception as e:
            # send_message("Invalid Message, press `/start` to retry")
            print(e)
            return
        
        print("ADDED USER", resp)


# reload1
def send_message(res, chat_id):
    """Sends a message to a Telegram chat.
    
    Args:
        res (str): The message to be sent.
        chat_id (int): The chat ID to send the message to.
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": res}
    requests.post(url=url, json=payload)


def handle_message(message):
    global USR_PLATFORM
    print("GOT MESSAGE", message)
    try:
        text: str = message["message"]["text"]
    except KeyError:
        # Handle the KeyError here, such as by assigning a default value to text
        print(message)
        print("No Text")
        return

    user_name = (
        message["message"]["from"]["first_name"]
        # + " "
        # + message["message"]["from"]["last_name"]
    )
    chat_id = message["message"]["chat"]["id"]
    response = "Invalid message"
    if text == "/start":
        response = f"Welcome, Trader Alvee to Alvee Signal Verfication Bot. See our vip members review👉 @alveessignal1\n\nStart by selecting the trading platform you were referred to.\n\n[Bangla] স্বাগতম, আলভি সিগন্যাল ভেরিফিকেশন বট-এ।\nপ্রতিদিন আমাদের VIP মেম্বাররা কত প্রফিট করেছে  এখানে দেখুন 👉 @alveessignal1\n\n✅একাউন্ট করতে অথবা ডিপোজিট সম্পর্কিত তথ্য জানতে এখানে ক্লিক করুন \n👉@alveesupportbot\n\nVIP চ্যানেলে জয়েন করতে নিচে থেকে আপনার পছন্দের প্লাটফর্ম চয়েস করুন👇"
        keyboard = '{ "keyboard": [[ "Pocket Option", "Binolla"]], "is_persistent": true, "resize_keyboard": true, "one_time_keyboard": true }'

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": response, "reply_markup": keyboard}
        requests.post(url=url, json=payload)
    # elif text == "Quotex":
    #     response = "Send your Trader ID:\n\n[Bangla] আপনার আইডি চেক করতে অথবা vip চ্যানেল লিংক পেতে Quotex ট্রেডার আইডি দিন:"
    #     USR_PLATFORM = "Quotex"
    #     send_message(response, chat_id=chat_id)
    elif ".peKv%o|<L9^5Ur.8:v`B@G<}zE!k{" in text:
        send_message("Admin Authenticated", chat_id=chat_id)
    elif text == "Pocket Option":
        response = "Send your Trader ID:\n\n[Bangla] আপনার আইডি চেক করতে অথবা vip চ্যানেল লিংক পেতে Pocket Option ট্রেডার আইডি দিন:"
        USR_PLATFORM = "PocketOption"
        send_message(response, chat_id=chat_id)
    elif text == "Binolla":
        response = "Send your Trader ID:\n\n[Bangla] আপনার আইডি চেক করতে অথবা vip চ্যানেল লিংক পেতে Binolla ট্রেডার আইডি দিন:"
        USR_PLATFORM = "Binolla"
        send_message(response, chat_id=chat_id)
    elif text.isnumeric():
        if USR_PLATFORM == None:
            send_message("Select Platform First", chat_id=chat_id)
            return
        checkUser = check_user(text)
        if checkUser == "confreq":
            # if USR_PLATFORM == "Quotex":
            #     send_message(
            #         "Your account created from our link. Now deposit $30 and Get our vip Channel Link.\n\n[Bangla]  আপনার একাউন্ট খোলা সফল হয়েছে এখন $৩০ ডিপোজিট করুন তাহলে আপনাকে VIP চ্যানেলের লিংক দেওয়া হবে।\n\n📊ডিপোজিট বোনাস পেতে নিচের Promo code ব্যাবহার করুন📊👇👇\n\n➡️Special  Promo Code: Alvee\n\n➡️Monthly Promo Code : 8gLK9ldJTy\n\n➡️150$ Promo Code: RLR50",
            #         chat_id=chat_id,
            #     )
            # if USR_PLATFORM == "PocketOption":
            send_message(
                "Your account created from our link. Now Verify your account and Get our vip Channel Link.\n\n[Bangla]  আপনার একাউন্ট খোলা সফল হয়েছে এখন ভেরিফাই করুন তাহলে আপনাকে Private  চ্যানেলের লিংক দেওয়া হবে।\n\n📊ডিপোজিট বোনাস পেতে নিচের Promo code ব্যাবহার করুন📊👇👇\n\n➡Special  Promo Code: TTQ438\n\n👆এই প্রমোকোড টি ব্যাবহার করার জন্য সর্বনিম্ন $৫০ ডিপোজিট করতে হবে।",
                chat_id=chat_id,
            )
            # else:
            #     send_message(
            #         "Your account created from our link. Now deposit $30 and Get our vip Channel Link.\n\n[Bangla]  আপনার একাউন্ট খোলা সফল হয়েছে এখন $৩০ ডিপোজিট করুন তাহলে আপনাকে VIP চ্যানেলের লিংক দেওয়া হবে।\n\n📊ডিপোজিট বোনাস পেতে নিচের Promo code ব্যাবহার করুন📊👇👇\n\n➡️Special  Promo Code: mqf895",
            #         chat_id=chat_id,
            #     )
        elif checkUser == "notfnd":
            message = (
                f"❌ this account ({text}) not created with my link\n\n"
                "[Bangla] আপনার একাউন্ট আমাদের রেফার লিংক থেকে খোলা হয়নি নিচের লিংক থেকে একাউন্ট করে আবার ট্রাই করুন।\n\n"
                "Create account and deposit minimum $30👇🔥📈\n\n"
                "Create`Pocket Option` or `Binolla` With The Link -👇\n\n"
                " https://cutt.ly/LeW1XNDQ\n\n"
                "https://cutt.ly/9w3EC0i0\n\n"
                "Deposit Minimum = $30 or more\n\n"
                " Pocket Option [  50% Bonus  = Aokcipbs ]\n\n"
                "Binolla [  50% Bonus  = a7ukwp ]\n\n"
                "Then Send TRADER ID (Only ID NO)"
            )
            send_message(
                message,
                chat_id=chat_id,
            )

        elif checkUser == "pass":
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/createChatInviteLink"
            payload = {
                "chat_id": INVITE_LINKS[USR_PLATFORM],
                "name": f"Created by {user_name} for {USR_PLATFORM}",
                "member_limit": 1,
            }
            response = requests.post(url=url, json=payload)
            send_message(
                f"Hey {user_name} congratulations you've successfully completed everything. Now join here for VIP Signal.",
                chat_id,
            )
            try:
                send_message(response.json()["result"]["invite_link"], chat_id)
            except:
                print("Couldnt send invite link")
        elif checkUser == "usd":
            send_message(
                "Invite link already claimed.\n\n[Bangla] এই ট্রেডার আইডি দিয়ে অলরেডি VIP চ্যানেলে জয়েন করা হয়েছে",
                chat_id=chat_id,
            )
    else:
        send_message(
            "Invalid message. Type `/start` to start verification process",
            chat_id=chat_id,
        )


# abc
@app.route("/", methods=["GET", "POST"])
def bot_messages():
    if request.method == "POST":
        message = request.get_json()

        handle_message(message)

        return "OK", 200
    return "<h1>API ENDPOINT<h1>"


@app.route("/postback/quotex", methods=["GET", "POST"])
def handle_postback_quotex():
    if request.method == "POST":
        # Extract postback data
        postback_data = request.form.to_dict()
        # Example: Log postback data
        print("Received postback data from pocket option(quotex):", postback_data)
        if postback_data["a"] == POCKET_OPTION_ID:
            add_user(
                postback_data["trader_id"], "PocketOption", postback_data["sumdep"], conf=postback_data.get("conf", False)
            )
        else:
            print("Tracker ID doesnt match the referral link.")
        # Return a JSON response with status code 200
        return jsonify({"message": "Received postback data successfully"}), 200
    else:
        return "<h1>This is an API Endpoint<h1>"


@app.route("/postback/pocket", methods=["GET", "POST"])
def handle_postback_pocket():
    if request.method == "POST":
        # Extract postback data
        postback_data = request.form.to_dict()
        # Example: Log postback data
        print("Received postback data from pocket option:", postback_data)
        if postback_data["a"] == POCKET_OPTION_ID:
            add_user(
                postback_data["trader_id"], "PocketOption", postback_data["sumdep"], conf=postback_data.get("conf", False)
            )
        else:
            print("Tracker ID doesnt match the referral link.")
        # Return a JSON response with status code 200
        return jsonify({"message": "Received postback data successfully"}), 200
    else:
        return "<h1>This is an API Endpoint<h1>"


@app.route("/postback/binolla", methods=["GET", "POST"])
def handle_postback_binolla():
    if request.method == "POST":
        # Extract postback data
        postback_data = request.get_json()
        # Example: Log postback data
        print("Received postback data from binolla:", postback_data)
        if postback_data["lid"] == BINOLLA_ID:
            add_user(
                postback_data["uid"],
                "Binolla",
                deposit=postback_data["payout"],
                conf=postback_data.get("conf", False),
            )
        else:
            print("Tracker ID doesnt match the referral link.")
        # Return a JSON response with status code 200
        return jsonify({"message": "Received postback data successfully"}), 200
    else:
        return "<h1>This is an API Endpoint<h1>"


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT"))
