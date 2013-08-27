import os
from base import *

class Theora(Base):

    def __init__(self):
        self.name = "theora"
        self.version = "18970"
        self.compilers = [Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012, Base.COMPILER_MAC_GCC]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = ["automake","autoconf","libtool","vorbis","ogg"]
        self.info = "We use the svn version; which contains a valid VS2010 build file"
        
    def download(self): 
        rb_svn_checkout(self, "http://svn.xiph.org/trunk/theora", self.version)

    def build(self):
        if rb_is_mac():

            cmds = [
                "export PATH=" +rb_install_get_bin_dir() +":${PATH}",
                "export CC=clang",
                "export CXX=clang++",
                "cd " +rb_get_download_dir(self),
                "./autogen.sh"
                ]
            rb_execute_shell_commands(self, cmds)

            # Using gcc-4.2 gives us this ASM error: https://gist.github.com/roxlu/2d238e0bd182d8079fc0
            envvars = {"CC":"clang", "CXX":"clang++"}
            
            opts = ()
            if rb_is_32bit():
                opts = ("--exec_prefix=" +rb_install_get_dir() +" --disable-asm ")
            elif rb_is_64bit():
                opts = ("--exec_prefix=" +rb_install_get_dir() )

            rb_build_with_autotools(self, opts, environmentVars = envvars)

        elif rb_is_msvc():

            rb_download_dir_copy_internal(self, "win32/VS2010", "win32/VS2012")
            rb_vs2010_upgrade_to_vs2012(self, rb_get_download_dir(self) +"win32/VS2012/", "libtheora_dynamic.sln")

            # Build the solution for the dll version
            dd = rb_get_download_dir(self)
            cmd = (
                "call " +rb_msvc_get_setvars(), 
                "cd " +dd +"/win32/VS" +("2010" if rb_is_vs2010() else "2012"),
                "msbuild.exe libtheora/libtheora_dynamic.vcxproj  " +rb_msvc_get_msbuild_type_flag() +rb_msvc_get_toolset_flag()
            )

            rb_execute_shell_commands(self, cmd)


    def deploy(self):
        if rb_is_msvc():
            sd = "VS2010" if rb_is_vs2010() else "VS2012"
            dd = rb_get_download_dir(self) +"win32/" +sd +"/libtheora/Win32/" +rb_msvc_get_build_type_string() +"/"
            rb_deploy_dll(dd +"libtheora.dll")
            rb_deploy_lib(dd +"libtheora.lib")
            rb_deploy_headers(dir = rb_get_download_dir(self) +"/include/theora", subdir =  "theora")
        elif rb_is_mac():
            rb_deploy_lib(rb_install_get_lib_file("libtheora.a"))
            rb_deploy_lib(rb_install_get_lib_file("libtheoraenc.a"))
            rb_deploy_lib(rb_install_get_lib_file("libtheoradec.a"))
            rb_deploy_lib(rb_install_get_lib_file("libtheoradec.1.dylib"))
            rb_deploy_lib(rb_install_get_lib_file("libtheoraenc.1.dylib"))
            rb_deploy_headers(dir = rb_install_get_include_dir() +"theora", subdir = "theora")

                
        
