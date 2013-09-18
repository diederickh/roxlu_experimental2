import os
from base import *

class GnuPlot(Base):
    
    def __init__(self):
        self.name = "gnuplot"
        self.version = "4.6.3"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        if rb_is_unix():
            self.dependencies = ["automake", "autoconf", "libtool"]
        else:
            self.dependencies = []

    def download(self):
        rb_download_and_extract(self, 
                                "http://sourceforge.net/projects/gnuplot/files/gnuplot/" +self.version +"/gnuplot-" +self.version +".tar.gz/download",
                                "gnuplot-" +self.version +".tar.gz", 
                                "gnuplot-" +self.version)


        """
        rb_download_and_extract(self, 
                                "http://ndevilla.free.fr/gnuplot/gnuplot_i-" +self.version +".tar.gz",
                                "gnuplot_i-" +self.version +".tar.gz", 
                                "gnuplot_i");
                                """

    def build(self):
        """
        cmd = [
            "cd " +rb_get_download_dir(self),
            "make"
            ]
        rb_execute_shell_commands(self, cmd, rb_get_autotools_environment_vars())
        """
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



                
            



