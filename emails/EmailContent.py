# -*- coding:utf-8 -*-
from  configs.Config import EmailContentConfig
from  configs.Config import CheckInTestConfig
from emails.EmailContact import nick_name_test_1_rcl

tab_2 = "<br>"
tab_3n = "<br>&emsp;"
tab_4n = "<br>&emsp;&emsp;"
tab_3n_txt = "\n"
tab_4n_txt = "\n\t"


def _get_msg_content(project_version, svn_log):
    """
    获取邮件的具体内容

    :param project_version: project 的版本
    :param svn_log: svn的log日志，[dict]类型
    :return: 具体内容
    """
    content = []
    content.append(tab_2)
    content.append(nick_name_test_1_rcl + "：")
    content.append(tab_3n)
    content.append("你好！现提交%s进行测试，本部门内部测试完毕，现提交给测试部门。%s" % (project_version, _get_content_main_content(svn_log, True)))
    content.append(tab_3n)
    content.append("此版本要进行全面测试，测试完毕后发布到市场供用户下载。")
    content.append(tab_3n)
    content.append("注意:此邮件是由自动化的工具发出，工具还在试用完善当中，如果存在问题，敬请包涵....")
    content.append(tab_3n)
    content.append("----------------------")
    # content.append(_get_content_footer())
    content_join = "".join(content)
    return content_join


def _get_content_main_content(svn_log, ishtml):
    """
    获得svn格式化后的内容

    :param svn_log: svn的log日志，[dict]类型
    :param ishtml: 内容的表示有两种，一种是html；另一种是txt
    :return: svn格式化后的内容
    """
    content = []
    _firstly_log_item = svn_log['first']
    _secondly_log_item = svn_log['second']
    if ishtml:
        content.append(tab_3n)
    else:
        # content.append(tab_3n_txt)
        pass
    content.append(EmailContentConfig.content_first_log)
    content.append(get_content_block(_firstly_log_item, ishtml))
    if ishtml:
        content.append(tab_3n)
    else:
        content.append(tab_3n_txt)
    content.append(EmailContentConfig.content_second_log)
    content.append(get_content_block(_secondly_log_item, ishtml))
    return "".join(content)


def get_content_block(_log_list, ishtml):
    """
    主要提交原因&&主要更新内容的排版

    :param _log_list: 日志列表
    :param ishtml:  是否返回html格式，否的话为txt格式
    :return: 内容的排版
    """
    content = []
    for i in range(0, len(_log_list)):
        if ishtml:
            content.append(tab_4n)
        else:
            content.append(tab_4n_txt)
        content.append(str(i + 1) + "、" + _log_list[i])
    return "".join(content)


def _get_msg_content_html(project_version, svn_log):
    """
     获取发送邮件时要加载到msg对象下的content：http://www.w3school.com.cn/html/index.asp

    :param project_version: project的版本
    :param svn_log: svn的log日志，[dict]类型
    :return: 返回content
    """
    content = _get_msg_content(project_version, svn_log)
    data_uri = open(CheckInTestConfig.check_int_test_img_logo, 'rb').read().encode('base64').replace('\n', '')
    img_tag = '<img src="data:image/png;base64,%s">' % data_uri
    html = """    
    <html>
      <head></head>
      <body>
        <p>
            %s
        </p>
        <p style="font-family:微软雅黑" >
            <font  size="2" color="#877c7b">
                <strong>Best Regards<br>
                  %s|%s<br>
                  深圳市维亿魄科技有限公司<br>
                 </strong>
            </font> 
        </p>
		<p style="font-family:微软雅黑">
            <font size="2" color="#0092e7">M</font><font size="2" color="#7f7f7f">: 0755-86713056</font> | 
            <font size="2" color="#0092e7">T</font><font size="2" color="#7f7f7f">: 0755-86543281</font><br>
            <font size="2" color="#0092e7">E</font><font size="2" color="#2e7aac"><strong>: %s</strong></font> | 
            <font size="2" color="#0092e7">W</font><font size="2" color="#2e7aac"><strong>: www.veepoo.cn</strong></font><br>
            <font size="2" color="#7f7f7f">深圳市南山区科技园科苑路15号科兴科学园A1栋505</font><br>
        %s
        </p>
      </body>
    </html>
    """ % (content, EmailContentConfig.email_footer_sign_name, EmailContentConfig.email_footer_sign_office,
           EmailContentConfig.email_footer_sign_email, img_tag)
    return html


if __name__ == "__main__":
    pass
