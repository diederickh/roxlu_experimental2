import os
from base import *

class Faac(Base):
    
    def __init__(self):
        self.name = "faac"
        self.version = "1.28"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []
        self.info = ""

    def download(self):
        rb_download_and_extract(self, 
                                "http://downloads.sourceforge.net/faac/faac-" +self.version +".tar.gz",
                                "faac-" +self.version +".tar.gz",
                                "faac-" +self.version)

    def build(self):
        if rb_is_unix():
            rb_build_with_autotools(self)
        else:
            rb_yellow_ln("@todo build faac on !unix")

    def is_build(self):
        return True

    def deploy(self):
        if rb_is_unix():
            rb_deploy_lib(rb_install_get_lib_file("libfaac.a"))
            rb_deploy_headers(dir = rb_install_get_include_dir() +"/faac.h");
        else:
            rb_yellow_ln("@todo deploy faac on !unix")
        return True


                
            



