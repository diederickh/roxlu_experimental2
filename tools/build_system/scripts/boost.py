import os
from base import *

class Boost(Base):
    
    def __init__(self):
        self.name = "boost"
        self.version = "1.54.0"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []

    def download(self):

        rb_download_and_extract(self, 
                                "http://sourceforge.net/projects/boost/files/boost/1.54.0/boost_1_54_0.tar.gz/download",
                                "boost_1_54_0.tar.gz", 
                                "boost_1_54_0")


    def build(self):

        if rb_is_unix():
            dd = rb_get_download_dir(self)
            variant = "debug" if rb_is_debug() else "release"
            address_model = "32" if rb_is_32bit() else "64"
            libs = ["date_time","exception","filesystem","iostreams","math","random","thread","timer","system"]
            # cxxflags=\"-stdlib=libc++\" linkflags=\"-stdlib=libc++\" 
            toolset = "toolset=clang " if rb_is_clang() else "" 

            cmd = (
                "cd " +dd,
                "./bootstrap.sh " +rb_get_configure_prefix_flag() +" --with-libraries=" +",".join(libs),
#                "./b2 --clean -a",
                "./b2 -a " +toolset +" --build-type=minimal --layout=system variant=" +variant +" threading=multi link=static address-model=" +address_model +" install"
                )

            rb_execute_shell_commands(self, cmd)

        elif rb_is_msvc():
            rb_red_ln("@todo boost")


    def is_build(self):
        if rb_is_unix():
            return rb_install_lib_file_exists("libboost_system.a")
        else:
            rb_reg_ln("@todo boost")

    def deploy(self):
        if rb_is_unix():
            ld = rb_install_get_lib_dir()
            rb_deploy_lib(ld +"libboost_*")

        rb_deploy_headers(dir = rb_install_get_dir() +"include/boost/", subdir = "boost")


                
            



