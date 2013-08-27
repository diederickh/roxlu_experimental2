import os
from base import *

class UV(Base):

    def __init__(self):
        self.name = "uv"
        self.version = "d7a1ba85f204183244721d838a70286cb5cfddeb"
        self.compilers = [Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012]        
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []

    def download(self): 
        rb_git_clone(self, "git@github.com:joyent/libuv.git", self.version)

    def build(self):
        if rb_is_macgcc():
            rb_red_len("@todo")

        elif rb_is_msvc():
            dd = rb_get_download_dir(self)
            cmd = (
                "cd " +dd,
                "call " +rb_msvc_get_setvars(),
                "call vcbuild.bat release shared",
                "msbuild.exe uv.sln /t:libuv " +rb_msvc_get_msbuild_type_flag()
            )
            rb_execute_shell_commands(self, cmd)

    
    def deploy(self):
        if rb_is_msvc():
            dd = rb_get_download_dir(self)
            cd = dd +"/" +rb_msvc_get_build_type_string() +"/"
            rb_deploy_lib(cd +"libuv.lib")
            rb_deploy_dll(cd +"libuv.dll")
            rb_deploy_headers(dd +"/include/")
        else:
            rb_red_ln("Deploy uv not implemented")
            


        
