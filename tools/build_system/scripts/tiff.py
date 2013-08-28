import os
from base import *

class Tiff(Base):

    def __init__(self):
        self.name = "tiff"
        self.version = "4.0.3"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012]        
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = ["jpeg", "zlib"]

    def download(self): 
        rb_download_and_extract(self, 
                                "ftp://ftp.remotesensing.org/pub/libtiff/tiff-" +self.version +".tar.gz",
                                "tiff-" +self.version +".tar.gz", 
                                "tiff-" +self.version)
    def build(self):
        if rb_is_mac():

            ef = (
                "--with-zlib-include-dir=" +rb_get_include_dir(),
                "--with-zlib-lib-dir=" +rb_get_lib_dir(),
                "--with-jpeg-include-dir=" +rb_get_include_dir(),
                "--with-jpeg-lib-dir=" +rb_get_lib_dir()
            )

            rb_build_with_autotools(self, " ".join(ef))

        elif rb_is_msvc():

            d = rb_get_download_path(self)

            cmd = (
                "call " +rb_msvc_get_setvars(),
                "cd " +d,
                "nmake /f Makefile.vc clean",
                "nmake /f Makefile.vc"
            )

            rb_execute_shell_commands(self, cmd)

    def is_build(self):
        if rb_is_unix():
            return rb_install_lib_file_exists("libtiff.a")
        elif rb_is_win():
            return rb_deploy_lib_file_exists("libtiff.lib")
        else:
            rb_red_ln("Cannot check if the lib is build on this platform")

    
    def deploy(self):
        if rb_is_msvc():
            bd = rb_get_download_dir(self) +"/libtiff/"
            rb_deploy_lib(bd +"libtiff.lib")
            rb_deploy_dll(bd +"libtiff.dll")
            rb_deploy_headers(bd, ["tiff.h", "tiffconf.h", "tiffio.h", "tiffio.hxx", "tiffvers.h"])
        
                
        
