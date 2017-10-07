import sys
import datetime
import email
import imaplib
import mailbox
import time
from subprocess import call
import os

while(1):

    EMAIL_ACCOUNT = ""
    PASSWORD = ""

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    mail.list()
    mail.select('inbox')



    result, data = mail.uid('search', None, "UNSEEN") # (ALL/UNSEEN)
    #print(data[0].split())
    i = len(data[0].split())


    for x in (range(i-1,-1,-1)):
        latest_email_uid = (data[0].split()[x])
        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        # result, email_data = conn.store(num,'-FLAGS','\\Seen') 
        # this might work to set flag to seen, if it doesn't already
        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)


        date_tuple = email.utils.parsedate_tz(email_message['Date'])
        #print(date_tuple)
    
        if time.strftime("%Y-%m-%d %H:%M:%S", date_tuple[:-1]) > str(datetime.datetime.now() - datetime.timedelta(days=1)):
            print(time.strftime("%Y-%m-%d %H:%M:%S", date_tuple[:-1]),'>',str(datetime.datetime.now() - datetime.timedelta(days=1)))
        
            if date_tuple:
                local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                local_message_date = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
            email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
            email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
            subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
            Email_From = email_from[:email_from.index('<') - 1]
        
        
            #speech = Email_From
            #call(["espeak",'You got a mail from'+speech])
            print(Email_From)
            print(Email_subject)
            s = "New mail from " + Email_From 
       
            read_text='"{}"'.format(s)
            speech ="espeak -s 125 -v en+f5 " +  read_text
            os.system(speech)    

    time.sleep(10)

