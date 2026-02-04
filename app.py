import smtplib
from email.message import EmailMessage
import time
import threading
import os
import sys
import webbrowser
from threading import Timer
from flask import Flask, render_template, request

# PyInstaller ke liye templates folder ka path handle karne ka logic
if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    app = Flask(__name__, template_folder=template_folder)
else:
    app = Flask(__name__)

def send_mail_logic(user_email, app_password, subject, message, client_list):
    for client in client_list:
        client = client.strip()
        if not client: continue
        try:
            msg = EmailMessage()
            msg.set_content(message)
            msg['Subject'] = subject
            msg['From'] = user_email
            msg['To'] = client

            # Port 587 and TLS for Local & Cloud (Render)
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(user_email, app_password)
                server.send_message(msg)
            
            print(f"✅ Success: Sent to {client}")
            time.sleep(9.6) # Anti-spam delay
        except Exception as e:
            print(f"❌ Error for {client}: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    user_email = request.form.get('email')
    app_password = request.form.get('password')
    subject = request.form.get('subject')
    message = request.form.get('message')
    
    # Cleaning the emails list
    clients_raw = request.form.get('clients')
    client_list = [c.strip() for c in clients_raw.replace('\n', ',').split(',') if c.strip()]

    thread = threading.Thread(target=send_mail_logic, args=(user_email, app_password, subject, message, client_list))
    thread.start()

    return "🚀 Emails are being sent! You can close this tab, but keep the application running."

def open_browser():
    """App start hote hi automatically browser mein page khol dega"""
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    # Server start hone ke 1.5 second baad browser khulega
    Timer(1.5, open_browser).start()
    # Debug=False executable ke liye better hota hai
    app.run(port=5000, debug=False)
