import os
from base import *


class Flac(Base):
    
    def __init__(self):
        self.name = "flac"
        self.version = "1.3.0"
        self.compilers = [Base.COMPILER_WIN_MSVC2010] # Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG]  # , Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = ["ogg"]

    def download(self):
        rb_download_and_extract(self, 
                                "http://downloads.xiph.org/releases/flac/flac-" +self.version +".tar.xz",
                                "flac-" +self.version +".tar.xz", 
                                "flac-" +self.version)

    def build(self):
        if rb_is_mac():
            rb_red_ln("@flac")
        elif rb_is_msvc():
            
            dd = rb_get_download_dir(self)
            rb_copy_to_download_dir(self, "libFLAC_dynamic.vcxproj", dd +"src/libFLAC/")

            rb_msvc_setup_build_environment()

            cmd = rb_msvc_get_environment_vars()
            cmd += (
                "call " +rb_msvc_get_setvars(), 
                "SET PATH=%PATH%;" +rb_deploy_get_include_dir(),
                "SET LINK=" +rb_deploy_get_lib_file("libogg.lib"),
                "cd " +dd,
                "msbuild.exe src\\libFLAC\\libFLAC_dynamic.vcxproj  " +rb_msvc_get_msbuild_type_flag() +rb_msvc_get_toolset_flag()
                )

            rb_execute_shell_commands(self, cmd)


    def is_build(self):
        if rb_is_unix():
            rb_red_ln("@flac")
        elif rb_is_win():
            return rb_deploy_lib_file_exists("libFLAC_dynamic.lib")
        else:
            rb_red_ln("Cannot check if the lib is build on this platform")
        return False


    def deploy(self):
        if rb_is_mac(): 
            rb_red_ln("@todo flac ")
        elif rb_is_win():
            dd = rb_get_download_dir(self) +"\\objs\\" +("debug" if rb_is_debug() else "release") +"\\"
            rb_deploy_dll(dd +"lib\\libFLAC_dynamic.dll")
            rb_deploy_lib(dd +"lib\\libFLAC_dynamic.lib")
            rb_deploy_headers(rb_get_download_dir(self)+"include/FLAC", subdir = "FLAC")
            rb_deploy_headers(rb_get_download_dir(self)+"include/share", subdir = "share")
            rb_deploy_headers(rb_get_download_dir(self)+"include/share/grabbag", subdir = "share/grabbag")
        else:
            rb_red_ln("@todo flac ")




                
            



