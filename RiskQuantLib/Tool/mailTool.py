#!/usr/bin/python
#coding = utf-8

from imapclient import IMAPClient
from redmail import EmailSender
import email
from email.policy import default

#<import>
#</import>


class mailConnector(object):
    """This is the basic connector of mail service."""
    def __init__(self, hostIMAP: str, hostSMTP: str, userName: str, password: str, portSMTP: int = 25):
        self.userName = userName
        self.password = password
        self.sender = EmailSender(host=hostSMTP, port=portSMTP, username=userName, password=password)
        self.imap_host = hostIMAP

    def receive(self, number: int = 5, folder: str = 'INBOX', message: str = 'ALL'):
        """This function is used to search mailbox and get the latest n mails, it returns html string."""
        with IMAPClient(self.imap_host, ssl=True) as client:
            client.login(self.userName, self.password)
            client.select_folder(folder)
            messages = client.search([message])
            results = []
            for msg_id, data in client.fetch(messages[-number:], ['RFC822']).items():
                msg = email.message_from_bytes(data[b'RFC822'], policy=default)
                results.append({
                    "subject": msg['subject'],
                    "sender": msg['from'],
                    "body": msg.get_body(preferencelist=('plain', 'html')).get_content()
                })
            return results

    def send(self, to: list, subject: str, content: str, html: bool = False):
        """This function will send mails to a list of users. You can pass html string or pure string to it."""
        self.sender.send(receivers=to,subject=subject,html=content) if html else self.sender.send(receivers=to,subject=subject,text=content)

    #<mailConnector>
    #</mailConnector>

#<mailTool>
#</mailTool>
