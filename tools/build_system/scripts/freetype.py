import os
from base import *

class FreeType(Base):

    def __init__(self):
        self.name = "freetype"
        self.version = "2.5.0"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_WIN_MSVC2010] #, Base.COMPILER_WIN_MSVC2012]        
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = ["zlib"]


    def download(self): 
        rb_download_and_extract(self, 
                                "http://download.savannah.gnu.org/releases/freetype/freetype-" +self.version  +".tar.gz",
                                "freetype-" +self.version +".tar.gz", 
                                "freetype-" +self.version)
    def build(self):
        if rb_is_unix():
            rb_build_with_autotools(self)

        elif rb_is_msvc():
            dd = rb_get_download_dir(self)
            cmd = (
                "call " +rb_msvc_get_setvars(), 
                "cd " +dd +"/builds/win32/vc2010/",
                "msbuild.exe freetype.sln /t:freetype " +rb_msvc_get_msbuild_type_flag() +rb_msvc_get_toolset_flag()
            )
            rb_execute_shell_commands(self, cmd)
            rb_red_ln("@todo freetype build msvc");
    

    def is_build(self):
        if rb_is_unix():
            return rb_install_lib_file_exists("libfreetype.a")
        else:
            rb_yellow_ln("@todo freetype")

    def deploy(self):
        if rb_is_mac():
            rb_deploy_lib(rb_install_get_lib_file("libfreetype.a"))
            rb_deploy_lib(rb_install_get_lib_file("libfreetype.6.dylib"))
            rb_deploy_headers(dir = rb_install_get_include_dir() +"freetype2/freetype/", subdir = "freetype2/freetype/")
            rb_deploy_header(rb_install_get_include_file("ft2build.h"))
        else:
            dd = rb_get_download_dir(self)
            libdir = dd +"objs/win32/vc2010/"
            rb_deploy_lib(libdir +"freetype250.lib")
            rb_deploy_headers(dir = dd +"include/freetype/", subdir = "freetype2/freetype/")
            rb_deploy_header(dd +"include/ft2build.h")
                
        
