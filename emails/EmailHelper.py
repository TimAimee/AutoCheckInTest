# -*- coding:utf-8 -*-                                                  
import mimetypes
import os
import smtplib
from  email import Encoders
from  email import MIMEBase
from  email.header import Header
from email.mime.application import MIMEApplication
from  email.mime.multipart import MIMEMultipart
from  email.mime.text import MIMEText
from  email.utils import parseaddr, formataddr

from EmailContent import _get_msg_content_html
from configs.Config import EmailConfig
from configs.Config import EmailContentConfig
from configs.Config import CheckInTestConfig


class EmailHelper:
    """
    邮件相关的工具：https://docs.python.org/2/library/email-examples.html
    """
    project_version = ""
    svn_log = ""

    # smtp的服务器
    smtp_server = "smtp.faidns.com"
    # 发送人
    from_addr = EmailConfig.email_user_account
    # 密码
    password = EmailConfig.email_user_pwd
    # 接收人
    to_addr = EmailConfig.email_list_receiver
    # 抄送人
    cc_addr = EmailConfig.email_list_cardon_copy
    # 是否有附件zip
    have_attach_file_name_rar = EmailConfig.have_email_attach_rar
    # 附件zip的路径
    attach_file_name_zip = ""
    # 邮件标题
    _subject = EmailConfig.email_subject

    def __init__(self, svn_log, project_version):
        """
        EmailHelper的初使化

        :param svn_log: svn的log日志，[dict]类型
        :param project_version: project的版本
        """
        self.svn_log = svn_log
        self.project_version = project_version

    def set_zippath(self, path_zip):
        """
        设置附件zip的路径

        :param path_zip: 附件zip的路径
        :return: 无
        """
        self.attach_file_name_zip = path_zip

    def _get_subject(self):
        """
        获取subject

        :param svn_log: svn的log日志，[dict]类型
        :return: subject
        """
        content_head = self._subject.replace("%s", self.project_version)
        content = ""
        _firstly_log_item = self.svn_log['first']
        for i in range(0, len(_firstly_log_item)):
            content = content + _firstly_log_item[i] + ";"
        content = content_head + EmailContentConfig.content_first_log + content;
        return content

    def _format_addr(self, str):
        """
        格式化字符串

        :param str: 字符串
        :return: 格式化后字符串
        """
        name, addr = parseaddr(str)
        return formataddr(( \
            Header(name, 'utf-8').encode(), \
            addr.encode('utf-8') if isinstance(addr, unicode) else addr
        ))

    def _get_email_msg(self):
        """
        获取到msg对象

        :return: msg对象
        """
        msg = MIMEMultipart('mixed')
        content_html = self._get_email_msg_content_html()
        msg.attach(content_html)

        if self.have_attach_file_name_rar:
            attach_zip = self._get_email_attach_rar()
            msg.attach(attach_zip)

        subject = self._get_subject()
        msg['From'] = self._format_addr(u'Android <%s>' % self.from_addr)
        msg['To'] = ",".join(self.to_addr)
        msg['Cc'] = ",".join(self.cc_addr)
        msg['Subject'] = Header(subject, 'utf-8').encode()

        return msg

    def _send_email_msg(self):
        """
        发送邮件

        :return: 发送结果，True表示成功，False表示失败
        """

        try:
            msg = self._get_email_msg()
            server = smtplib.SMTP(self.smtp_server, 25)
            server.set_debuglevel(0)
            server.login(self.from_addr, self.password)
            server.sendmail(msg["From"], self.to_addr + self.cc_addr, msg.as_string())
            server.quit()
            return True
        except smtplib.SMTPException:
            return False

    def _get_email_msg_content_html(self):
        """
        获取到content的msg对象

        :return: content的msg对象
        """
        html = _get_msg_content_html(self.project_version, self.svn_log)
        msgHtml = MIMEText(html, 'html', 'utf-8')
        return msgHtml


    def _get_email_attach_rar(self):
        """
        获取到zip的msg对象

        :return: zip的msg对象
        """
        data = open(self.attach_file_name_zip, 'rb')
        ctype, encoding = mimetypes.guess_type(self.attach_file_name_zip)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)

        file_msg = MIMEBase.MIMEBase(maintype, subtype)
        file_msg.set_payload(data.read())
        data.close()

        # 把附件编码
        Encoders.encode_base64(file_msg)
        ## 设置附件头
        basename = os.path.basename(self.attach_file_name_zip)
        file_msg.add_header('Content-Disposition', 'attachment', filename=basename)  # 修改邮件头
        return file_msg

    def _save_oprate(self, stopversion):
        """
        获取成功后，将svn log日志的版本保存

        :param _check_int_text: svn log的最终路径
        :param stopversion: svn log的版本
        :return: 无返回
        """
        fo = open(CheckInTestConfig.check_int_text_svnversion, "w")
        fo.write(stopversion)
        fo.close()


if __name__ == "__main__":
    email_helper = EmailHelper("svn_log", "project_version")
    email_helper._send_email_msg()
