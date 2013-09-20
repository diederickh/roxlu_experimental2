import os
from base import *

class Nanomsg(Base):
    
    def __init__(self):
        self.name = "nanomsg"
        self.version = ""
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []

    def download(self):
        rb_git_clone(self, "git@github.com:nanomsg/nanomsg.git", self.version)

    def build(self):
        if rb_is_unix():
            if not rb_download_file_exists(self, "configure"):
                cmd = [
                    "cd " +rb_get_download_dir(self),
                    "./autogen.sh"
                    ]
                rb_execute_shell_commands(self, cmd, rb_get_autotools_environment_vars())

            rb_build_with_autotools(self)

    def is_build(self):
        
        if rb_is_unix():
            return rb_install_lib_file_exists("libnanomsg.a")
        else:
            rb_red_ln("@todo nanomsg")

    def deploy(self):

        if rb_is_mac():
            rb_deploy_lib(rb_install_get_lib_file("libnanomsg.0.dylib"))
            rb_deploy_lib(rb_install_get_lib_file("libnanomsg.dylib"))

        if rb_is_unix():
            rb_deploy_lib(rb_install_get_lib_file("libnanomsg.a"))
            rb_deploy_headers(dir = rb_install_get_include_dir() +"nanomsg", subdir = "nanomsg")
        else:
            rb_yellow_ln("@todo nanomsg")





                
            



