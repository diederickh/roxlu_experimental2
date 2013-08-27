import os
from base import *


class GLFW(Base):
    
    def __init__(self):
        self.name = "glfw"
        self.version = "5da6a903f9a533063a77400b0a8873d5c9753f99"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []

    def download(self):
        rb_git_clone(self, "git@github.com:glfw/glfw.git", self.version)

    def build(self):
        rb_cmake_configure(self)
        rb_cmake_build(self)

    def deploy(self):
         if rb_is_msvc():
             dd = rb_get_download_dir(self)
             nd = rb_install_get_dir()
             rb_deploy_lib(nd +"lib/glfw3.lib")
             rb_deploy_create_headers_dir("GLFW")
             rb_deploy_headers(nd +"include/GLFW/", ["glfw3.h", "glfw3native.h"], "GLFW")
         elif rb_is_mac():
             rb_deploy_lib(rb_install_get_lib_file("libglfw3.a"))
             rb_deploy_headers(dir = rb_install_get_include_dir() +"GLFW", subdir = "GLFW")
         
                
            



