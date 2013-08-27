import os
from base import *

class Glib(Base):
    
    def __init__(self):
        self.name = "glib"
        self.version = "2.36"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG]  # , Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []
        self.info = "on mac we need to figure out why the build complaints it cannot find automake"

    def download(self):
        rb_download_and_extract(self, 
                                "http://ftp.gnome.org/pub/gnome/sources/glib/2.36/glib-2.36.4.tar.xz",
                                "glib-" +self.version +".4.tar.gz", 
                                "glib-" +self.version +".4")


    def build(self):
        if rb_is_mac():
            id = rb_install_get_dir()
            env = {"LIBFFI_LIBS":"\"-L" +id+"/lib -lffi\"",
                   "LIBFFI_CFLAGS":"\"-I" +id+"/include -I" +id+"/lib/libffi-3.0.13/include/\""}
            rb_build_with_autotools(self, environmentVars=env)
        else:
            rb_red_ln("@todo pkgconfig")

    def is_build(self):
        return rb_install_lib_exists("libglib.a")

    def deploy(self):
        if rb_is_mac():
            rb_red_ln("@todo pkgconfig ")
        else:
            rb_red_ln("@todo pkgconfig ")



                
            



