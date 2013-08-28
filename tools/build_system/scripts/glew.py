import os
from base import *

class Glew(Base):
    
    def __init__(self):
        self.name = "glew"
        self.version = "1.10.0"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG, Base.COMPILER_WIN_MSVC2010] # , Base.COMPILER_WIN_MSVC2012]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []

    def download(self):
        rb_download_and_extract(self, 
                                "https://sourceforge.net/projects/glew/files/glew/1.10.0/glew-" +self.version +".tgz/download",
                                "glew-" +self.version +".tar.gz", 
                                "glew-" +self.version)


    def build(self):
        if rb_is_unix():
            dd = rb_get_download_dir(self)
            env = rb_get_autotools_environment_vars()
            cmd = (
                "cd " +dd,
                "make clean",
                ("make all" if not rb_is_debug() else "make debug") +rb_get_make_compiler_flags()
                )
            rb_execute_shell_commands(self, cmd, env)

        elif rb_is_msvc():
            dd = rb_get_download_dir(self)
            
            # We only change the runtime library from /MT to /MD
            rb_copy_to_download_dir(self, "glew_shared.vcxproj", dd +"build/vc10/")

            cmd = (
                "call " +rb_msvc_get_setvars(),
                "cd " +dd +"/build/vc10/",
                "msbuild.exe glew.sln /t:glew_shared " +rb_msvc_get_msbuild_type_flag() +rb_msvc_get_toolset_flag()
                )
            rb_execute_shell_commands(self, cmd)
           

    def is_build(self):
        if rb_is_unix():
            return rb_install_lib_file_exists("libGLEW.a")
        else:
            dbg = "d" if rb_is_debug() else ""
            return rb_deploy_lib_file_exists("glew32" +dbg +".lib")

    def deploy(self):
        if rb_is_mac():
            rb_deploy_lib(rb_download_get_file(self, "lib/libGLEW.a"))
            rb_deploy_lib(rb_download_get_file(self, "lib/libGLEW.1.10.0.dylib"))
            rb_deploy_lib(rb_download_get_file(self, "lib/libGLEW.1.10.dylib"))
        elif rb_is_win():
            dbg = "d" if rb_is_debug() else ""
            rb_deploy_dll(rb_download_get_file(self, "bin/" +rb_msvc_get_build_type_string() +"/Win32/glew32" +dbg +".dll"))
            rb_deploy_lib(rb_download_get_file(self, "lib/" +rb_msvc_get_build_type_string() +"/Win32/glew32" +dbg +".lib"))

        rb_deploy_headers(dir = rb_get_download_dir(self) +"include/GL", subdir = "GL")

                
            



