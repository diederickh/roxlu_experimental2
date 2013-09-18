import os
from base import *

class Pango(Base):
    
    def __init__(self):
        self.name = "pango"
        self.version = "05fe0e7443026b8504da32fd8bc92433cacdb431"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        if rb_is_unix():
            self.dependencies = ["automake", "autoconf", "libtool", "glib", "png","cairo"]
        else:
            self.dependencies = []

    def download(self):
        rb_git_clone(self, "git://git.gnome.org/pango", self.version)

    def build(self):

        cmd = [
            "cd " +rb_get_download_dir(self),
            "autoreconf --force --install"
            ]
        #rb_execute_shell_commands(self, cmd, rb_get_autotools_environment_vars())
        rb_build_with_autotools(self)

    def is_build(self):
        return True
        if rb_is_unix():
            return rb_install_lib_file_exists("libpixman-1.a")
        else:
            rb_red_ln("@todo pixman")

    def deploy(self):
        return True
        if rb_is_unix():
            rb_deploy_lib(rb_install_get_lib_file("libpixman-1.a"))
            rb_deploy_lib(rb_install_get_lib_file("libpixman-1.0.dylib"))
            rb_deploy_lib(rb_install_get_lib_file("libpixman-1.dylib"))
            rb_deploy_headers(dir = rb_install_get_include_dir() +"pixman-1", subdir = "pixman-1")
        else:
            rb_red_ln("@todo pixman")



                
            



