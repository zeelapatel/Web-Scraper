# import smtplib
# import ssl
# from email.message import EmailMessage

# # Define email sender and receiver
# email_sender = 'saiart2754@gmail.com'
# email_password = 'qisp rbww zthe igsn'
# email_receiver = 'zeelpatel2754@gmail.com'

# # Set the subject and body of the email
# subject = 'Check out my new video!'
# body = """
# I've just published a new video on YouTube: https://youtu.be/2cZzP9DLlkg
# """

# em = EmailMessage()
# em['From'] = email_sender
# em['To'] = email_receiver
# em['Subject'] = subject
# em.set_content(body)

# # Add SSL (layer of security)
# context = ssl.create_default_context()

# # Log in and send the email
# with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#     smtp.login(email_sender, email_password)
#     smtp.sendmail(email_sender, email_receiver, em.as_string())


# import win32com.client as win32
# olApp = win32.Dispatch('Outlook.Application')
# olNS = olApp.GetNameSpace('MAPI')
# for i in range(1):
#     mail_item = olApp.CreateItem(0)

#     mail_item.Subject = "Just Testing"
#     mail_item.BodyFormat = 1

#     mail_item.Body = "Hello, How are you? I am sending this email for testing purpose."
#     mail_item.Sender = "patel.zeel3@northeastern.edu"
#     mail_item.To = "zeelapatel2754@gmail.com"

#     mail_item.Display()
#     mail_item.Save()
#     mail_item.Send()

import win32com.client as win32

def send_email_to_recipients(subject, body, to_emails):
    olApp = win32.Dispatch('Outlook.Application')
    
    for email in to_emails:
        mail_item = olApp.CreateItem(0)  
        
        mail_item.Subject = subject
        mail_item.BodyFormat = 1  
        
        mail_item.Body = body
        mail_item.To = email
        
        mail_item.Send()

if __name__ == "__main__":
    subject = "Just Testing"
    body = "Hello, How are you? I am sending this email for testing purpose."
    to_emails = ["sanghavi.sp@northeastern.edu", "zeelapatel2754@gmail.com"]  # List of recipient emails
    
    send_email_to_recipients(subject, body, to_emails)
