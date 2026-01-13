import telebot
import json
import os
import re
import random
import string
from typing import Dict, List, Optional

# إعدادات البوت
TOKEN = '8554107823:AAG-YHE7DqNgAihEgRGYSiy0TL-S5QWmur4'  # توكن بوتك
ADMIN_ID = 1595285929  # ايدي المطور
ADMIN_USERNAME = 'NTBgg'  # معرف الادمن دون @
PROOF_CHANNEL_ID = '00'  # ايدي قناة الاثبات
PROOF_CHANNEL_USERNAME = '00'  # معرف قناة إثبات
SUDO_USERS = [ADMIN_ID, 000, 0000]  # ايدهات الادمن

bot = telebot.TeleBot(TOKEN)

# ملفات التخزين
SALES_FILE = 'sales.json'
AMR0_FILE = 'AMR0.txt'
AMR1_FILE = 'AMR1.txt'
USERS_FILE = 'AMR4.txt'
AMR_FILE = 'AMR.txt'
AMR3_FILE = 'AMR3.txt'

# تهيئة الملفات إذا لم تكن موجودة
def init_files():
    files_config = {
        SALES_FILE: {"sales": {}, "mode": None},
        AMR0_FILE: "",
        AMR1_FILE: "",
        USERS_FILE: "",
        AMR_FILE: "",
        AMR3_FILE: ""
    }
    
    for file, default_content in files_config.items():
        if not os.path.exists(file):
            if file.endswith('.json'):
                with open(file, 'w', encoding='utf-8') as f:
                    json.dump(default_content, f, ensure_ascii=False)
            else:
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(str(default_content))

# استدعاء تهيئة الملفات
init_files()

def load_sales() -> Dict:
    try:
        with open(SALES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"sales": {}, "mode": None}

