import os
from base import *

class x264(Base):
    def __init__(self):
        self.name = "x264"
        self.version = "e61d9f9d3d77584136a591e01cebecbd7547a43b"
        self.compilers = [Base.COMPILER_MAC_GCC,Base.COMPILER_MAC_CLANG] # Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012, 
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = ["yasm"]
        self.info = ""

    def download(self): 
        rb_git_clone(self, "git://git.videolan.org/x264.git", self.version)

    def build(self):
        if rb_is_mac():
            opts = " --enable-static "
            rb_build_with_autotools(self, opts)
        elif rb_is_msvc():
            rb_red_ln("@win todo")

    def is_build(self):
        return rb_install_lib_file_exists("libx264.a")
    
    def deploy(self):
        if rb_is_mac():
            rb_deploy_lib(rb_install_get_lib_file("libx264.a"))
            rb_deploy_header(rb_install_get_include_file("x264.h"))
            rb_deploy_header(rb_install_get_include_file("x264_config.h"))
        else:
            rb_red_ln("@todo")

