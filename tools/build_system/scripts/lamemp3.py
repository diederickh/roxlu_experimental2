import os
from base import *

class LameMP3(Base):

    def __init__(self):
        self.name = "lamemp3"
        self.version = "3.99.5"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012]        
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []
        self.info = "@todo check out if we can use the SSE2 version"

    def download(self): 
        rb_download_and_extract(self, 
                                "http://downloads.sourceforge.net/project/lame/lame/3.99/lame-3.99.5.tar.gz",
                                "lame-" +self.version +".tar.gz", 
                                "lame-" +self.version)
    def build(self):
        if rb_is_macgcc():
            rb_build_with_autotools(self)
        elif rb_is_msvc():

            dd = rb_get_download_dir(self)
            rb_msvc_copy_custom_project(self, dd +"/" +rb_get_compiler_shortname())

            cmd = (
                "call " +rb_msvc_get_setvars(),
                "cd " +dd +"/" +rb_get_compiler_shortname(),
                "del /q .\\..\\output\\" +rb_msvc_get_build_type_string() +"\\*",
                "msbuild.exe vc9_lame.sln " +rb_msvc_get_msbuild_type_flag()  +" /t:libmp3lame "
            )

            rb_execute_shell_commands(self, cmd)
    
    def deploy(self):
        if rb_is_msvc():
            id = rb_get_download_dir(self) +"/include/"
            sd = rb_get_download_dir(self) +"/output/" +rb_msvc_get_build_type_string() +"/"
            rb_deploy_dll(sd +"libmp3lame.dll")
            rb_deploy_lib(sd +"libmp3lame.lib")
            rb_deploy_header(id +"lame.h", "lame")
        else:
            rb_red_ln("Deploy lamemp3 not implemented")
            


        
