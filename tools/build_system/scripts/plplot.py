import os
from base import *

class PLplot(Base):
    
    def __init__(self):
        self.name = "plplot"
        self.version = ""
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = ["cairo", "freetype"]

    def download(self):
        rb_svn_checkout(self, "https://svn.code.sf.net/p/plplot/code/trunk")

    def build(self):
        if rb_is_unix():
            opts = [
                "-DBUILD_SHARED_LIBS=0",
                "-DFREETYPE_INCLUDE_DIR=" +rb_install_get_include_dir(),
                "-DFREETYPE_LIBRARY=" +rb_install_get_lib_file("libfreetype.a")
                ]
            rb_cmake_configure(self, opts)
            rb_cmake_build(self)
        else:
            rb_yellow_ln("@todo plplot")

    def is_build(self):
        if rb_is_unix():
            d = "d" if rb_is_debug() else ""
            return rb_install_lib_file_exists("libplplot" +d +".a")
        else:
            rb_red_ln("@todo plplot")

    def deploy(self):
        if rb_is_unix():
            d = "d" if rb_is_debug() else ""
            rb_deploy_lib(rb_install_get_lib_file("libplplot" +d +".a"))
            rb_deploy_lib(rb_install_get_lib_file("libplplotcxx" +d +".a"))
            rb_deploy_headers(dir = rb_install_get_include_dir() +"plplot", subdir = "plplot")
        else:
            rb_red_ln("@todo plplot")



                
            



