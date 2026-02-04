import smtplib
from email.message import EmailMessage
import time
import threading
from flask import Flask, render_template, request

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
            time.sleep(9.6) # 25 emails in 4 minutes gap
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
    
    # Cleaning the emails list to remove New Lines/Enters
    clients_raw = request.form.get('clients')
    # Enter ko comma mein badla, phir split kiya, phir extra spaces hataye
    client_list = [c.strip() for c in clients_raw.replace('\n', ',').split(',') if c.strip()]

    thread = threading.Thread(target=send_mail_logic, args=(user_email, app_password, subject, message, client_list))
    thread.start()

    return "🚀 Processing... Check your VS Code terminal (or Render Logs) to see progress!"

if __name__ == '__main__':
    app.run(debug=True)