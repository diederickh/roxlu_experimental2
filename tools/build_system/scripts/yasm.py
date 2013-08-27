import os
from base import *

class Yasm(Base):

    def __init__(self):
        self.name = "yasm"
        self.version = "1.2.0"
        self.compilers = [Base.COMPILER_MAC_GCC]        
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []

    def download(self): 
        rb_download_and_extract(self, 
                                "http://www.tortall.net/projects/yasm/releases/yasm-" +self.version +".tar.gz",
                                "yasm-" +self.version +".tar.gz", 
                                "yasm-" +self.version)
    def build(self):
        if rb_is_mac():
            rb_build_with_autotools(self)

    def is_build(self):
        return rb_install_lib_file_exists("libyasm.a")

    def deploy(self):
        rb_red_ln("No deploy for yasm")


        
