import os
from base import *

class Ogg(Base):

    def __init__(self):
        self.name = "ogg"
        self.version = "1.3.1"
        self.compilers = [Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012, Base.COMPILER_MAC_GCC]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []
        self.info = "see how we use the helper functions for vs2010/vs2012 in vorbis.py"
        
    def download(self): 
        rb_download_and_extract(self, 
                                "http://downloads.xiph.org/releases/ogg/libogg-" +self.version +".tar.gz",
                                "libogg-" +self.version +".tar.gz", 
                                "libogg-" +self.version)
    def build(self):
        if rb_is_macgcc():
            rb_build_with_autotools(self);
        elif rb_is_msvc():

            # Make a copy of the vs2010 sln provided by the distribution and convert it to VS2012
            dd = rb_get_download_dir(self)
            src = dd +"win32/VS2010"
            dest = dd +"win32/VS2012"
            if not os.path.exists(dest):
                shutil.copytree(src, dest)
                convert = (
                    "call " +rb_msvc_get_setvars(), 
                    "cd " +dest,
                    "devenv libogg_dynamic.sln /upgrade"
                )
                rb_execute_shell_commands(self, convert)
                rb_green_ln("Upgraded ogg vs2010 to vs2012")

            # Execute the commands
            cmd = (
                "call " +rb_msvc_get_setvars(), 
                "cd " +dd +"/win32/VS" +("2010" if rb_is_vs2010() else "2012"),
                "msbuild.exe libogg_dynamic.sln /t:libogg " +rb_msvc_get_msbuild_type_flag() +rb_msvc_get_toolset_flag()
            )
            rb_execute_shell_commands(self, cmd)


    def deploy(self):
        if rb_is_msvc():
            sd = "VS2010" if rb_is_vs2010() else "VS2012"
            dd = rb_get_download_dir(self) +"win32/" +sd +"/Win32/" +rb_msvc_get_build_type_string() +"/"
            rb_deploy_dll(dd +"libogg.dll")
            rb_deploy_lib(dd +"libogg.lib")
            rb_deploy_headers(dir = rb_get_download_dir(self) +"/include/ogg", subdir =  "ogg")
        elif rb_is_mac():
            rb_deploy_lib(rb_install_get_lib_file("libogg.a"))
            rb_deploy_lib(rb_install_get_lib_file("libogg.0.dylib"))
            rb_deploy_headers(dir = rb_install_get_include_dir() +"ogg", subdir = "ogg")

                
        
