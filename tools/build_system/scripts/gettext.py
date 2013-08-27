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
            rb_red_ln("@todo pkgconfig")


    def deploy(self):
        if rb_is_mac():
            rb_red_ln("@todo pkgconfig ")
        else:
            rb_red_ln("@todo pkgconfig ")



                
            



