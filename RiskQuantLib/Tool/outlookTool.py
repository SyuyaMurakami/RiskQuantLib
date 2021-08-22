#!/usr/bin/python
#coding = utf-8


import os,re
from win32com import client as win32  # 发送邮件模块
from win32com.client.gencache import EnsureDispatch as Dispatch  # 读取邮件模块

class readMailFromOutlook():

    def _saveMailAttachment(self,mailObject):
        # 保存邮件中的附件，如果没有附件不会执行也不会产生异常
        attachment = mailObject.Attachments
        for each in attachment:
            save_attachment_path = os.getcwd()  # 保存附件到当前路径
            each.SaveAsFile(r'{}\{}'.format(save_attachment_path, each.FileName))
            print('附件（{}）保存完毕'.format(each.FileName))

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

    def readOutlookMailbox(self,numberOfReadingMails):

        """连接Outlook邮箱，读取收件箱内的邮件内容"""
        # 使用MAPI协议连接Outlook
        account = Dispatch('Outlook.Application').GetNamespace('MAPI')

        # 获取收件箱所在位置
        inbox = account.GetDefaultFolder(6)  # 数字6代表收件箱
        # 获取收件箱下的所有邮件
        mails = inbox.Items
        mails.Sort('[ReceivedTime]', True)  # 邮件按时间排序

        # 读取收件箱内前3封邮件的所有信息（下标从1开始）
        infoList = [self._extractInfoFromMailsObject(mails,i) for i in range(1,numberOfReadingMails+1)]
        result = dict(zip(range(1,numberOfReadingMails+1),infoList))
        self.mail = result
        return result

class sendMailFromOutlook():

    def sendMail(self,receiverAddressList, subjectString, htmlBodyString, addAttachment = False, attachmentFilePathString = ''):
        """
        连接Outlook邮箱，发送邮件
        :return:
        """
        outlook = win32.Dispatch('Outlook.Application')  # 连接Outlook

        mail_item = outlook.CreateItem(0)  # 创建新邮件
        [mail_item.Recipients.Add(i) for i in receiverAddressList]  # 收件人邮箱
        mail_item.Subject = subjectString  # 主题
        mail_item.BodyFormat = 2  # 使用HTML格式编写正文
        mail_item.HTMLBody = htmlBodyString
        if addAttachment:
            mail_item.Attachments.Add(attachmentFilePathString)  # 添加附件
        else:
            pass
        mail_item.Send()  # 发送邮件










