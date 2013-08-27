import os
from base import *
import subprocess

class Jansson(Base):
    def __init__(self):
        self.name = "jansson"
        self.version = "2.4"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_WIN_MSVC2012, Base.COMPILER_WIN_MSVC2010]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []

    def download(self): 
        rb_download_and_extract(self, 
                                "http://www.digip.org/jansson/releases/" "jansson-" +self.version +".tar.gz", 
                                "jansson-" +self.version +".tar.gz", 
                                "jansson-" +self.version)
    def build(self):

        # MAC 
        if rb_is_mac():
            rb_build_with_autotools(self)

        # WIN VS2010
        elif Base.compiler == Base.COMPILER_WIN_MSVC2010:

            bd = rb_get_download_path(self) +"win32/vs2010"
            cmd = ("call " +rb_msvc_get_setvars(),
                   "cd " +bd,
                   "msbuild.exe jansson.sln " +rb_vs2010_get_msbuild_type_flag())

            rb_execute_shell_commands(self, cmd)


        # WIN VS2012
        elif Base.compiler == Base.COMPILER_WIN_MSVC2012:
            # Make a copy of the 2010 dir + upgrade
            bd = rb_get_download_path(self) +"win32/"
            vs2010_dir = bd +"vs2010/"
            vs2012_dir = bd +"vs2012/"
            if not os.path.exists(vs2012_dir):
                shutil.copytree(vs2010_dir, vs2012_dir)
                shutil.rmtree(vs2012_dir +"\\Output")
                shutil.rmtree(vs2012_dir +"\\Build")
                        
            rb_red_ln("Jansson, should alsouse rb_execute_shell_commands")

            cmd = (
                "call " +rb_msvc_get_setvars(),
                "cd " +os.path.normpath(bd) +"\\vs2012",
                "devenv jansson.sln /upgrade",
                "msbuild.exe jansson.sln " +rb_vs2012_get_msbuild_type_flag()
            )

            rb_execute_shell_commands(cmd)

    def deploy(self):
        if rb_is_win():
            dp = rb_get_download_path(self)
            sd = rb_get_download_path(self) +"win32/" \
                 +rb_get_compiler_shortname() \
                 +"/Output/" \
                 +rb_msvc_get_build_type_string()
 
            rb_deploy_dll(sd +"/jansson.dll")
            rb_deploy_lib(sd +"/jansson.lib")
            rb_deploy_header(dp +"/src/jansson.h")
            rb_deploy_header(dp +"/src/jansson_config.h")
            
        else:
            rb_deploy_lib(rb_install_get_lib_file("libjansson.a"))
            rb_deploy_lib(rb_install_get_lib_file("libjansson.4.dylib"))
            rb_deploy_lib(rb_install_get_lib_file("libjansson.dylib"))
            rb_deploy_header(rb_install_get_include_file("jansson.h"))
            rb_deploy_header(rb_install_get_include_file("jansson_config.h"))
        
