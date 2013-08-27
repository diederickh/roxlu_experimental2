import os
from base import *

class AutoConf(Base):

    def __init__(self):
        self.name = "autoconf"
        self.version = "2.69"
        self.compilers = [Base.COMPILER_MAC_GCC]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []
        self.info = ""
        
    def download(self): 
        rb_download_and_extract(self, 
                                "http://ftp.gnu.org/gnu/autoconf/autoconf-" +self.version +".tar.gz",
                                "autoconf-" +self.version +".tar.gz", 
                                "autoconf-" +self.version)

    def build(self):
        if rb_is_macgcc():
            rb_build_with_autotools(self)
        elif rb_is_msvc():
            rb_red_ln("autoconf is only for unices")


    def deploy(self):
        if rb_is_msvc():
            rb_red_ln("autoconf is only for unices")
        elif rb_is_macgcc():
            rb_red_ln("we do not implement deploy for autoconf; is run from build dir")

                
        
