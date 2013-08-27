import os
from base import *

class Speex(Base):

    def __init__(self):
        self.name = "speex"
        self.version = "1.2rc1"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_WIN_MSVC2010] #, Base.COMPILER_WIN_MSVC2012,
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []
        self.info = "WORK IN PROGRESS"
        
    def download(self): 
        rb_download_and_extract(self, 
                                "http://downloads.xiph.org/releases/speex/speex-" +self.version +".tar.gz",
                                "speex-" +self.version +".tar.gz", 
                                "speex-" +self.version)


    def build(self):
        if rb_is_macgcc():
            rb_build_with_autotools(self)
        elif rb_is_msvc():
            dd = rb_get_download_dir(self)
            rb_msvc_copy_custom_project(self, dd +"\\win32\\" +rb_get_compiler_shortname())
            cmd = (
                "call " +rb_msvc_get_setvars(), 
                "cd " +dd +"\\win32\\vs" +("2010" if rb_is_vs2010() else "2012"),
                "msbuild.exe libspeex\\libspeex.sln /t:libspeex " +rb_msvc_get_msbuild_type_flag() +rb_msvc_get_toolset_flag()
                )
            rb_execute_shell_commands(self, cmd)


    def deploy(self):
        if rb_is_msvc():
            sd = "vs2010" if rb_is_vs2010() else "vs2012"
            dd = rb_get_download_dir(self) +"win32/" +sd +"/libspeex/" +rb_msvc_get_build_type_string() +"/"
            rb_deploy_dll(dd +"libspeex.dll")
            rb_deploy_lib(dd +"libspeex.lib")
            rb_deploy_headers(dir = rb_get_download_dir(self) +"include/speex", subdir = "speex")

        elif rb_is_macgcc():
            rb_deploy_lib(rb_install_get_lib_file("libspeex.a"))
            rb_deploy_lib(rb_install_get_lib_file("libspeexdsp.a"))
            rb_deploy_lib(rb_install_get_lib_file("libspeexdsp.1.5.0.dylib"))
            rb_deploy_lib(rb_install_get_lib_file("libspeex.1.5.0.dylib"))
            rb_deploy_headers(dir = rb_install_get_include_dir() +"speex", subdir = "speex")


                
        
