# -*- coding:utf-8 -*-
from emails.EmailHelper import EmailHelper
from svn.SvnHelper import SvnHelper
from emails.EmailContent import _get_content_main_content
from fils.FileOprate import FileOprate
from configs.Config import CheckInTestConfig, project_name, EmailConfig

if __name__ == "__main__":
    # 获取svn日志
    svn = SvnHelper()
    fileOprate = FileOprate()

    start = fileOprate.get_datetime_sencond()
    log_version_start = svn.get_svn_version()
    log_version_stop = svn._get_svn_version_stop()
    svn_log = svn._get_svn_log(log_version_start, log_version_stop)
    project_verison = svn._get_svn_version_app()
    print "project version:", project_verison
    print "get svn log:", log_version_start, '-', log_version_start

    # 生成本地日志文件
    dir_svn_log = CheckInTestConfig.check_int_test_dir_log
    dir_pack = CheckInTestConfig.check_int_test_dir_pack
    dir_zip = CheckInTestConfig.check_int_test_dir_zip
    file_laster_name = project_name + "_" + project_verison + "_" + log_version_start + "_" + log_version_stop + "_" + fileOprate.get_datetime()

    txt_file_name = file_laster_name + ".txt"
    content = _get_content_main_content(svn_log, False)
    txt_svn_log_pack = dir_svn_log + txt_file_name
    fileOprate.save_result_from_txt(txt_svn_log_pack, content)

    txt_svn_log = dir_pack + txt_file_name
    fileOprate.save_result_from_txt(txt_svn_log, content)
    print "save svn log to txt:", txt_file_name

    emailHelper = EmailHelper(svn_log, project_verison)
    # 压缩打包文件
    if EmailConfig.have_email_attach_rar:
        zip_file_name = file_laster_name + ".zip"
        dir_zip = dir_zip + zip_file_name
        fileOprate.zip_dir(dir_pack, dir_zip)
        emailHelper.set_zippath(dir_zip)
        print "zip pack dir:", zip_file_name

    # 发送邮件
    success = emailHelper._send_email_msg()
    if success:
        print "send the email success..."
        fileOprate.delet_file_oprate(dir_pack)
        print "delete pack file..."
        svn.save_svn_version(log_version_stop)
        print "save svn version:", log_version_stop
    else:
        print "send the email fail"

    print "starts time:", start
    print "finish time:", fileOprate.get_datetime_sencond()
    raw_input("")
