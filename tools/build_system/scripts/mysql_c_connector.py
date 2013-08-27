import os
from base import *
import subprocess

class MySQLCConnector(Base):
    def __init__(self):
        self.name = "mysql-connector-c"
        self.version = "6.1.1"
        self.compilers = [Base.COMPILER_MAC_GCC] # , Base.COMPILER_WIN_MSVC2012, Base.COMPILER_WIN_MSVC2010]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []
        self.info = "Work in progress; compiles but we need to implement deploy()"

    def download(self): 
        rb_download_and_extract(self, 
                                "http://dev.mysql.com/get/Downloads/Connector-C/mysql-connector-c-" +self.version +"-src.tar.gz/from/http://cdn.mysql.com/",
                                "mysql-connector-c-" +self.version +"-src.tar.gz", 
                                "mysql-connector-c-" +self.version +"-src")
    def build(self):

        if rb_is_mac_gcc():
            dd = rb_get_download_dir(self)
            rb_cmake_configure(self)
            rb_cmake_build(self)

        elif rb_is_msvc():
            rb_red_ln("@todo mysql-connector-c for win")

    def deploy(self):
        if rb_is_msvc():
            rb_red_ln("@todo mysql-connector-c for win")
        elif rb_is_mac_gcc():
            rb_red_ln("@todo working on it :")
        
