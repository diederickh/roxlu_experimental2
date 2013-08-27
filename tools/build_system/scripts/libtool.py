import os
from base import *

class LibTool(Base):

    def __init__(self):
        self.name = "libtool"
        self.version = "2.4.2"
        self.compilers = [Base.COMPILER_MAC_GCC]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []
        self.info = ""
        
    def download(self): 
        rb_download_and_extract(self, 
                                "http://ftp.gnu.org/gnu/libtool/libtool-" +self.version +".tar.gz",
                                "libtool-" +self.version +".tar.gz", 
                                "libtool-" +self.version)

    def build(self):
        if rb_is_macgcc():
            rb_build_with_autotools(self)
        elif rb_is_msvc():
            rb_red_ln("libtool is only for unices")


    def deploy(self):
        if rb_is_msvc():
            rb_red_ln("libtool is only for unices")
        elif rb_is_macgcc():
            rb_red_ln("we do not implement deploy for libtool; is run from build dir")

                
        