def save_sales(data: Dict):
    with open(SALES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def read_file(filename: str) -> str:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except:
        return ""

def write_file(filename: str, content: str, append=False):
    mode = 'a' if append else 'w'
    with open(filename, mode, encoding='utf-8') as f:
        f.write(content + '\n' if append else content)

def get_users_list() -> List[str]:
    content = read_file(USERS_FILE)
    return [uid.strip() for uid in content.split('\n') if uid.strip()]

def add_user(user_id: int):
    users = get_users_list()
    if str(user_id) not in users:
        write_file(USERS_FILE, str(user_id), append=True)

def check_subscription(user_id: int) -> bool:
    """التحقق من اشتراك المستخدم في القنوات المطلوبة"""
    try:
        amr0_channel = read_file(AMR0_FILE)
        amr1_channel = read_file(AMR1_FILE)
        
        if amr0_channel:
            try:
                chat_member = bot.get_chat_member(amr0_channel, user_id)
                if chat_member.status in ['left', 'kicked']:
                    return False
            except Exception as e:
                print(f"Error checking channel 1: {e}")
                return False
        
        if amr1_channel:
            try:
                chat_member = bot.get_chat_member(amr1_channel, user_id)
                if chat_member.status in ['left', 'kicked']:
                    return False
            except Exception as e:
                print(f"Error checking channel 2: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"Error in subscription check: {e}")
        return True  # رجوعي للسماح بالدخول في حالة الخطأ

def create_admin_menu():
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        telebot.types.InlineKeyboardButton("قسم الاشتراك الاجباري ⚜️", callback_data="AMR78"),
        telebot.types.InlineKeyboardButton("قسم توجيه الرسائل من الاعضاء 🔙", callback_data="yfffgh"),
        telebot.types.InlineKeyboardButton("قسم الاذاعه 🎉", callback_data="6g77g"),
        telebot.types.InlineKeyboardButton("احصائيات البوت 👤", callback_data="AMR7"),
        telebot.types.InlineKeyboardButton("اعدادات البوت", callback_data="c")
    ]
    
    # إضافة الأزرار واحدة تلو الأخرى
    for button in buttons:
        markup.add(button)
    
    return markup

# أوامر البوت
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    add_user(user_id)
    
    # التحقق من الاشتراك الإجباري
    if not check_subscription(user_id):
        amr0_channel = read_file(AMR0_FILE)
        amr1_channel = read_file(AMR1_FILE)
        channels_text = ""
        if amr0_channel:
            channels_text += f"{amr0_channel}\n"
        if amr1_channel:
            channels_text += f"{amr1_channel}\n"
        
        bot.send_message(
            message.chat.id,
            f"عذراً عزيزي، يجب عليك الإشتراك في قنوات المطور أولاً ⚜️:\n\n{channels_text}\nاشترك ثم ارسل /start 📛!",
            parse_mode="HTML"
        )
        return
    
    sales = load_sales()
    if str(user_id) not in sales:
        sales[str(user_id)] = {"collect": 0}
        save_sales(sales)
    
    # إذا كان أدمن
    if user_id in SUDO_USERS:
        markup = create_admin_menu()
        bot.send_message(
            message.chat.id,
            "~ اهلا بك في لوحه الأدمن الخاصه بالبوت 🤖\n\n~ يمكنك التحكم في جميع اوامر البوت من هنا\n------------------------------------",
            reply_markup=markup
        )
        return
    
    # واجهة المستخدم العادي
    users_count = len(get_users_list())
    user_points = sales.get(str(user_id), {}).get("collect", 0)
    
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    
    # إنشاء الأزرار
    button1 = telebot.types.InlineKeyboardButton("• العروض التي يقدمها البوت ✨", callback_data="sales")
    button2 = telebot.types.InlineKeyboardButton("• تجميع النقاط 💸", callback_data="col")
    button3 = telebot.types.InlineKeyboardButton("• معلومات حسابك 🔍", callback_data="myacont")
    button4 = telebot.types.InlineKeyboardButton("• إثبات التسليم ⚖️", url=f"https://t.me/{PROOF_CHANNEL_USERNAME}")
    button5 = telebot.types.InlineKeyboardButton("• تابعنا 🧨", url="https://t.me/ali313eme")
    button6 = telebot.types.InlineKeyboardButton("• مطور البوت 👼", url=f"https://t.me/{ADMIN_USERNAME}")
    
    # إضافة الأزرار
    markup.add(button1, button2, button3, button4, button5, button6)
    
    bot.send_message(
        message.chat.id,
        f"""*اهلا بك في بوت الماركت 🌿🥸*

• يوجد بالبوت سلع مناسباً لك انشالله ✅
• شارك الرابط الخاص بك 🍂📮
• ثم خذ السلع التي تعجبك 🫀✨

مستخدمين البوت 👤🎩: *{users_count}*

*• عدد نقاطك ({user_points}) 🍂📮*""",
        parse_mode="Markdown",
        reply_markup=markup
    )

# معالجة Callback Queries
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    
    # التحقق من صلاحيات الأدمن
    is_admin = user_id in SUDO_USERS
    
    if call.data == "AMR" and is_admin:
        markup = create_admin_menu()
        bot.edit_message_text(
            "~ اهلا بك في لوحه الأدمن الخاصه بالبوت 🤖\n\n~ يمكنك التحكم في جميع اوامر البوت من هنا\n------------------------------------",
            chat_id,
            message_id,
            reply_markup=markup
        )
        write_file(AMR_FILE, "")
    
    elif call.data == "AMR78" and is_admin:
        markup = telebot.types.InlineKeyboardMarkup()
        
        # الصف الأول
        row1 = [
            telebot.types.InlineKeyboardButton("قناة ¹", callback_data="AMR765"),
            telebot.types.InlineKeyboardButton("قناة ²", callback_data="AMR907")
        ]
        
        # الصف الثاني
        row2 = [
            telebot.types.InlineKeyboardButton("عرض قنوات الإشتراك ★»", callback_data="AMR4")
        ]
        
        # الصف الثالث
        row3 = [
            telebot.types.InlineKeyboardButton("🔙", callback_data="AMR")
        ]
        
        markup.row(*row1)
        markup.row(*row2)
        markup.row(*row3)
        
        bot.edit_message_text(
            "*مرحبا بك في قسم الاشتراك الاجباري*🌟\nاختار القناة الذي تريد التحكم به 🇪🇬",
            chat_id,
            message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )
    
    elif call.data == "AMR765" and is_admin:
        markup = telebot.types.InlineKeyboardMarkup()
        
        # الصف الأول
        row1 = [
            telebot.types.InlineKeyboardButton("وضع قناة ➕", callback_data="AMR0"),
            telebot.types.InlineKeyboardButton("حذف قناة 📮", callback_data="delete11")
        ]
        
        # الصف الثاني
        row2 = [
            telebot.types.InlineKeyboardButton("عرض قناة ¹", callback_data="AMR987")
        ]
        
        # الصف الثالث
        row3 = [
            telebot.types.InlineKeyboardButton("🔙", callback_data="AMR")
        ]
        
        markup.row(*row1)
        markup.row(*row2)
        markup.row(*row3)
        
        bot.edit_message_text(
            "*مرحبا بك في التحكم ب قناة ¹*✨👇",
            chat_id,
            message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )
    
    elif call.data == "AMR0" and is_admin:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("🔙", callback_data="AMR"))
        
        bot.edit_message_text(
            "حسناً، الآن قم بإرسال معرف قناتك من ثم قم برفع البوت ادمن في القناة",
            chat_id,
            message_id,
            reply_markup=markup
        )
        write_file(AMR_FILE, "AMR0")
    
    elif call.data == "AMR987" and is_admin:
        amr0_channel = read_file(AMR0_FILE)
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("🔙", callback_data="AMR"))
        
        bot.edit_message_text(
            f"القناة => {amr0_channel} √",
            chat_id,
            message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )
    
    elif call.data == "delete11" and is_admin:
        markup = telebot.types.InlineKeyboardMarkup()
        row = [
            telebot.types.InlineKeyboardButton("لا ❎", callback_data="AMR"),
            telebot.types.InlineKeyboardButton("نعم ✅", callback_data="AMR1")
        ]
        markup.row(*row)
        
        bot.edit_message_text(
            "هل أنت متأكد من أنك تريد حذف القناة من الإشتراك الإجباري؟",
            chat_id,
            message_id,
            reply_markup=markup
        )
    
    elif call.data == "AMR1" and is_admin:
        write_file(AMR0_FILE, "")
        write_file(AMR_FILE, "")
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("🔙", callback_data="AMR"))
        
        bot.edit_message_text(
            "لقد تم حذف القناة من الإشتراك الإجباري بنجاح 📮",
            chat_id,
            message_id,
            reply_markup=markup
        )
    
    elif call.data == "AMR4" and is_admin:
        amr0_channel = read_file(AMR0_FILE)
        amr1_channel = read_file(AMR1_FILE)
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("🔙", callback_data="AMR"))
        
        bot.edit_message_text(
            f"""هلا بك عزيزي 
قنوات الاشتراك الاجباري
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــ
قناة ¹ => {amr0_channel} √
قناة ² => {amr1_channel} √
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــ""",
            chat_id,
            message_id,
            reply_markup=markup
        )
    
    elif call.data == "yfffgh" and is_admin:
        markup = telebot.types.InlineKeyboardMarkup()
        row = [
            telebot.types.InlineKeyboardButton("تفعيل التوجيه 🔙", callback_data="AMR11"),
            telebot.types.InlineKeyboardButton("قفل التوجيه ❎", callback_data="AMR12")
        ]
        markup.row(*row)
        
        bot.edit_message_text(
            "*اختار ماذا تريد الان 🖤*",
            chat_id,
            message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )
    
    elif call.data == "6g77g" and is_admin:
        markup = telebot.types.InlineKeyboardMarkup()
        row = [
            telebot.types.InlineKeyboardButton("إذاعة توجيه 🔄", callback_data="AMR5"),
            telebot.types.InlineKeyboardButton("إذاعة عامه 🔱", callback_data="AMR6")
        ]
        markup.row(*row)
        
        bot.edit_message_text(
            "*اختار نوع الاذاعه الان*",
            chat_id,
            message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )
    
    elif call.data == "AMR5" and is_admin:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("🔙", callback_data="AMR"))
        
        bot.edit_message_text(
            "قم برسال التوجيه الان 💚",
            chat_id,
            message_id,
            reply_markup=markup
        )
        write_file(AMR_FILE, "AMR2")
    
    elif call.data == "AMR6" and is_admin:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("🔙", callback_data="AMR"))
        
        bot.edit_message_text(
            "قم برسال المراد الاذاعه له الان 💛",
            chat_id,
            message_id,
            reply_markup=markup
        )
        write_file(AMR_FILE, "AMR3")
    
    elif call.data == "AMR7" and is_admin:
        users_count = len(get_users_list())
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("🔙", callback_data="AMR"))
        
        bot.edit_message_text(
            f"""هلا بك في قسم الاحصايات 💛
ــــــــــــــــــــ؍.َِ⇣𖤍🖤ء͡⇣ــــــــــــــــــ

 عدد مشتركين البوت  [ {users_count} ]

حاله سرعه البوت -: 100%
ــــــــــــــــــــ؍.َِ⇣𖤍🖤ء͡⇣ــــــــــــــــــ""",
            chat_id,
            message_id,
            reply_markup=markup
        )
        write_file(AMR_FILE, "")
    
    elif call.data == "AMR11" and is_admin:
        write_file(AMR3_FILE, "AMR")
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("🔙", callback_data="AMR"))
        
        bot.edit_message_text(
            "تم تنفيذ الامر ✅",
            chat_id,
            message_id,
            reply_markup=markup
        )
    
    elif call.data == "AMR12" and is_admin:
        write_file(AMR3_FILE, "")
        write_file(AMR_FILE, "")
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("🔙", callback_data="AMR"))
        
        bot.edit_message_text(
            "تم تنفيذ الامر ❎",
            chat_id,
            message_id,
            reply_markup=markup
        )
    
    elif call.data == "c" and is_admin:
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        
        # الصف الأول
        row1 = [
            telebot.types.InlineKeyboardButton("اضف سلعة 🔨", callback_data="add"),
            telebot.types.InlineKeyboardButton("حذف سلعة 🗑", callback_data="del")
        ]
        
        # الصف الثاني
        row2 = [
            telebot.types.InlineKeyboardButton("ارسال نقاط", callback_data="addcon"),
            telebot.types.InlineKeyboardButton("خصم نقاط", callback_data="delcon")
        ]
        
        # الصف الثالث
        row3 = [
            telebot.types.InlineKeyboardButton("رجوع", callback_data="AMR")
        ]
        
        markup.row(*row1)
        markup.row(*row2)
        markup.row(*row3)
        
        bot.edit_message_text(
            f"مرحباً عزيزي المطور (@{call.from_user.username}) 🔥.",
            chat_id,
            message_id,
            reply_markup=markup
        )
        sales = load_sales()
        sales["mode"] = None
        save_sales(sales)
    
    elif call.data == "add" and is_admin:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("الغاء 🚫", callback_data="c"))
        
        bot.edit_message_text(
            "قم بأرسال اسم السلعة 📬",
            chat_id,
            message_id,
            reply_markup=markup
        )
        sales = load_sales()
        sales["mode"] = "add"
        save_sales(sales)
    
    elif call.data == "del" and is_admin:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("الغاء 🚫", callback_data="c"))
        
        bot.edit_message_text(
            "قم بأرسال كود السلعة 📬",
            chat_id,
            message_id,
            reply_markup=markup
        )
        sales = load_sales()
        sales["mode"] = "del"
        save_sales(sales)
    
    elif call.data == "addcon" and is_admin:
        bot.edit_message_text(
            "أرسل أيدي الشخص الذي تريد إرسال النقاط له",
            chat_id,
            message_id
        )
        sales = load_sales()
        sales["mode"] = "chat"
        save_sales(sales)
    
    elif call.data == "delcon" and is_admin:
        bot.edit_message_text(
            "أرسل أيدي الشخص الذي تريد خصم النقاط منه",
            chat_id,
            message_id
        )
        sales = load_sales()
        sales["mode"] = "chat1"
        save_sales(sales)
    
    elif call.data == "bae":
        sales = load_sales()
        users_count = len(get_users_list())
        user_points = sales.get(str(user_id), {}).get("collect", 0)
        
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        
        # إنشاء الأزرار
        buttons = [
            telebot.types.InlineKeyboardButton("• العروض التي يقدمها البوت ✨", callback_data="sales"),
            telebot.types.InlineKeyboardButton("• تجميع النقاط 💸", callback_data="col"),
            telebot.types.InlineKeyboardButton("• معلومات حسابك 🔍", callback_data="myacont"),
            telebot.types.InlineKeyboardButton("• إثبات التسليم ⚖️", url=f"https://t.me/{PROOF_CHANNEL_USERNAME}"),
            telebot.types.InlineKeyboardButton("• تابعنا 🧨", url="https://t.me/amrakl"),
            telebot.types.InlineKeyboardButton("• مطور البوت 👼", url=f"https://t.me/{ADMIN_USERNAME}")
        ]
        
        for button in buttons:
            markup.add(button)
        
        bot.edit_message_text(
            f"""*اهلا بك في بوت الماركت 🌿🥸*

• يوجد بالبوت سلع مناسباً لك انشالله ✅
• شارك الرابط الخاص بك 🍂📮
• ثم خذ السلع التي تعجبك 🫀✨

مستخدمين البوت 👤🎩: *{users_count}*

*• عدد نقاطك ({user_points}) 🍂📮*""",
            chat_id,
            message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )
    
    elif call.data == "myacont":
        sales = load_sales()
        user_points = sales.get(str(user_id), {}).get("collect", 0)
        user = call.from_user
        
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("رجوع", callback_data="bae"))
        
        bot.edit_message_text(
            f"""*معلومات حسابك عزيزي*

اسمك: {user.first_name or ''} {user.last_name or ''}
معرفك: @{user.username if user.username else 'لا يوجد'}
ايدي: {user_id}
نقاطك: {user_points}""",
            chat_id,
            message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )
    
    elif call.data == "col":
        bot_username = bot.get_me().username
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("رجوع", callback_data="bae"))
        
        bot.edit_message_text(
            f"""*انسخ الرابط ثم قم بمشاركته مع اصدقائك 📥.*

• كل شخص يقوم بالدخول ستحصل على *1* نقطه

*- بإمكانك عمل اعلان خاص برابط الدعوة الخاص بك* 

~ رابط الدعوة: https://t.me/{bot_username}?start={user_id}""",
            chat_id,
            message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )
    
    elif call.data == "sales":
        sales_data = load_sales()
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        
        # رأس الجدول
        markup.row(
            telebot.types.InlineKeyboardButton("💵┇السعر", callback_data="s"),
            telebot.types.InlineKeyboardButton("ℹ️┇الاسم", callback_data="s")
        )
        
        # إضافة السلع
        for code, item in sales_data.get("sales", {}).items():
            markup.row(
                telebot.types.InlineKeyboardButton(str(item["price"]), callback_data=code),
                telebot.types.InlineKeyboardButton(item["name"], callback_data=code)
            )
        
        bot.edit_message_text(
            "العروض التي يقدمها البوت 🔥",
            chat_id,
            message_id,
            reply_markup=markup
        )
    
    elif call.data == "yes":
        sales = load_sales()
        if "mode" in sales and sales["mode"]:
            code = sales["mode"]
            item = sales["sales"].get(code)
            if item:
                user = call.from_user
                bot.edit_message_text(
                    f"تم ارسال طلبك لمالك البوت ✨\nقم بمراسلته لينفذ طلبك... @{ADMIN_USERNAME}",
                    chat_id,
                    message_id
                )
                try:
                    bot.send_message(
                        ADMIN_ID,
                        f"@{user.username if user.username else user.first_name}\n - قام بشراء {item['name']} بسعر {item['price']} 🧨"
                    )
                    bot.send_message(
                        PROOF_CHANNEL_ID,
                        f"""*قام البوت بتسليم طلب جديد* 
                        
*السلعة:* {item['name']}

*السعر:* {item['price']}

*العضو:* @{user.username if user.username else 'لا يوجد'}

*ايدي:* {user_id}""",
                        parse_mode="Markdown"
                    )
                    sales[str(user_id)]["collect"] -= item["price"]
                    sales["mode"] = None
                    save_sales(sales)
                except Exception as e:
                    print(f"Error in purchase: {e}")
    
    elif call.data != "s":  # إذا كان كود سلعة
        sales = load_sales()
        item = sales["sales"].get(call.data)
        if item:
            user_points = sales.get(str(user_id), {}).get("collect", 0)
            if user_points >= item["price"]:
                markup = telebot.types.InlineKeyboardMarkup()
                markup.row(
                    telebot.types.InlineKeyboardButton("نعم 🔥", callback_data="yes"),
                    telebot.types.InlineKeyboardButton("لا 🚫", callback_data="sales")
                )
                bot.edit_message_text(
                    f"هل انت متأكد من شراء {item['name']} بسعر {item['price']}؟ 🕸",
                    chat_id,
                    message_id,
                    reply_markup=markup
                )
                sales["mode"] = call.data
                save_sales(sales)
            else:
                bot.answer_callback_query(call.id, "ليس لديك نقاط كافية للشراء 🚫", show_alert=True)

