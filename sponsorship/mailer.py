import datetime,time
import smtplib

from datetime import datetime
from datetime import date

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def smtp_connection():
    # CREDS
    SITE_ADDRESS = 'znet.social@gmail.com'
    PASSWORD = '*********'
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
   

def sender(username,email,action):
    # set up the SMTP server
    try:
        s = smtp_connection()
    except:
        print("Failed to connect to smtp...")
        time.sleep(600)
   
    # get message
    path = 'D:\\DEV\\task\\src\\sponsorship\\'
    if action == 'approved':
        message_template = read_template(path+'approved.txt') # reads message
    elif action =='sponsored':
        message_template = read_template(path+'sponsored.txt') # reads message
  
    # BEGIN EMAIL BODY
    msg = MIMEMultipart("alternative")       # create a message to client
   
    # add in the actual person name to the message template
    message = message_template.substitute(USERNAME=username)
    
    # Prints out the client message body for our sake
    # print(message)
    print("-----------------------------------------")

    # setup the parameters of the message to client
    msg['From'] = 'znet.social@outlook.com'
    msg['To'] = email
    if action == 'approved':
        msg['Subject'] = "Application approved"
    elif action =='sponsored':
        msg['Subject'] = "You have a sponsor"
    
    # add in the client message body
    msg.attach(MIMEText(message, 'html'))

    s.send_message(msg)
    del msg
    print("EMAIL RESET: ", email)

    # Terminate the SMTP session and close the connection
    s.quit()

