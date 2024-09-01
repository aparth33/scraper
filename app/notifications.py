import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from twilio.rest import Client
import requests

def send_email(subject, smtp_server, smtp_port, body, to_email, from_email, password):
    # Create the MIME object
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body to the MIME object
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the Gmail SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Start TLS encryption
        server.login(from_email, password)  # Log in to your Gmail account

        # Send the email
        server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()  # Terminate the SMTP session

def send_sms(body, to, from_, account_sid, auth_token):
    try:
        # Initialize the Twilio client
        client = Client(account_sid, auth_token)
        
        # Create and send the SMS message
        message = client.messages.create(
            body=body,
            from_=from_,
            to=to
        )
        
        # Print the SID of the sent message
        print(f"Message sent with SID: {message.sid}")
    
    except Exception as e:
        # Log or print the error if something goes wrong
        logging.error(f"Failed to send SMS: {e}")
        print(f"An error occurred: {e}")

def send_slack_notification(message, webhook_url):
    try:
        payload = {
            "text": message
        }
        
        # Send the POST request to Slack
        response = requests.post(webhook_url, json=payload)
        
        # Check if the request was successful
        if response.status_code != 200:
            raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")
        
        print("Notification sent successfully.")
    
    except requests.exceptions.RequestException as e:
        # Handle any exception that occurs during the request
        logging.error(f"An error occurred while sending the Slack notification: {e}")
        print(f"Failed to send Slack notification: {e}")


def notify(message: str):
    print(message)
    from_email=os.getenv('FROM_EMAIL')
    password=os.getenv('APP_PASSWORD')
    account_sid=os.getenv('TWILIO_ACCOUNT_SID')
    auth_token=os.getenv('TWILIO_AUTH_TOKEN')
    webhook_url=os.getenv('SLACK_WEBHOOK_URL')
    
    # Use email
    if len(from_email)>0 and len(password)>0:    
        send_email(
            subject="Scraping Notification",
            smtp_server = os.getenv('SMTP_SERVER'),
            smtp_port = os.getenv('SMTP_PORT'),
            body=message,
            from_email=from_email,
            to_email="aparth33@yahoo.co.in",
            password=password
        )

    # Use SMS
    if len(account_sid)>0 and len(auth_token)>0:
        send_sms(
            body=message,
            to="+1234567890",
            from_=os.getenv('FROM_SEND_SMS'),
            account_sid=account_sid,
            auth_token=auth_token
        )

    # Use Slack
    if len(webhook_url)>0:
        send_slack_notification(
        message=message,
        webhook_url=webhook_url
        )
