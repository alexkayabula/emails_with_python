import imaplib
import email
from email.header import decode_header
import webbrowser
import os

# set your account credentials(Service email)
username = "YOUR EMAIL"
password = "YOUR PASSWORD"

# create an IMAP4 class with SSL
imap = imaplib.IMAP4_SSL("imap.gmail.com")
# authenticate
imap.login(username, password)


status, messages = imap.select("INBOX")

# number of top emails to fetch
N = 12
# total number of emails
messages = int(messages[0])


for i in range(messages, messages-N, -1):
    # fetch the email message by ID
    res, msg = imap.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            # parse a bytes email into a message object
            msg = email.message_from_bytes(response[1])
            # decode the email subject
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                # if it's a bytes, decode to str
                subject = subject.decode()
            # email sender
            from_ = msg.get("From")
            # extract content type of email
            content_type = msg.get_content_type()

            if content_type == "text/plain":
                # get the email body
                body = msg.get_payload(decode=True).decode()
                # print only text email parts
                print("Subject:", subject)
                print("From:", from_)
                print(body)
                print("="*100)

            # if the email message is multipart
            if msg.is_multipart():
                # iterate over email parts
                for part in msg.walk():
                    # extract content type of email
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        # get the email body
                        body = part.get_payload(decode=True).decode()
                        # print only text email parts
                        print("Subject:", subject)
                        print("From:", from_)
                        print(body)
                        print("="*100)
imap.close()
imap.logout()
