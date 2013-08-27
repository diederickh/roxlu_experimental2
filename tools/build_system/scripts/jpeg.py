import os
from base import *

class JPEG(Base):
    def __init__(self):
        self.name = "jpeg"
        self.version = "8d"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []
        self.info = "Make sure to install the Windows SDK"
        

    def download(self): 
        rb_download_and_extract(self, 
                                "http://www.ijg.org/files/jpegsrc.v" +self.version +".tar.gz",
                                "jpegsrc.v" +self.version +".tar.gz", 
                                "jpeg-" +self.version)
    def build(self):
        if rb_is_macgcc():
            rb_build_with_autotools(self)
        elif rb_is_msvc():

            debug_flag = ""
            if rb_is_release():
                debug_flag = "nodebug=1"

            rb_copy_to_download_dir(self, "Win32.mak")
            rb_download_dir_copy_file_internal(self, "jconfig.vc", "jconfig.h")

            bd = rb_get_download_dir(self)
            cmd =(
                "call " +os.path.normpath(rb_msvc_get_setvars()),
                "cd " +os.path.normpath(bd),
                "nmake /f Makefile.vc clean",
                "nmake /f Makefile.vc " +debug_flag
            )

            rb_execute_shell_commands(self, cmd)
    
    def deploy(self):
        bd = rb_get_download_dir(self)
        
        if rb_is_msvc():
            rb_deploy_lib(bd + "libjpeg.lib")

        rb_deploy_header(bd +"jpeglib.h")
        rb_deploy_header(bd +"jconfig.h")
        rb_deploy_header(bd +"jerror.h")
        rb_deploy_header(bd +"jmorecfg.h")

        
