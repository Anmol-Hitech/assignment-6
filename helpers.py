import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
EMAIL_ADDRESS = "poojanppatel2005@gmail.com"
EMAIL_PASSWORD = "jbiltrjwrctuofll"  
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
def generate_otp():
    return random.randint(1000, 9999)

def send_otp_email(to_email: str,otp: int):
    subject = "Your OTP Verification Code"
    body = f"""
    Hello,
 
    Your OTP code is: {otp}
 
    Please use this to verify your account.
 
    Thank you!
    """
 
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
 
    msg.attach(MIMEText(body, "plain"))
 
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
    server.quit()

def correct_email(input:str):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.fullmatch(pattern, input):
        return True
    else:
        return False