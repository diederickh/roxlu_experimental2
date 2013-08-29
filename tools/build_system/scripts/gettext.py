import os
from base import *

class GetText(Base):
    
    def __init__(self):
        self.name = "gettext"
        self.version = "0.18.3"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG]  # , Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []

    def download(self):
        rb_download_and_extract(self, 
                                "http://ftp.gnu.org/pub/gnu/gettext/gettext-" +self.version +".tar.gz",
                                "gettext-" +self.version +".tar.gz", 
                                "gettext-" +self.version)

        """
        if rb_is_win():

            rb_download_and_extract(self, 
                                    "http://winkde.org/pub/kde/ports/win32/repository-4.8/win32libs/gettext-vc100-0.18-src.tar.bz2",
                                    "gettext-vc100-0.18-src.tar.bz2"
                                    "gettext-vc100-0.18")

            else:
                rb_download_and_extract(self, 
                                "http://ftp.gnu.org/pub/gnu/gettext/gettext-" +self.version +".tar.gz",
                                "gettext-" +self.version +".tar.gz", 
                                "gettext-" +self.version)
                                """


    def build(self):
        if rb_is_mac():
            """
            id = rb_install_get_dir()
            env = {"LIBFFI_LIBS":"-L\"" +id+"/lib\" -lffi",
                   "LIBFFI_CFLAGS":"-I\"" +id+"/include\" -I\"" +id+"/lib/libffi-3.0.13/include/\""}
            rb_build_with_autotools(self, environmentVars=env)
                   """
            rb_build_with_autotools(self)
        else:
            opts = [ 
                "-DICONV_LIBRARIES=libiconv.lib",
                ]
            rb_cmake_configure(self, opts)
            rb_cmake_build(self, "gettext-runtime")
            rb_red_ln("@todo gettext --")


    def deploy(self):
        if rb_is_mac():
            rb_red_ln("@todo gettext")
        else:
            rb_red_ln("@todo gettext")




                
            



