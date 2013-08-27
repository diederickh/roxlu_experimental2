import os
from base import *


class PortAudio(Base):
    
    def __init__(self):
        self.name = "portaudio"
        self.version = "1907"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG]  # , Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012]
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
            rb_red_ln("@todo portaudio")


    def deploy(self):
        if rb_is_mac():
            rb_deploy_lib(rb_install_get_lib_file("libportaudio.a"))
            rb_deploy_lib(rb_install_get_lib_file("libportaudio.2.dylib"))
            rb_deploy_lib(rb_install_get_lib_file("libportaudio.dylib"))
            rb_deploy_header(rb_install_get_include_file("portaudio.h"))
        else:
            rb_red_ln("@todo portaudio ")



                
            



