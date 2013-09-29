import os
from base import *

class LibYUV(Base):
    
    def __init__(self):
        self.name = "libyuv"
        self.version = ""
        self.compilers = [Base.COMPILER_WIN_MSVC2010]
        self.arch = [Base.ARCH_M32]
        self.dependencies = []
        self.info = ""

    def download(self):
        rb_svn_checkout(self, "http://libyuv.googlecode.com/svn/trunk")


    def build(self):
        rb_copy_to_download_dir(self, "CMakeLists.txt")
        rb_cmake_configure(self)
        rb_cmake_build(self)

    def is_build(self):
        if rb_is_win():
            return rb_deploy_lib_file_exists("libyuv.lib")
        return False

    def deploy(self):
        if rb_is_win():
            rb_deploy_headers(dir = rb_install_get_include_dir() +"libyuv/", subdir = "libyuv")
            rb_deploy_lib(rb_install_get_lib_file("libyuv.lib"))
        else:
            rb_yellow_ln("@todo libyuv - deploy on !win")



                
            