# معالجة الرسائل النصية
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    text = message.text
    sales = load_sales()
    mode = sales.get("mode")
    amr_mode = read_file(AMR_FILE)
    
    # التحقق من الاشتراك الإجباري
    if not check_subscription(user_id) and text != "/start":
        amr0_channel = read_file(AMR0_FILE)
        amr1_channel = read_file(AMR1_FILE)
        channels_text = ""
        if amr0_channel:
            channels_text += f"{amr0_channel}\n"
        if amr1_channel:
            channels_text += f"{amr1_channel}\n"
        
        bot.send_message(
            message.chat.id,
            f"عذراً عزيزي، يجب عليك الإشتراك في قنوات المطور أولاً ⚜️:\n\n{channels_text}\nاشترك ثم ارسل /start 📛!",
            parse_mode="HTML"
        )
        return
    
    # معالجة أوضاع الأدمن
    if user_id in SUDO_USERS:
        if amr_mode == "AMR0" and user_id == ADMIN_ID:
            write_file(AMR0_FILE, text)
            write_file(AMR_FILE, "")
            markup = telebot.types.InlineKeyboardMarkup()
            markup.row(telebot.types.InlineKeyboardButton("🔙", callback_data="AMR"))
            
            bot.send_message(
                message.chat.id,
                "لقد تم وضع القناة بنجاح ✅",
                reply_markup=markup
            )
        
        elif amr_mode == "AMR2" and user_id == ADMIN_ID:
            users = get_users_list()
            success_count = 0
            for uid in users:
                try:
                    bot.forward_message(int(uid), user_id, message.message_id)
                    success_count += 1
                except Exception as e:
                    print(f"Error forwarding to {uid}: {e}")
                    continue
            
            markup = telebot.types.InlineKeyboardMarkup()
            markup.row(telebot.types.InlineKeyboardButton("🔙", callback_data="AMR"))
            
            bot.send_message(
                message.chat.id,
                f"تم توجيه الرسالة إلى {success_count} مستخدم",
                reply_markup=markup
            )
            write_file(AMR_FILE, "")
        
        elif amr_mode == "AMR3" and user_id == ADMIN_ID:
            users = get_users_list()
            success_count = 0
            for uid in users:
                try:
                    bot.send_message(int(uid), text)
                    success_count += 1
                except Exception as e:
                    print(f"Error broadcasting to {uid}: {e}")
                    continue
            
            markup = telebot.types.InlineKeyboardMarkup()
            markup.row(telebot.types.InlineKeyboardButton("🔙", callback_data="AMR"))
            
            bot.send_message(
                message.chat.id,
                f"تم النشر بنجاح إلى {success_count} مستخدم ✅",
                reply_markup=markup
            )
            write_file(AMR_FILE, "")
    
    # معالجة أوضاع الإدارة
    if mode == "add" and user_id in SUDO_USERS:
        sales["n"] = text
        sales["mode"] = "addm"
        save_sales(sales)
        bot.send_message(message.chat.id, "تم الحفظ ✅.\nالان ارسل عدد النقاط (السعر) المطلوبة للشراء 💸... رقم فقط")
    
    elif mode == "addm" and user_id in SUDO_USERS and text.isdigit():
        code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
        sales["sales"][code] = {
            "name": sales["n"],
            "price": int(text)
        }
        sales["n"] = None
        sales["mode"] = None
        save_sales(sales)
        bot.send_message(
            message.chat.id,
            f"""تم الحفظ السلعة ✅.
ℹ️┇الاسم: {sales['sales'][code]['name']}
💵┇السعر: {sales['sales'][code]['price']}
⛓┇كود السلعة: {code}"""
        )
    
    elif mode == "del" and user_id in SUDO_USERS:
        if text in sales["sales"]:
            item = sales["sales"].pop(text)
            sales["mode"] = None
            save_sales(sales)
            bot.send_message(
                message.chat.id,
                f"""تم حذف السلعة ✅.
ℹ️┇الاسم: {item['name']}
💵┇السعر: {item['price']}
⛓┇كود السلعة: {text}"""
            )
        else:
            bot.send_message(message.chat.id, "الكود الذي ارسلته غير موجود 🚫!")
    
    elif mode == "chat" and user_id in SUDO_USERS and text.isdigit():
        sales["idd"] = text
        sales["mode"] = "poi"
        save_sales(sales)
        bot.send_message(message.chat.id, "أرسل الكمية التي تريد إرسالها")
    
    elif mode == "poi" and user_id in SUDO_USERS and text.isdigit():
        amount = int(text)
        target_id = sales["idd"]
        
        # التأكد من وجود المستخدم في sales
        if target_id not in sales:
            sales[target_id] = {"collect": 0}
        
        sales[target_id]["collect"] = sales.get(target_id, {"collect": 0})["collect"] + amount
        sales["mode"] = None
        sales["idd"] = None
        save_sales(sales)
        
        bot.send_message(message.chat.id, f"تم إضافة {amount} نقطة إلى حساب {target_id} بنجاح")
        try:
            bot.send_message(int(target_id), f"تمت إضافة {amount} نقطة إلى حسابك في البوت من قبل المطور")
        except:
            pass
    
    elif mode == "chat1" and user_id in SUDO_USERS and text.isdigit():
        sales["idd"] = text
        sales["mode"] = "poi1"
        save_sales(sales)
        bot.send_message(message.chat.id, "أرسل الكمية التي تريد خصمها")
    
    elif mode == "poi1" and user_id in SUDO_USERS and text.isdigit():
        amount = int(text)
        target_id = sales["idd"]
        
        if target_id in sales:
            sales[target_id]["collect"] = max(0, sales[target_id].get("collect", 0) - amount)
        
        sales["mode"] = None
        sales["idd"] = None
        save_sales(sales)
        
        bot.send_message(message.chat.id, f"تم خصم {amount} نقطة من حساب {target_id} بنجاح")
        try:
            bot.send_message(int(target_id), f"تمت خصم {amount} نقطة من حسابك في البوت من قبل المطور")
        except:
            pass
    
    # توجيه الرسائل إذا كان التوجيه مفعلاً
    amr3_content = read_file(AMR3_FILE)
    if amr3_content == "AMR" and user_id != ADMIN_ID:
        try:
            bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        except Exception as e:
            print(f"Error forwarding message: {e}")

# تشغيل البوت
if __name__ == "__main__":
    print("Bot is running...")
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Error: {e}")
        bot.infinity_polling()