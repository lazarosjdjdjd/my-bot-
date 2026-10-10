import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# Το Token σας από τον BotFather
TOKEN = 8820635848:AAGUh41z1M9IBsMdxt57bke5PSgeWztLxNo

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Γεια! Το bot σου τρέχει μόνιμα στο Cloud!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Απάντηση: {update.message.text}")

# Server για να κρατάει το Render το bot "ζωντανό"
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

def main():
    # Εκκίνηση του web server σε ξεχωριστό thread
    threading.Thread(target=run_health_server, daemon=True).start()
    
    # Εκκίνηση του Telegram Bot
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    print("Το bot ξεκίνησε...")
    app.run_polling()

if __name__ == "__main__":
   
  main()
