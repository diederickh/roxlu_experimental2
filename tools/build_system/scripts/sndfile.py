import os
from base import *


class SndFile(Base):
    
    def __init__(self):
        self.name = "sndfile"
        self.version = "1.0.25"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG, Base.COMPILER_WIN_MSVC2010]  # , Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.info = "There is no vorbisenc.dll project for windows yet so sndfile is not compiled with flag/vorbis/ogg support on windows"

        if not rb_is_win():
            self.dependencies = ["ogg","speex","vorbis","pkgconfig"]
        else:
            self.dependencies = ["ogg","speex","vorbis"]

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
        elif rb_is_win():

            dd = rb_get_download_dir(self)
#             rb_mingw_create_pkgconfig_file("ogg", "1.3.1", "-logg")
#             rb_mingw_create_pkgconfig_file("vorbisenc", "1.3.3", "-lvorbisenc")
#             rb_mingw_create_pkgconfig_file("vorbis", "1.3.3", "-lvorbis")
#             rb_mingw_create_pkgconfig_file("flac", "1.3.0", "-lFLAC_dynamic")

            
            # execute commands in the mingw environment
            cmd = (
                "cd " +dd,
                "./configure " +rb_mingw_get_configure_prefix_flag()  +" --enable-static=no --enable-shared=yes --host=i686-w64-mingw32",
                "make clean",
                "make V=1",
                "make install"
                )
            env = rb_get_autotools_environment_vars()
            rb_mingw_execute_shell_commands(self, cmd, env)

            # execute some commands in the default vs201X shell
            cmd = (
                "cd " +dd,
                "call " +rb_msvc_get_setvars(),
                "cd src/ && lib /machine:i386 /def:libsndfile-1.def"
                )
            rb_execute_shell_commands(self, cmd)


    def is_build(self):

        if rb_is_unix():
            return rb_install_lib_file_exists("libsndfile.a")
        elif rb_is_win():
            return rb_deploy_lib_file_exists("libsndfile-1.lib")
        else:
            rb_red_ln("Cannot check if the lib is build on this platform")


    def deploy(self):
        if rb_is_mac():
            rb_deploy_lib(rb_install_get_lib_file("libsndfile.a"))
            rb_deploy_lib(rb_install_get_lib_file("libsndfile.dylib"))
            rb_deploy_lib(rb_install_get_lib_file("libsndfile.1.dylib"))

        elif rb_is_win():
            dd = rb_get_download_dir(self)
            sd = dd +"/src/.libs/"
            rb_deploy_dll(sd +"libsndfile-1.dll")
            rb_deploy_lib(dd +"src/libsndfile-1.lib")
            
        else:
            rb_red_ln("@todo sndfile ")

        rb_deploy_header(rb_install_get_include_file("sndfile.h"))
        rb_deploy_header(rb_install_get_include_file("sndfile.hh"))



                
            



