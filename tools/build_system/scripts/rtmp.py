import os
from base import *

class Rtmp(Base):

    def __init__(self):
        self.name = "rtmp"
        self.version = ""
        self.compilers = [Base.COMPILER_MAC_GCC] #, Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012]        
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = ["zlib", "openssl"]

    def download(self): 
        rb_git_clone(self, "git://git.ffmpeg.org/rtmpdump")

    def build(self):
        return True
        if rb_is_unix():
            dd = rb_get_download_dir(self)
            env = rb_get_autotools_environment_vars()
            ef = (
                "cd " +dd,
                "make sys=darwin"
                )
            rb_execute_shell_commands(self, ef, env)
        return True

    def is_build(self):
        if rb_is_unix():
            return rb_deploy_lib_file_exists("librtmp.a")
        return False
    
    def deploy(self):

        if rb_is_unix():
            rb_deploy_lib(rb_download_get_file(self, "librtmp/librtmp.a"))

        rb_deploy_headers(dir = rb_get_download_dir(self) +"librtmp/", subdir = "librtmp")
        return True
                
        
