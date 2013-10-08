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
        """
        dd = rb_get_download_dir(self)
        cmd = (
            "cd " +dd,
            "python glxw_gen.py"
            )
        rb_execute_shell_commands(self, cmd)
        """
        return True

    def is_build(self):
        return True

    def deploy(self):
        return True


                
            



