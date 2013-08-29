import os
from base import *

class Iconv(Base):
    
    def __init__(self):
        self.name = "iconv"
        self.version = "1.14"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG, Base.COMPILER_WIN_MSVC2010] # , Base.COMPILER_WIN_MSVC2012]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []
        self.info = "Not yet compiling libcharset on windows"

    def download(self):
        rb_download_and_extract(self, 
                                "http://ftp.gnu.org/pub/gnu/libiconv/libiconv-" +self.version +".tar.gz",
                                "libiconv-" +self.version +".tar.gz", 
                                "libiconv-" +self.version)


    def build(self):
        if rb_is_mac():
            rb_build_with_autotools(self, "--enable-static=yes --enable-shared=yes")
        else:
            # setup the project, we fixed iconv so it compiled on VS2010 using this 
            # awesome how-to http://www.codeproject.com/Articles/302012/How-to-Build-libiconv-with-Microsoft-Visual-Studio
            dd = rb_get_download_dir(self)

            if rb_is_vs2010():
                vs_name = "vs2010"
                vs_dir = dd +vs_name +"/"
                if not os.path.exists(vs_dir):
                    rb_msvc_copy_custom_project(self, vs_dir)
                    rb_ensure_dir(vs_dir +"include/")
                    rb_move_file(vs_dir +"/src/iconv.h", vs_dir +"include/iconv.h")
                    rb_move_file(vs_dir +"/src/config.h", vs_dir +"include/config.h")
                    
                    rb_download_dir_copy_file_internal(self, "lib/*.h", vs_name +"/include/")
                    rb_download_dir_copy_file_internal(self, "lib/*.def", vs_name +"/include/")

            cmd = (
                "call " +rb_msvc_get_setvars(), 
                "cd " +dd +"\\vs" +("2010" if rb_is_vs2010() else "2012"),
                "msbuild.exe libiconv.sln /t:libiconv " +rb_msvc_get_msbuild_type_flag() +rb_msvc_get_toolset_flag()
                )

            rb_execute_shell_commands(self, cmd)


    def is_build(self):
        if rb_is_mac():
            return rb_install_lib_file_exists("libiconv.a")
        else:
            return rb_deploy_lib_file_exists("libiconv.lib")

    def deploy(self):
        if rb_is_mac():
            rb_deploy_lib(rb_install_get_lib_file("libiconv.a"))
            rb_deploy_lib(rb_install_get_lib_file("libiconv.dylib"))
            rb_deploy_lib(rb_install_get_lib_file("libiconv.2.dylib"))
            rb_deploy_lib(rb_install_get_lib_file("libcharset.a"))
            rb_deploy_lib(rb_install_get_lib_file("libcharset.dylib"))
            rb_deploy_lib(rb_install_get_lib_file("libcharset.1.dylib"))
            rb_deploy_header(rb_install_get_include_file("iconv.h"))
            rb_deploy_header(rb_install_get_include_file("libcharset.h"))
            rb_deploy_header(rb_install_get_include_file("localcharset.h"))

        else:
            dd = rb_get_download_dir(self)
            vs_dir = dd +("vs2010" if rb_is_vs2010() else "vs2012") 
            vs_install = vs_dir +"/" +rb_msvc_get_build_type_string() +"/"
            rb_deploy_lib(vs_install +"libiconv.lib")
            rb_deploy_dll(vs_install +"libiconv.dll")
            rb_deploy_header(vs_dir +"/include/iconv.h")
                
            



