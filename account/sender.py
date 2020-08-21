import datetime,time
import smtplib

from datetime import datetime
from datetime import date

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



FIRST_RUN = 0
DATES = {}


def smtp_connection():
    # CREDS
    SITE_ADDRESS = 'znet.social@gmail.com'
    PASSWORD = 'login.gmail'
    # CONNECTION
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(SITE_ADDRESS, PASSWORD)
    return s


def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename ie message to client.
    """
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
        return Template(template_file_content)
   

def sender(username,email,code):
    # set up the SMTP server
    try:
        s = smtp_connection()
    except:
        s.quit()
        print("Failed to connect to smtp...")
        time.sleep(600)
   
    # get message
    path = 'D:\\DEV\\DFA\\jitunze\\src\\account\\'
    # path = '/home/znet/znet_app/my_project/account/'
    message_template = read_template(path+'message.txt') # reads message
  
    # BEGIN EMAIL BODY
    msg = MIMEMultipart("alternative")       # create a message to client
   
    # add in the actual person name to the message template
    message = message_template.substitute(USERNAME=username,EMAIL=email,CODE=code)
    
    # Prints out the client message body for our sake
    # print(message)
    print("-----------------------------------------")

    # setup the parameters of the message to client
    msg['From'] = 'znet.social@outlook.com'
    msg['To'] = email
    msg['Subject'] = "Reset your password"
    
    # add in the client message body
    msg.attach(MIMEText(message, 'html'))

    s.send_message(msg)
    del msg
    print("EMAIL RESET: ", email)

    # Terminate the SMTP session and close the connection
    s.quit()

