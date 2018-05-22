# -*- coding:utf-8 -*-
import time
import shutil
import os
import os.path
import zipfile
from configs.Config import *


class FileOprate:
    def get_result_from_txt(self, file_path):
        """
        获取文本的内容

        :param file_path: 文本的路径
        :return: 具体内容
        """
        fo = open(file_path, "r")
        result = fo.read().strip()
        fo.close()
        return result

    def save_result_from_txt(self, file_path, content):
        """
        保存内容到文本

        :param file_path: 文本的路径
        :param content: 文本的内容
        """
        fileObject = open(file_path.decode('utf-8'), 'w')
        fileObject.write(content)
        fileObject.close()

    def copy(self, dir_source, dir_target):
        """拷贝文件到另一个文件下

        :param file_path: 原路径
        :param new_file_path: 目的路径
        :return:
        """
        shutil.copy(dir_source, dir_target)

    def is_file(self, file_path):
        """当前路径是否为文件

        :param file_path: 文件路径
        :return: 是否为文件
        """
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                return False
            elif os.path.isfile(file_path):
                return True
            else:
                return False
        else:
            print "未知"
            return False
            raise

    def is_dictory(self, file_path):
        """当前路径是否为文件夹

        :param file_path: 文件路径
        :return: 是否为文件夹
        """
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                return True
            elif os.path.isfile(file_path):
                return False
            else:
                print "未知"
                return False
        else:
            print "文件夹不存在"
            raise

    def delet_file_oprate(self, file_path):
        """
        删除文件夹

        :param file_path: 文件路径
        """
        dir_list = os.listdir(file_path)
        for item_name in dir_list:
            item_path = os.path.join(file_path, item_name)
            os.remove(item_path)

    def create_dir(self, file_path):
        """
        创建文件夹

        :param file_path: 文件路径
        """
        if os.path.exists(file_path):
            pass
        else:
            os.mkdir(file_path)

    def get_datetime(self):
        """获得当前格式化的时间戳

        :return: 当前格式化的时间戳
        """
        now = int(time.time())
        timeStruct = time.localtime(now)
        # strTime = time.strftime("%Y%m%d%H%M%S", timeStruct)
        strTime = time.strftime("%Y%m%d", timeStruct)
        return strTime

    def get_datetime_sencond(self):
        """获得当前格式化的时间戳

        :return: 当前格式化的时间戳
        """
        now = int(time.time())
        timeStruct = time.localtime(now)
        strTime = time.strftime("%M:%S", timeStruct)
        return strTime

    def zip_dir(self, dirname, zipname):
        """压缩文件夹：
        http://www.cnblogs.com/pclook/archive/2009/05/06/1450539.html
        http://www.cnblogs.com/fetty/p/4769279.html

        :return:
        """
        os.chdir(winrar_home);
        winrar_cmd = 'winrar a -ep1 %s %s' % (zipname, dirname)
        os.system(winrar_cmd)


if __name__ == '__main__':
    pass
