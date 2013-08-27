import os
from base import *


class SndFile(Base):
    
    def __init__(self):
        self.name = "sndfile"
        self.version = "1.0.25"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG]  # , Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = ["ogg","speex","vorbis","pkgconfig"]

    def download(self):
        rb_download_and_extract(self, 
                                "http://www.mega-nerd.com/libsndfile/files/libsndfile-" +self.version +".tar.gz",
                                "libsndfile-" +self.version +".tar.gz", 
                                "libsndfile-" +self.version)

        # fix carbon include
        if rb_is_mac():
            dd = rb_get_download_dir(self)
            cmd = (
                "cd " +dd,
                "cd programs",
                "sed \"s/#include <Carbon.h>/#include <Carbon\/Carbon.h>/g\" sndfile-play.c > sndfile-play.c.new",
                "mv sndfile-play.c sndfile-play.orig",
                "mv sndfile-play.c.new sndfile-play.c"
                )
            rb_execute_shell_commands(self, cmd)

    def build(self):
        if rb_is_mac():
            rb_build_with_autotools(self)
        else:
            rb_red_ln("@todo sndfile")

    def is_build(self):
        return rb_install_lib_file_exists("libsndfile.a")

    def deploy(self):
        if rb_is_mac():
            rb_deploy_lib(rb_install_get_lib_file("libsndfile.a"))
            rb_deploy_lib(rb_install_get_lib_file("libsndfile.dylib"))
            rb_deploy_lib(rb_install_get_lib_file("libsndfile.1.dylib"))
            rb_deploy_header(rb_install_get_include_file("sndfile.h"))
            rb_deploy_header(rb_install_get_include_file("sndfile.hh"))
        else:
            rb_red_ln("@todo sndfile ")



                
            



