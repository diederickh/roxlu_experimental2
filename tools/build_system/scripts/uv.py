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

            # libuv checks this environment variable that will compile with vs11 instead of vs10, therefore
            # we have to unset it.
            vs11comtools_copy = os.environ["VS110COMNTOOLS"];
            if rb_is_vs2010():
                os.environ["VS110COMNTOOLS"] = "";

            cmd = (
                "cd " +dd,
                "call " +rb_msvc_get_setvars(),
                "call vcbuild.bat release shared",
                "msbuild.exe uv.sln /t:libuv " +rb_msvc_get_msbuild_type_flag()
            )
            rb_execute_shell_commands(self, cmd)
            
            # and set back...
            if rb_is_vs2010():
                os.environ["VS110COMNTOOLS"] = vs11comtools_copy;

    def is_build(self):
        if rb_is_unix():
            return rb_install_lib_file_exists("libuv.a")
        elif rb_is_win():
            return rb_deploy_lib_file_exists("libuv.dll") # test this!
        else:
            rb_red_ln("Cannot check if the lib is build on this platform")

    # on mac the build file destination can be either in "Release/out", "out" or just "Release"
    # this finds the correct one :) 
    def get_build_file(self, filename):
        dd = rb_get_download_dir(self)
        output_dir = rb_get_download_dir(self) +rb_get_triplet() +"_" +rb_msvc_get_build_type_string()
        output_dir_a = output_dir +"/" +rb_msvc_get_build_type_string() +"/"
        output_dir_b = output_dir +"/out/" +rb_msvc_get_build_type_string() +"/";
        output_dir_c = output_dir +"_Shared/" +rb_msvc_get_build_type_string() +"/"
        output_dir_d = output_dir +"_Shared/out/" +rb_msvc_get_build_type_string() +"/"
        file_a = output_dir_a +filename
        file_b = output_dir_b +filename
        file_c = output_dir_c +filename
        file_d = output_dir_d +filename
        if os.path.exists(file_a):
            return file_a
        elif os.path.exists(file_b):
            return file_b
        elif os.path.exists(file_c):
            return file_c
        elif os.path.exists(file_d):
            return file_d
        else:
            rb_yellow_ln("Cannot find file: " +filename +" in either: " +file_a +" or " +file_b)
            return False
            
    def deploy_lib_if_exists(self, filename):
        fn = self.get_build_file(filename)
        if fn:
            rb_deploy_lib(fn)
    
    def deploy(self):
        if rb_is_msvc():
            dd = rb_get_download_dir(self)
            cd = dd +"/" +rb_msvc_get_build_type_string() +"/"
            rb_deploy_lib(cd +"libuv.lib")
            rb_deploy_dll(cd +"libuv.dll")
            rb_deploy_headers(dd +"/include/")
        elif rb_is_unix():
 
            self.deploy_lib_if_exists("libuv.a")
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
            


        
