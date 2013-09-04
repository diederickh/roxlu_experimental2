import os
from base import *

class PNG(Base):
    def __init__(self):
        self.name = "png"
        self.version = "1.6.3"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = ["zlib"]
        self.info = "The mac build is not using our own custom zlib! "

    def download(self): 
        rb_download_and_extract(self, 
                                "http://prdownloads.sourceforge.net/libpng/libpng-" +self.version +".tar.gz?download",
                                "libpng-" +self.version +".tar.gz", 
                                "libpng-" +self.version)
    def build(self):
        
        if rb_is_mac():
      
            ef = ("--with-zlib-prefix=" +rb_install_get_dir(),
                  "--with-sysroot=" +rb_install_get_dir())

            dd = rb_get_download_dir(self)
            cmd = (
                "cd " +dd,
                "./configure "+ rb_get_configure_prefix_flag(),
                "make clean && make && make install"
                )

            rb_execute_shell_commands(self, cmd)

            # something goes wrong with zlib version; the detected version is old/wrong
            #rb_build_with_autotools(self, " ".join(ef))

        elif rb_is_msvc():

            # copy our custom project
            dd = rb_get_download_dir(self)
            rb_msvc_copy_custom_project(self, dd +"/projects/" +rb_get_compiler_shortname()) 

            # copy the default config
            rb_download_dir_copy_file_internal(self, "scripts/pnglibconf.h.prebuilt", "pnglibconf.h")

            # build through command line
            cmd = (
                "cd " +dd +"/projects/" +rb_get_compiler_shortname(),
                "call " +rb_msvc_get_setvars(), 
                "msbuild.exe vstudio.sln /t:libpng " +rb_msvc_get_msbuild_type_flag()
            )
            rb_execute_shell_commands(self, cmd)

            

    def deploy(self):
        if rb_is_msvc():
            dd = rb_get_download_dir(self)
            bd = dd +"/projects/" +rb_get_compiler_shortname() +"/" +rb_msvc_get_build_type_string() 
            rb_deploy_dll(bd +"/libpng16.dll")
            rb_deploy_lib(bd +"/libpng16.lib")
            rb_deploy_headers(dd, ["png.h", "pngconf.h", "pnglibconf.h"])
        elif rb_is_mac():
            id = rb_install_get_dir()
            rb_deploy_lib(rb_install_get_lib_file("libpng16.a"))
            rb_deploy_lib(rb_install_get_lib_file("libpng16.16.dylib"))
            rb_deploy_lib(rb_install_get_lib_file("libpng.dylib"))
            rb_deploy_lib(rb_install_get_lib_file("libpng.a"))
            rb_deploy_headers(dir = rb_install_get_include_dir() +"libpng16", subdir = "libpng16")
            rb_deploy_headers(rb_install_get_include_dir(), ["png.h", "pngconf.h", "pnglibconf.h"])


            
            
            
        
