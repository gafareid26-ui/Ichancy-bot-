import telebot
import sqlite3
import random
import threading
import time
import os
from telebot import types
from datetime import datetime

TOKEN = os.getenv("8234299846:AAGwgFJ0BaLRyUnObQCaX3t2kQcqXOjoED0")
if not TOKEN:
    print("ضع التوكن في Render Environment Variables!")
    exit()

bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect("ichancy.db", check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
             user_id INTEGER PRIMARY KEY,
             balance INTEGER DEFAULT 5000,
             daily TEXT,
             invites INTEGER DEFAULT 0)''')

c.execute('''CREATE TABLE IF NOT EXISTS jackpot (amount INTEGER DEFAULT 1000000)''')
c.execute('''INSERT OR IGNORE INTO jackpot(amount) VALUES (1000000)''')
conn.commit()

ADMIN_ID = 7939712752  # غيّر الرقم ده بـ ID بتاعك

def menu():
    k = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    k.add("الألعاب", "رصيدي")
    k.add("مكافأة يومية", "دعوة أصدقاء")
    k.add("الجاكبوت", "الإعدادات")
    return k

def get_balance(uid):
    c.execute("SELECT balance FROM users WHERE user_id=?", (uid,))
    r = c.fetchone()
    return r[0] if r else 0

def update_balance(uid, amount):
    c.execute("UPDATE users SET balance = balance + ? WHERE user_id=?", (amount, uid))
    conn.commit()

@bot.message_handler(commands=['start'])
def start(m):
    uid = m.from_user.id
    c.execute("INSERT OR IGNORE INTO users (user_id, balance) VALUES (?, 5000)", (uid,))
    conn.commit()

    if len(m.text.split()) > 1:
        try:
            ref = int(m.text.split()[1])
            if ref != uid:
                update_balance(ref, 2500)
                c.execute("UPDATE users SET invites = invites + 1 WHERE user_id=?", (ref,))
                conn.commit()
                bot.send_message(ref, "صديق جديد انضم برابطك! +2500 عملة")
        except:
            pass

    bot.send_message(m.chat.id, """
مرحباً في iChance Pro

هدية التسجيل: 5000 عملة
المكافأة اليومية: 3000 عملة
كل دعوة: 2500 عملة

ابدأ اللعب الآن!
    """, reply_markup=menu())

@bot.message_handler(func=lambda m: m.text == "رصيدي")
def bal(m):
    b = get_balance(m.from_user.id)
    c.execute("SELECT amount FROM jackpot")
    j = c.fetchone()[0]
    bot.send_message(m.chat.id, f"رصيدك: {b:,}\nالجاكبوت: {j:,}")

@bot.message_handler(func=lambda m: m.text == "مكافأة يومية")
def daily(m):
    uid = m.from_user.id
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT daily FROM users WHERE user_id=?", (uid,))
    last = c.fetchone()
    last = last[0] if last else None

    if last != today:
        update_balance(uid, 3000)
        c.execute("UPDATE users SET daily=? WHERE user_id=?", (today, uid))
        conn.commit()
        bot.send_message(m.chat.id, "تم استلام المكافأة اليومية! +3000")
    else:
        bot.send_message(m.chat.id, "خلّصت المكافأة اليومية، ارجع بكرة")

print("iChance Bot شغال...")
bot.infinity_polling()
