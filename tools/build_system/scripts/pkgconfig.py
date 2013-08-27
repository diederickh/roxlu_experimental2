import os
from base import *

class PkgConfig(Base):
    
    def __init__(self):
        self.name = "pkgconfig"
        self.version = "0.28"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG]  # , Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []

    def download(self):
        rb_download_and_extract(self, 
                                "http://pkgconfig.freedesktop.org/releases/pkg-config-" +self.version +".tar.gz",
                                "pkg-config-" +self.version +".tar.gz", 
                                "pkg-config-" +self.version)


    def build(self):
        if rb_is_mac():
            rb_build_with_autotools(self, "--with-internal-glib")
        else:
            rb_red_ln("@todo pkgconfig")

    def is_build(self):
        return rb_install_bin_file_exists("pkg-config")

    def deploy(self):
        if rb_is_mac():
            rb_red_ln("@todo pkgconfig ")
        else:
            rb_red_ln("@todo pkgconfig ")



                
            



