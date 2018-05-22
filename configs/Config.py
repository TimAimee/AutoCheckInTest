# -*- coding:utf-8 -*-
#自动提交的配置文件

from emails import EmailContact

# 自动提交的工作目录
checkintest_home = 'E:\\ExportProject\\App_SDK_Release\\xxx\\CheckInTest\\'

# winrar的安装路径
winrar_home = 'C:\\Program Files\\WinRAR\\'

# 项目svn的版本仓库
svn_url_pro_home = 'E:\\Android_Veepoo_SVN_Code\\xxx_android\\trunk\\xxx\\app'

# 项目名，最好不要带空格的命名
project_name = "HBand"


class CheckInTestConfig:
    """
    工作目录配置
    """
    # 临时要打包的文件
    check_int_test_dir_pack = checkintest_home + "pack"
    # 用于保存邮件提交时的更新txt日志
    check_int_test_dir_log = checkintest_home + "packtxt\\"
    # 用于保存邮件提交时的zip文件
    check_int_test_dir_zip = checkintest_home + "packzip\\"
    # 发送邮件时，底部个人签名要使用的图片
    check_int_test_img_logo = checkintest_home + "micon.jpg"
    # appversion.txt用来专门保存app的版本号
    check_int_text_appversion = checkintest_home + "project_version.txt"
    # logversion.txt用来专门保存上一次记录的版本号
    check_int_text_svnversion = checkintest_home + "svn_log_version.txt"


class EmailConfig:
    """
     邮箱配置
     """
    # 邮箱帐户
    email_user_account = EmailContact.app_android_ljl
    # 密码
    email_user_pwd = "123456"
    # 邮件标题 %s会替换成版本号
    email_subject = project_name + '_%s上线测试;'
    # 是否要发送zip附件
    have_email_attach_rar = True
    # 接收人 如 email_list_cardon_copy = [EmailContact.ljl_work_qq,EmailContact.sf_hjj]
    email_list_receiver = [EmailContact.ljl_work_qq]
    # 抄送人 如 email_list_cardon_copy = [EmailContact.ljl_work_qq,EmailContact.sf_hjj]
    email_list_cardon_copy = [EmailContact.ljl_work_qq]


class EmailContentConfig:
    """
     邮件内容配置
     """
    # commit提交时，提交的主要原因前面添加*
    _firstly_regex = "*"
    # commit提交时，主要更新内容前面添加~
    _secondly_regex = "~"
    # 邮件内容文本
    content_first_log = "提交的主要原因:"
    content_second_log = "主要更新内容:"
    # 邮件底部的名片
    email_footer_sign_name = 'timaimee'
    email_footer_sign_office = 'Android工程师'
    email_footer_sign_email = 'android1@veepoo.org'
