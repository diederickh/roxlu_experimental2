import os
from base import *


class PortAudio(Base):
    
    def __init__(self):
        self.name = "portaudio"
        self.version = "1907"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG, Base.COMPILER_WIN_MSVC2010] #, Base.COMPILER_WIN_MSVC2012]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []

    def download(self):
        rb_svn_checkout(self, "https://subversion.assembla.com/svn/portaudio/portaudio/trunk/", self.version)

    def build(self):

        if rb_is_mac():
            dd = rb_get_download_dir(self)
            env = rb_get_autotools_environment_vars()
            
            # PortAudio won't compile with -werror
            cmd = (
                "cd " +dd,
                "./configure " +rb_get_configure_flags() +rb_get_configure_options(),
                "sed \"s/-Werror/-Wall/g\" Makefile > Makefile.new",
                "mv Makefile Makefile.old",
                "mv Makefile.new Makefile",
                "make",
                "make install"
                )

            rb_execute_shell_commands(self, cmd, env)
        else:
            opts = [ 
                "-DPA_DLL_LINK_WITH_STATIC_RUNTIME=False",
                ]
            rb_cmake_configure(self, opts)
            rb_cmake_build(self, "portaudio")

    def is_build(self):
        if rb_is_unix():
            return rb_install_lib_file_exists("libportaudio.a")
        elif rb_is_win():
            return rb_deploy_lib_file_exists("portaudio_x86.lib")
        else:
            rb_red_ln("Cannot check if the lib is build on this platform")

    def deploy(self):
        if rb_is_mac():
            rb_deploy_lib(rb_install_get_lib_file("libportaudio.a"))
            rb_deploy_lib(rb_install_get_lib_file("libportaudio.2.dylib"))
            rb_deploy_lib(rb_install_get_lib_file("libportaudio.dylib"))
            rb_deploy_header(rb_install_get_include_file("portaudio.h"))
        else:
            bd = rb_get_download_dir(self) +rb_get_cmake_configure_dir() +"/" +rb_msvc_get_build_type_string() +"/"
            rb_deploy_lib(bd +"portaudio_x86.lib")
            rb_deploy_dll(bd +"portaudio_x86.dll")
            rb_deploy_header(rb_get_download_dir(self) +"include\portaudio.h")




                
            



