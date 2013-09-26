import os
from base import *

class x264(Base):
    def __init__(self):
        self.name = "x264"
        self.version = "e61d9f9d3d77584136a591e01cebecbd7547a43b"
        self.compilers = [Base.COMPILER_MAC_GCC,Base.COMPILER_MAC_CLANG,Base.COMPILER_WIN_MSVC2010] # Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012, 
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = ["yasm"]
        self.info = "Windows build needs mingw"

    def download(self): 
        rb_git_clone(self, "git://git.videolan.org/x264.git", self.version)

    def build(self):

        if rb_is_mac():
            opts = " --enable-static "
            rb_build_with_autotools(self, opts)
        elif rb_is_msvc():

            dbg_flag = "--enable-debug" if rb_is_debug() else ""

            # x264 needs c99 which is not supported by vs2010/2012 yet
            # and it seems there is a bug in x264dll.c, DllMain takes a HINSTANCE, not a HANDLE for the first argument
            dd = rb_get_download_dir(self)
            cmd = (
                "cd " +rb_mingw_windows_path_to_cygwin_path(dd),
                "./configure " +rb_mingw_get_configure_prefix_flag() +" --cross-prefix=i686-w64-mingw32- --disable-cli --enable-shared " +dbg_flag +" --enable-win32thread --extra-ldflags=\"-Wl,--output-def=libx264.def\"",
                "sed \"s/HANDLE hinstDLL/HINSTANCE hinstDLL/g\" x264dll.c > x264dll.c.new",
                "mv x264dll.c x264dll.orig",
                "mv x264dll.c.new x264dll.c",
                "make clean",
                "make",
                "make install"
                )

            rb_mingw_execute_shell_commands(self, cmd)

    def is_build(self):
        if rb_is_unix():
            return rb_install_lib_file_exists("libx264.a")
        elif rb_is_win():
            return rb_deploy_lib_file_exists("libx264.dll.a")
        else:
            rb_red_ln("Cannot check if the lib is build on this platform")
    
    def deploy(self):
        if rb_is_unix():
            rb_deploy_lib(rb_install_get_lib_file("libx264.a"))
            rb_deploy_header(rb_install_get_include_file("x264.h"))
            rb_deploy_header(rb_install_get_include_file("x264_config.h"))
        elif rb_is_win():
            rb_deploy_lib(rb_install_get_lib_file("libx264.dll.a"))
            rb_deploy_dll(rb_install_get_bin_file("libx264-138.dll"))
            rb_deploy_header(rb_install_get_include_file("x264.h"))
            rb_deploy_header(rb_install_get_include_file("x264_config.h"))
        else:
            rb_red_ln("@todo")

