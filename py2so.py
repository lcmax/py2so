#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  toolkit to compile a python project into dynamic link library files

  Author: wangleyi
  Email: wangleyi@baidu.com
  File:  py2so.py
  Date: 2019-02-27 14:06
"""
import os
import re
import shutil
from distutils.core import setup, Extension
from optparse import OptionParser

from Cython.Build import cythonize
from Cython.Distutils import build_ext


class Py2so(object):
    """
    Compiling Python files into dynamic link library files
    """
    # directories that do not need to be copied
    exclude_dirs = ['.git', '__pycache__']
    # files that do not need to be copied
    exclude_files = ["setup.py", "py2so.py", ".gitignore"]
    # scripts that do not need to compile
    not_complie_files = ["gunicorn_config.py"]

    def __init__(self, language=2, filename=None):
        """

        :param language: int, python language version, 2 or 3
        :param filename: str, file path need to compile
        """
        if language not in [2, 3]:
            raise ValueError("The input language parameter is invalid!")
        self.language = language
        if filename:
            if os.path.isdir(filename):
                raise ValueError("The input file parameter should not be a directory!")
            elif not os.path.exists(filename):
                raise ValueError("The input file to compile is not exist!")
            self.package_path = os.path.dirname(filename)
            self.fname_list = [filename]
        else:
            self.package_path = "."
            self.fname_list = self.get_file_list(self.package_path)
        self.build_path_dir = os.path.join(self.package_path, "build")
        self.tmp_path_dir = os.path.join(self.build_path_dir, "tmp")

    @classmethod
    def get_file_list(cls, dir_path):
        """
        get the path of all files under the input folder
        :param dir_path: str, input folder name
        :return: list, file path list
        """
        file_path_list = []
        if not os.path.exists(dir_path):
            raise IOError("The input module path invalid! please check the input parameters")

        for root, dirs, files in os.walk(dir_path):
            files[:] = [_file for _file in files if _file not in cls.exclude_files]
            dirs[:] = [_dir for _dir in dirs if _dir not in cls.exclude_dirs]
            curr_file_list = list(map(lambda x: os.path.join(root, x), files))
            file_path_list.extend(curr_file_list)
        return file_path_list

    @classmethod
    def is_valid_file(cls, fname_path):
        """
        judge whether the input file is valid
        :param fname_path: str, the input file path
        :return:
        """
        file_name = os.path.split(fname_path)[1]
        file_format = os.path.splitext(fname_path)[1]
        if file_format in [".py", ".pyx"] and not file_name.startswith("__") \
                and file_name not in cls.not_complie_files:
            return True
        else:
            return False

    def clean_tmp_files(self, modules_list, obj=True, c=True):
        """
        clean the tmp files
        :param modules_list: list, the models list
        :param obj: bool, whether removing the object files
        :param c: bool, whether removing the '.c' files
        """
        if obj:
            shutil.rmtree(self.tmp_path_dir)
        if c:
            c_list = map(lambda x: os.path.splitext(x)[0] + ".c", modules_list)
            for filename in c_list:
                os.remove(filename)

    def copy_other_files(self, file_list):
        """
        copy resource files
        :param file_list: list, file_list
        """
        rel_start_idx = len(self.package_path) + 1
        pack_dir = os.path.split(os.path.dirname(os.path.abspath(__file__)))[-1]
        if os.path.exists("__init__.py"):
            obj_path_list = map(lambda x: os.path.join(self.build_path_dir, pack_dir, x[rel_start_idx:]),
                                file_list)
        else:
            obj_path_list = map(lambda x: os.path.join(self.build_path_dir, x[rel_start_idx:]),
                                file_list)
        for src, des in zip(file_list, obj_path_list):
            dir_name = os.path.dirname(des)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            shutil.copy(src, des)

    def rename(self):
        """
        rename the dynamic link library files
        """
        fname_list = self.get_file_list(self.build_path_dir)
        for src in fname_list:
            if re.findall("\\.so$", src):
                des = re.sub("^(.*?)\\.cpython-.*?\\.so$", "\\1.so", src)
                os.rename(src, des)

    def run(self):
        """start complie"""
        valid_modules_list = list(filter(lambda x: self.is_valid_file(x), self.fname_list))
        other_file_list = list(filter(lambda x: not self.is_valid_file(x), self.fname_list))
        exts = Extension(name='app',
                         sources=valid_modules_list,
                         extra_link_args=['-framework', 'OpenGL', '-framework', 'GLUT'])

        setup(ext_modules=cythonize(
                exts,
                compiler_directives=dict(always_allow_keywords=True,
                                         c_string_encoding='utf-8',
                                         language_level=self.language)
        ),
                cmdclass=dict(build_ext=build_ext),
                script_args=["build_ext", "-b", self.build_path_dir, "-t", self.tmp_path_dir]
        )

        self.clean_tmp_files(valid_modules_list)
        self.copy_other_files(other_file_list)
        self.rename()


def get_user_params():
    """
    parameters parsing
    """
    opt = OptionParser()

    opt.add_option('-l', '--language',
                   dest='language',
                   type=int,
                   default=3,
                   help='the python version, python2 or python3, default 2')

    opt.add_option("-f", '--file',
                   dest='file',
                   type=str,
                   default=None,
                   help='the local path of a file to compile')

    options, args = opt.parse_args()
    return options


def main():
    """main"""
    argv = get_user_params()
    p = Py2so(argv.language, argv.file)
    p.run()


if __name__ == '__main__':
    main()
