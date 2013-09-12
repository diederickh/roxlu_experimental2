import os
from base import *

class AutoMake(Base):

    def __init__(self):
        self.name = "automake"
        self.version = "1.14"
        self.compilers = [Base.COMPILER_MAC_GCC]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []
        self.info = ""
        
    def download(self): 
        rb_download_and_extract(self, 
                                "http://ftp.gnu.org/gnu/automake/automake-" +self.version +".tar.gz",
                                "automake-" +self.version +".tar.gz", 
                                "automake-" +self.version)

    def build(self):
        if rb_is_mac():
            rb_build_with_autotools(self)
        elif rb_is_msvc():
            rb_red_ln("automake is only for unices")


    def is_build(self):
        if rb_is_unix():
            return rb_install_bin_file_exists("automake")

    def deploy(self):
        if rb_is_msvc():
            rb_red_ln("automake is only for unices")
        elif rb_is_mac():
            rb_red_ln("we do not implement deploy for automake; is run from build dir")

                
        
