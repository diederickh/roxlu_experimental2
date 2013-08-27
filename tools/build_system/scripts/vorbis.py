import os
from base import *

class Vorbis(Base):

    def __init__(self):
        self.name = "vorbis"
        self.version = "1.3.3"
        self.compilers = [Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012, Base.COMPILER_MAC_GCC]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []
        
    def download(self): 
        rb_download_and_extract(self, 
                                "http://downloads.xiph.org/releases/vorbis/libvorbis-" +self.version +".tar.gz",
                                "libvorbis-" +self.version +".tar.gz", 
                                "libvorbis-" +self.version)
    def build(self):
        if rb_is_macgcc():
            rb_build_with_autotools(self)
        elif rb_is_msvc():

            # Copy the VS2010 project to VS2012 and convert
            rb_download_dir_copy_internal(self, "win32/VS2010", "win32/VS2012")
            rb_vs2010_upgrade_to_vs2012(self, rb_get_download_dir(self) +"win32/VS2012/", "vorbis_dynamic.sln")
            
            # Build the solution for the dll version
            dd = rb_get_download_dir(self)
            cmd = (
                "call " +rb_msvc_get_setvars(), 
                "cd " +dd +"/win32/VS" +("2010" if rb_is_vs2010() else "2012"),
                "msbuild.exe vorbis_dynamic.sln /t:libvorbis " +rb_msvc_get_msbuild_type_flag() +rb_msvc_get_toolset_flag()
            )

            rb_execute_shell_commands(self, cmd)

    def deploy(self):
        if rb_is_msvc():
            sd = "VS2010" if rb_is_vs2010() else "VS2012"
            dd = rb_get_download_dir(self) +"win32/" +sd +"/Win32/" +rb_msvc_get_build_type_string() +"/"
            rb_deploy_dll(dd +"libvorbis.dll")
            rb_deploy_lib(dd +"libvorbis.lib")
            rb_deploy_headers(dir = rb_get_download_dir(self) +"/include/vorbis", subdir =  "vorbis")

        elif rb_is_macgcc():
            rb_deploy_lib(rb_install_get_lib_file("libvorbis.a"))
            rb_deploy_lib(rb_install_get_lib_file("libvorbisenc.a"))
            rb_deploy_lib(rb_install_get_lib_file("libvorbisfile.a"))
            rb_deploy_lib(rb_install_get_lib_file("libvorbis.0.dylib"))
            rb_deploy_lib(rb_install_get_lib_file("libvorbisenc.2.dylib"))
            rb_deploy_lib(rb_install_get_lib_file("libvorbisfile.3.dylib"))
            rb_deploy_headers(dir = rb_install_get_include_dir() +"vorbis", subdir = "vorbis")

                
        
