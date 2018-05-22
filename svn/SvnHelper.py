# -*- coding:utf-8 -*-
import os

from configs.Config import *
from fils.FileOprate import FileOprate


class SvnHelper:
    def save_svn_version(self, stop_svn_version):
        """
        保存svn的版本

        :param stop_svn_version: 结果的svn log版本
        """
        fileOprate = FileOprate()
        fileOprate.save_result_from_txt(CheckInTestConfig.check_int_text_svnversion, stop_svn_version)

    def get_svn_version(self):
        """
        从本地获取上一次的svn log版本

        :param _check_int_text: 获取的目录
        :return: 返回log版本号
        """
        fileOprate = FileOprate()
        result = fileOprate.get_result_from_txt(CheckInTestConfig.check_int_text_svnversion)
        return result

    def _get_svn_version_app(self):
        """
        获取app版本

        :param _check_int_text: 获取的目录
        :return: 返回app版本
        """
        fileOprate = FileOprate()
        result = fileOprate.get_result_from_txt(CheckInTestConfig.check_int_text_appversion)
        return result

    def _get_svn_version_stop(self):
        """
        获取最新的log版本：http://svnbook.red-bean.com/en/1.7/svn.ref.svn.c.info.html

        :return:最新的log版本
        """
        t = os.popen('svn info -r head %s' %svn_url_pro_home)
        result = t.read()
        max_version = self._get_max_svn_version(result)
        return max_version;

    def _get_max_svn_version(self, result):
        """
        通过svn命令获取最新log的版本号

        :param result:svn执行完命令后的结果
        :return: 最新log的版本号
        """
        _log_array = result.split("\n")
        max_version = 0
        for i in range(0, len(_log_array)):
            _log_item = _log_array[i]
            if "Revision" in _log_item:
                max_version = _log_item.split(":")[1].strip()
                # print max_version
                break;
        return max_version;

    def _get_svn_log(self, _log_version_start, _log_version_stop):
        """
        获取svn的log日志：
        https://blog.csdn.net/gengxiaoming7/article/details/50518877
        http://svnbook.red-bean.com/en/1.7/svn.ref.svn.c.log.html

        :param _log_version_start: 开始的版本号
        :param _log_version_stop: 结束的版本号
        :return: svn执行完命令后的结果
        """
        _cmd_svn_log = 'svn log -r %s:%s %s' % (_log_version_start, _log_version_stop, svn_url_pro_home)
        # print _cmd_svn_log
        t = os.popen(_cmd_svn_log)
        result = t.read()
        result = self._get_svn_log_commit(result)
        # print result
        return result

    def _get_svn_log_commit(self, result):
        """
        处理成我们想要的svn log格式,**开头表示主要更新内容,*表示次要更新内容

        :param result: svn的log日志
        :return: svn执行完命令后的结果
        """
        _log_array = result.split("\n")

        _firstly_log_item = []
        _secondly_log_item = []

        for i in range(0, len(_log_array)):
            _log_item = _log_array[i]
            _log_item = _log_item.decode('gbk').encode('utf-8')
            if "--------" in _log_item:
                pass
            elif len(_log_item) == 0:
                pass
            elif "|" in _log_item:
                pass
            elif EmailContentConfig._firstly_regex in _log_item:
                # 主要更新内容
                _log_item = _log_item.replace(EmailContentConfig._firstly_regex, "")
                _firstly_log_item.append(_log_item)
            elif EmailContentConfig._secondly_regex in _log_item:
                _log_item = _log_item.replace(EmailContentConfig._secondly_regex, "")
                _secondly_log_item.append(_log_item)
                # 次要更新内容
            else:
                # print _log_item
                pass
        dict = {"first": _firstly_log_item, "second": _secondly_log_item}
        return dict


if __name__ == "__main__":
    svn = SvnHelper()
    log_version_start = svn.get_svn_version()
    log_version_stop = svn._get_svn_version_stop()
    log_version_start, "-", log_version_stop
    svn._get_svn_log(log_version_start, log_version_stop)
    
