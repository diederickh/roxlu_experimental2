import os
from base import *

class UV(Base):

    def __init__(self):
        self.name = "uv"
        self.version = "d7a1ba85f204183244721d838a70286cb5cfddeb"
        self.compilers = [Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012]        
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []

    def download(self): 
        rb_git_clone(self, "git@github.com:joyent/libuv.git", self.version)

    def build(self):
        if rb_is_unix():

            arch = "ia32" if rb_is_32bit() else "x64"

            output_dir = rb_get_triplet() +"_" +rb_msvc_get_build_type_string()

            dd = rb_get_download_dir(self)

            # static lib
            cmd = (
                "set -x",
                "cd " +dd,
                "if [ ! -d build/gyp ] ; then  git clone https://git.chromium.org/external/gyp.git build/gyp ; fi",
                "./gyp_uv -Dtarget_arch=" +arch +" -Dhost_arch=" +arch,
                "make -C out BUILDTYPE=" +rb_msvc_get_build_type_string() +rb_get_make_compiler_flags(),
                "mv out " +output_dir
                )

            rb_execute_shell_commands(self, cmd)
            return True
            # shared lib
            output_dir = output_dir +"_Shared"
            cmd = (
                "cd " +dd,
                "if [ ! -d build/gyp ] ; then  git clone https://git.chromium.org/external/gyp.git build/gyp ; fi",
                "./gyp_uv -Dtarget_arch=" +arch +" -Dlibrary=shared_library -Dcomponent=shared_library ",
                "make -C out BUILDTYPE=" +rb_msvc_get_build_type_string() +rb_get_make_compiler_flags(),
                "mv out " +output_dir
                )

            rb_execute_shell_commands(self, cmd)



        elif rb_is_msvc():
            dd = rb_get_download_dir(self)
            cmd = (
                "cd " +dd,
                "call " +rb_msvc_get_setvars(),
                "call vcbuild.bat release shared",
                "msbuild.exe uv.sln /t:libuv " +rb_msvc_get_msbuild_type_flag()
            )
            rb_execute_shell_commands(self, cmd)


    def is_build(self):
        if rb_is_unix():
            return rb_install_lib_file_exists("libuv.a")
        elif rb_is_win():
            return rb_deploy_lib_file_exists("libuv.dll") # test this!
        else:
            rb_red_ln("Cannot check if the lib is build on this platform")

    
    def deploy(self):
        if rb_is_msvc():
            dd = rb_get_download_dir(self)
            cd = dd +"/" +rb_msvc_get_build_type_string() +"/"
            rb_deploy_lib(cd +"libuv.lib")
            rb_deploy_dll(cd +"libuv.dll")
            rb_deploy_headers(dd +"/include/")
        elif rb_is_unix():

            # static and dynamic libs are build separately + clang<>gcc use different paths (gyp)
            output_dir = rb_get_download_dir(self) +rb_get_triplet() +"_" +rb_msvc_get_build_type_string()
            od_shared = output_dir +"_Shared"
            od_static = output_dir
            if rb_is_clang():
                od_static = od_static +"/out/" +rb_msvc_get_build_type_string() +"/"
                od_shared = od_shared +"/out/" +rb_msvc_get_build_type_string() +"/"
            else:
                od_static = od_static +"/" +rb_msvc_get_build_type_string() +"/" 
                od_shared = od_shared +"/" +rb_msvc_get_build_type_string() +"/"

            # And install
            rb_deploy_lib(od_static +"libuv.a")
            rb_deploy_lib(od_shared +"libuv.dylib")
            rb_deploy_header(rb_download_get_file(self, "include/pthread-fixes.h"))
            rb_deploy_header(rb_download_get_file(self, "include/stdint-msvc2008.h"))
            rb_deploy_header(rb_download_get_file(self, "include/tree.h"))
            rb_deploy_header(rb_download_get_file(self, "include/uv-bsd.h"))
            rb_deploy_header(rb_download_get_file(self, "include/uv-darwin.h"))
            rb_deploy_header(rb_download_get_file(self, "include/uv-errno.h"))
            rb_deploy_header(rb_download_get_file(self, "include/uv-linux.h"))
            rb_deploy_header(rb_download_get_file(self, "include/uv-sunos.h"))
            rb_deploy_header(rb_download_get_file(self, "include/uv-unix.h"))
            rb_deploy_header(rb_download_get_file(self, "include/uv-win.h"))
            rb_deploy_header(rb_download_get_file(self, "include/uv.h"))
        else:
            rb_red_ln("Deploy uv not implemented")
            


        
