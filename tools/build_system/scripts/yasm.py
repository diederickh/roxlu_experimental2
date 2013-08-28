import os
from base import *

class Yasm(Base):

    def __init__(self):
        self.name = "yasm"
        self.version = "1.2.0"
        self.compilers = [Base.COMPILER_MAC_GCC]        
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []

    def download(self): 
        rb_download_and_extract(self, 
                                "http://www.tortall.net/projects/yasm/releases/yasm-" +self.version +".tar.gz",
                                "yasm-" +self.version +".tar.gz", 
                                "yasm-" +self.version)

        # On windows we use YASM with mingw (eg. to build x264)
        if rb_is_win():
            rb_ensure_tools_dir("yasm/win32")
            rb_ensure_tools_dir("yasm/win64")
        
            if not rb_tools_file_exists("yasm/win32/yasm.exe"):
                rb_download(self, "http://www.tortall.net/projects/yasm/releases/yasm-" +self.version +"-win32.exe", "yasm32.exe")
                rb_move_file(rb_download_get_file(self, "yasm32.exe"), rb_get_tools_path() +"yasm/win32/yasm.exe")

            if not rb_tools_file_exists("yasm/win64/yasm.exe"):
                rb_download(self, "http://www.tortall.net/projects/yasm/releases/yasm-" +self.version +"-win64.exe", "yasm64.exe")
                rb_move_file(rb_download_get_file(self, "yasm64.exe"), rb_get_tools_path() +"yasm/win64/yasm.exe")

    def build(self):
        if rb_is_mac():
            rb_build_with_autotools(self)


    def is_build(self):
        if rb_is_unix():
            return rb_install_lib_file_exists("libyasm.a")
        else:
            return rb_tools_file_exists("yasm\\win32\\yasm.exe")

    def deploy(self):
        rb_red_ln("No deploy for yasm")


        
