import os
from base import *

class Samplerate(Base):
    
    def __init__(self):
        self.name = "samplerate"
        self.version = "0.1.8"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        if rb_is_unix():
            self.dependencies = ["automake", "autoconf", "libtool"]
        else:
            self.dependencies = []

    def download(self):

        rb_download_and_extract(self, 
                                "http://www.mega-nerd.com/SRC/libsamplerate-" +self.version +".tar.gz",
                                "libsamplerate-" +self.version +".tar.gz", 
                                "libsamplerate-" +self.version)

        if rb_is_mac():
            # there is an incorrect carbon include (doesnt work on mac 10.8)
            dd = rb_get_download_dir(self)
            cmd = [
                "cd " +dd,
                "cd examples",
                "sed \"s/#include <Carbon.h>/#include <Carbon\/Carbon.h>/g\" audio_out.c > audio_out.new",
                "mv audio_out.c audio_out.orig",
                "mv audio_out.new audio_out.c"
            ]
            rb_execute_shell_commands(self, cmd)


    def build(self):
        rb_build_with_autotools(self)

    def is_build(self):
        if rb_is_unix():
            return rb_install_lib_file_exists("libsamplerate.a")
        else:
            rb_red_ln("@todo samplerate")

    def deploy(self):
        if rb_is_mac():
            rb_deploy_lib(rb_install_get_lib_file("libsamplerate.dylib"))
            rb_deploy_lib(rb_install_get_lib_file("libsamplerate.0.dylib"))

        if rb_is_unix():
            rb_deploy_lib(rb_install_get_lib_file("libsamplerate.a"))
        else:
            rb_yellow_ln("@todo samplerate")

        rb_deploy_header(rb_install_get_include_file("samplerate.h"))



                
            



