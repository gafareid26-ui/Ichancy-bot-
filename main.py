import telebot
import sqlite3
import random
import threading
import time
import os
from telebot import types
from datetime import datetime, timedelta

# التوكن من Render (آمن 100%)
TOKEN = os.getenv("8234299846:AAGwgFJ0BaLRyUnObQCaX3t2kQcqXOjoED0")
if not TOKEN:
    print("8234299846:AAGwgFJ0BaLRyUnObQCaX3t2kQcqXOjoED0")
    exit()

bot = telebot.TeleBot(TOKEN)

# قاعدة البيانات
conn = sqlite3.connect("ichancy.db", check_same_thread=False)
c = conn.cursor()

# الجداول
c.execute('''CREATE TABLE IF NOT EXISTS users (
             user_id INTEGER PRIMARY KEY,
             balance INTEGER DEFAULT 5000,
             daily TEXT,
             invites INTEGER DEFAULT 0,
             vip INTEGER DEFAULT 0,
             total_bet INTEGER DEFAULT 0)''')

c.execute('''CREATE TABLE IF NOT EXISTS jackpot (amount INTEGER DEFAULT 1000000)''')
c.execute('''INSERT OR IGNORE INTO jackpot(amount) VALUES (1000000)''')
conn.commit()

# غيّر الرقم ده بـ ID بتاعك (هتعرفه من @userinfobot)
ADMIN_ID = 7939712752  # ←←← غيّره حالا !!

# زيادة الجاكبوت تلقائي
def jackpot_loop():
    while True:
        time.sleep(600)  # كل 10 دقايق
        c.execute("UPDATE jackpot SET amount = amount + 15000")
        conn.commit()
threading.Thread(target=jackpot_loop, daemon=True).start()

# القائمة الرئيسية
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🎰 الألعاب", "💰 رصيدي")
    markup.add("🎁 مكافأة يومية", "👥 دعوة أصدقاء")
    markup.add("🏆 الجاكبوت", "⚙️ الإعدادات")
    return markup

# الألعاب
def games_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🎰 روليت", callback_data="roulette"),
        types.InlineKeyboardButton("🎰
