import os
from base import *

class x264(Base):
    def __init__(self):
        self.name = "x264"
        self.version = "e61d9f9d3d77584136a591e01cebecbd7547a43b"
        self.compilers = [Base.COMPILER_MAC_GCC] # Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012, 
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []
        self.info = ""

    def download(self): 
        rb_git_clone(self, "git://git.videolan.org/x264.git", self.version)

    def build(self):
        if rb_is_macgcc():
            opts = " --enable-static "
            rb_build_with_autotools(self, opts)
            rb_red_ln("@mac todo")
        elif rb_is_msvc():
            rb_red_ln("@win todo")
    
    def deploy(self):
        if rb_is_mac():
            rb_deploy_lib(rb_install_get_lib_file("libx264.a"))
            rb_deploy_header(rb_install_get_include_file("x264.h"))
            rb_deploy_header(rb_install_get_include_file("x264_config.h"))
        else:
            rb_red_ln("@todo")

