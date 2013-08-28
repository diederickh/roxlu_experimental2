import os
from base import *
import subprocess

class MySQLCConnector(Base):
    def __init__(self):
        self.name = "mysql-connector-c"
        self.version = "6.1.1"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG, Base.COMPILER_WIN_MSVC2010] #, Base.COMPILER_WIN_MSVC2012]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []
        self.info = "Work in progress; compiles but we need to implement deploy()"

    def download(self): 
        rb_download_and_extract(self, 
                                "http://dev.mysql.com/get/Downloads/Connector-C/mysql-connector-c-" +self.version +"-src.tar.gz/from/http://cdn.mysql.com/",
                                "mysql-connector-c-" +self.version +"-src.tar.gz", 
                                "mysql-connector-c-" +self.version +"-src")
    def build(self):
        rb_cmake_configure(self)
        rb_cmake_build(self)

    def is_build(self):
        if rb_is_unix():
            return rb_install_lib_file_exists("libmysql.a")
        elif rb_is_win():
            return rb_deploy_lib_file_exists("libmysql.lib")
        else:
            rb_red_ln("Cannot check if the lib is build on this platform")

    def deploy(self):
        if rb_is_msvc():
            ld = rb_install_get_lib_dir()
            bd = rb_install_get_bin_dir()
            id = rb_install_get_include_dir()
            rb_deploy_lib(ld +"libmysql.lib")
            rb_deploy_lib(ld +"mysqlclient.lib")
            rb_deploy_dll(ld +"libmysql.dll")

        elif rb_is_mac_gcc():
            rb_red_ln("@todo working on it :")

        hdrs = [
                "big_endian.h",
                "byte_order_generic.h",
                "byte_order_generic_x86.h",
                "byte_order_generic_x86_64.h",
                "decimal.h",
                "errmsg.h",
                "keycache.h",
                "little_endian.h",
                "m_ctype.h",
                "m_string.h",
                "my_alloc.h",
                "my_attribute.h",
                "my_byteorder.h",
                "my_compiler.h",
                "my_config.h",
                "my_dbug.h",
                "my_dir.h",
                "my_getopt.h",
                "my_global.h",
                "my_list.h",
                "my_net.h",
                "my_pthread.h",
                "my_sys.h",
                "my_xml.h",
                "mysql.h",
                "mysql_com.h",
                "mysql_com_server.h",
                "mysql_embed.h",
                "mysql_time.h",
                "mysql_version.h",
                "mysqld_ername.h",
                "mysqld_error.h",
                "sql_common.h",
                "sql_state.h",
                "sslopt-case.h",
                "sslopt-longopts.h",
                "sslopt-vars.h",
                "typelib.h"]

        rb_deploy_headers(id, hdrs)
        rb_deploy_headers(dir = rb_install_get_include_dir() +"mysql", subdir = "mysql")

