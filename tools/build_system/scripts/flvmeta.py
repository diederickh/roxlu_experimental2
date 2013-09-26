import os
from base import *

class FLVMeta(Base):
    
    def __init__(self):
        self.name = "flvmeta"
        self.version = "ca53a8eb319176023b1ac95e7498156a9a53c347"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []

    def download(self):
        rb_git_clone(self, "git@github.com:noirotm/flvmeta.git")

    def build(self):
        rb_cmake_configure(self)
        rb_cmake_build(self)
        return True

    def is_build(self):
        if rb_is_unix():
            return True
        else:
            rb_yellow_ln("@todo FLVMeta")

    def deploy(self):
        rb_yellow_ln("@todo -- ")

                
            



