import os
from base import *

class GLXW(Base):
    
    def __init__(self):
        self.name = "glxw"
        self.version = ""
        self.compilers = [Base.COMPILER_WIN_MSVC2010]
        self.arch = [Base.ARCH_M32]
        self.dependencies = []
        self.info = ""

    def download(self):
        rb_git_clone(self, "git@github.com:rikusalminen/glxw.git")

    def build(self):
        return True
        dd = rb_get_download_dir(self)
        cmd = (
            "cd " +dd,
            "python glxw_gen.py"
            )
        rb_execute_shell_commands(self, cmd)

        return True

    def is_build(self):
        return False

    def deploy(self):
        if rb_is_win():
            rb_deploy_headers(dir = rb_get_download_dir(self) +"/include/GL/", subdir = "GL")
            rb_deploy_headers(dir = rb_get_download_dir(self) +"/include/GLXW/", subdir = "GLXW")
            rb_deploy_sources(dir = rb_get_download_dir(self) +"/src/", subdir = "GLXW")




                
            



