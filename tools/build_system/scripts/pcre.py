import os
from base import *

class PCRE(Base):
    def __init__(self):
        self.name = "pcre"
        self.version = "8.33"
        self.compilers = [Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012, Base.COMPILER_MAC_GCC]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []
        self.info = ""

    def download(self): 
        rb_download_and_extract(self, 
                                "ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-" +self.version +".tar.gz",
                                "pcre-" +self.version +".tar.gz", 
                                "pcre-" +self.version)

    def build(self):
        if rb_is_unix():
            rb_build_with_autotools(self);
        elif rb_is_msvc():

            # Construct the CMake command
            custom_opts = [
                "-DZLIB_INCLUDE_DIR=" +rb_deploy_get_include_dir(),
                "-DZLIB_LIBRARY=" +rb_deploy_get_lib_dir() +"zdll.lib",
                "-DBUILD_SHARED_LIBS=yes"
            ]

            rb_cmake_configure(self, custom_opts)
            rb_cmake_build(self)

    def is_build(self):
        if rb_is_unix():
            return rb_install_lib_file_exists("libcpre.a")
        elif rb_is_win():
            debug_flag = ""
            if rb_is_debug():
                debug_flag = "d"
            libname = "pcrecpp" +debug_flag +".lib"
            return rb_deploy_lib_file_exists(libname)
        else:
            rb_red_ln("Cannot check if the lib is build on this platform")


    def deploy(self):

        if rb_is_msvc():
            ih = rb_install_get_include_dir() 
            ld = rb_install_get_lib_dir()
            bd = rb_install_get_bin_dir()
            rb_deploy_headers(ih, ["pcre.h", "pcre_scanner.h", "pcre_stringpiece.h", "pcrecpp.h", "pcrecpparg.h", "pcreposix.h"])

            debug_flag = ""
            if rb_is_debug():
                debug_flag = "d"

            rb_deploy_lib(ld +"pcrecpp" +debug_flag +".lib")
            rb_deploy_lib(ld +"pcre" +debug_flag +".lib")
            rb_deploy_lib(ld +"pcreposix" +debug_flag +".lib")
            rb_deploy_dll(bd +"pcrecpp" +debug_flag +".dll")
            rb_deploy_dll(bd +"pcre" +debug_flag +".dll")
            rb_deploy_dll(bd +"pcreposix" +debug_flag +".dll")
        else:
            # headers
            ih = rb_install_get_include_dir() 
            ld = rb_install_get_lib_dir()
            bd = rb_install_get_bin_dir()
            rb_deploy_headers(ih, ["pcre.h", "pcre_scanner.h", "pcre_stringpiece.h", "pcrecpp.h", "pcrecpparg.h", "pcreposix.h"])

            # libs
            id = rb_install_get_dir();
            rb_deploy_lib(id +"lib/libpcre.a")
            rb_deploy_lib(id +"lib/libpcrecpp.a")
            rb_deploy_lib(id +"lib/libpcreposix.a")
            rb_deploy_lib(id +"lib/libpcre.1.dylib")
            rb_deploy_lib(id +"lib/libpcrecpp.0.dylib")
            rb_deploy_lib(id +"lib/libpcreposix.0.dylib")


            
                
            
