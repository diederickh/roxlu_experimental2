import os
from base import *

class Iconv(Base):
    
    def __init__(self):
        self.name = "iconv"
        self.version = "1.14"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG]  # , Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []

    def download(self):
        rb_download_and_extract(self, 
                                "http://ftp.gnu.org/pub/gnu/libiconv/libiconv-" +self.version +".tar.gz",
                                "libiconv-" +self.version +".tar.gz", 
                                "libiconv-" +self.version)


    def build(self):
        if rb_is_mac():
            rb_build_with_autotools(self, "--enable-static=yes --enable-shared=yes")
        else:
            rb_red_ln("@todo iconv")

    def is_build(self):
        if rb_is_mac():
            return rb_install_lib_file_exists("libiconv.a")

    def deploy(self):
        if rb_is_mac():
            rb_deploy_lib(rb_install_get_lib_file("libiconv.a"))
            rb_deploy_lib(rb_install_get_lib_file("libiconv.dylib"))
            rb_deploy_lib(rb_install_get_lib_file("libiconv.2.dylib"))
            rb_deploy_lib(rb_install_get_lib_file("libcharset.a"))
            rb_deploy_lib(rb_install_get_lib_file("libcharset.dylib"))
            rb_deploy_lib(rb_install_get_lib_file("libcharset.1.dylib"))
            rb_deploy_header(rb_install_get_include_file("iconv.h"))
            rb_deploy_header(rb_install_get_include_file("libcharset.h"))
            rb_deploy_header(rb_install_get_include_file("localcharset.h"))

        else:
            rb_red_ln("@todo iconv")

            #rb_deploy_lib(rb_download_get_file(self, "lib/libGLEW.a"))
            #rb_deploy_lib(rb_download_get_file(self, "lib/libGLEW.1.10.0.dylib"))
            #rb_deploy_lib(rb_download_get_file(self, "lib/libGLEW.1.10.dylib"))
            #rb_deploy_headers(dir = rb_get_download_dir(self) +"include/GL", subdir = "GL")

                
            



