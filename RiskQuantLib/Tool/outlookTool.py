#!/usr/bin/python
#coding = utf-8

import os,re
from win32com import client as win32  # outlook control module
from win32com.client.gencache import EnsureDispatch as Dispatch  # read mail module
#<import>
#</import>

class readMailFromOutlook(object):
    """
    This class is used to control Outlook App in windows.
    Due to the difference of version of win32.com module, this class may not perform well.
    """
    def _saveMailAttachment(self,mailObject):
        # save all attachments in the mail
        attachment = mailObject.Attachments
        for each in attachment:
            save_attachment_path = os.getcwd()  # save files to current dictionary
            each.SaveAsFile(r'{}\{}'.format(save_attachment_path, each.FileName))
            print('Attachment（{}）Saved'.format(each.FileName))

    def _getMailAttr(self, mailObject, attrNameString):
        if hasattr(mailObject, attrNameString):
            return getattr(mailObject, attrNameString)
        else:
            return ''


    def _extractInfoFromMailsObject(self,mailsObject,mailIndex,saveAttachment = False, findAllLinks = True):
        resultDict = {}
        resultDict['mailIndex'] = mailIndex
        mail = mailsObject.Item(mailIndex)
        attrList = ['sender','receiver','CC','subject','content','numberOfAttachment','messageID','conversationTopic','conversationID','conversationIndex']
        attrNameList = ['SenderName','To','CC','Subject','Body','Attachments','EntryID','ConversationTopic','ConversationID','ConversationIndex']
        if hasattr(mail, 'receiveTime'):
            resultDict['receiveTime'] = str(mail.ReceivedTime)[:-6]
        else:
            resultDict['receiveTime'] = ''
        attrValueList = [self._getMailAttr(mail,j) for i,j in zip(attrList, attrNameList)]
        resultDict.update(dict(zip(attrList,attrValueList)))
        if saveAttachment:
            self._saveMailAttachment(mail)
        else:
            pass
        if findAllLinks:
            pattern = re.compile(r'<.*?>')
            resultDict['links'] = [i.strip(' ').strip('<').strip('>') for i in pattern.findall(resultDict['content'])]
            contentWithoutLink = pattern.sub('',resultDict['content'])
            pattern = re.compile(r' *[\t,\r]* *\n+')
            contentWithoutLink = re.sub(pattern,'\n', contentWithoutLink,count=0)
            pattern = re.compile(r'( *\t*)*\n+')
            resultDict['contentWithoutLink'] = re.sub(pattern,'\n', contentWithoutLink,count=0)
        return resultDict

    def readOutlookMailbox(self,numberOfReadingMails:int):
        """
        Connect to outlook, and read numberOfReadingMails mails in receive box.

        Parameters
        ----------
        numberOfReadingMails : int
            The number of mails you want to read.

        Returns
        -------
        result : dict
            A dict which contains information of mails. Key starts from 1.
        """
        # connect outlook with MAPI
        account = Dispatch('Outlook.Application').GetNamespace('MAPI')

        # get the position of receive box
        inbox = account.GetDefaultFolder(6)  # number 6 means receive box
        # get all mails in receive box
        mails = inbox.Items
        mails.Sort('[ReceivedTime]', True)  # sort mails by time

        # read all information of the first numberOfReadingMails mails（index start from 1）
        infoList = [self._extractInfoFromMailsObject(mails,i) for i in range(1,numberOfReadingMails+1)]
        result = dict(zip(range(1,numberOfReadingMails+1),infoList))
        self.mail = result
        return result

    #<readMailFromOutlook>
    #</readMailFromOutlook>

class sendMailFromOutlook(object):
    """
    This class is used to send mails by outlook.
    """
    def sendMail(self,receiverAddressList:list, subjectString:str, htmlBodyString:str, addAttachment:bool = False, attachmentFilePathString:str = ''):
        """
        Send mails by outlook
        """
        outlook = win32.Dispatch('Outlook.Application')  # connect outlook.

        mail_item = outlook.CreateItem(0)  # create a new mail
        [mail_item.Recipients.Add(i) for i in receiverAddressList]  # receiver
        mail_item.Subject = subjectString  # subject
        mail_item.BodyFormat = 2  # write content with html
        mail_item.HTMLBody = htmlBodyString
        if addAttachment:
            mail_item.Attachments.Add(attachmentFilePathString)  # add attachment
        else:
            pass
        mail_item.Send()  # send it.

    #<sendMailFromOutlook>
    #</sendMailFromOutlook>








