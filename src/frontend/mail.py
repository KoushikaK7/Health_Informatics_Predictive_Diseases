from flask import Flask, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route('/send_email', methods=['POST'])
def send_email():
    # Get form data
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']

    # Email configuration
    sender_email = 'your_email@example.com'  # Replace with your email address
    receiver_email = 'receiver_email@example.com'  # Replace with recipient's email address
    password = 'your_email_password'  # Replace with your email password

    # Create message
    msg = MIMEMultipart()
    msg['From'] = name
    msg['To'] = receiver_email
    msg['Subject'] = 'New Message from Contact Form'

    body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"
    msg.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server and send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        return 'Email sent successfully!'
    except Exception as e:
        return f'Failed to send email. Error: {str(e)}'

if __name__ == '__main__':
    app.run(host='localhost', port=5000)



