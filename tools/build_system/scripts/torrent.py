import os
from base import *

class Torrent(Base):
    
    def __init__(self):
        self.name = "torrent"
        self.version = "0.15.0"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = ["boost","automake","autoconf","libtool"]

    def download(self):
        rb_svn_checkout(self, "svn://svn.code.sf.net/p/libtorrent/code/trunk")

    def build(self):
        if rb_is_unix():
            
            cmd = (
                "cd " +rb_get_download_dir(self),
                "./autotool.sh"
                )
            rb_execute_shell_commands(self, cmd, rb_get_autotools_environment_vars())
            rb_build_with_autotools(self, "--enable-examples=yes --enable-logging=yes --enable-dht=yes --with-boost-libdir=" +rb_deploy_get_lib_dir())

        elif rb_is_msvc():
            rb_red_ln("@todo torrent - probably win needs boost build")

    def is_build(self):
        rb_red_ln("@todo torrent")

    def deploy(self):
        if rb_is_unix():
            ld = rb_install_get_lib_dir()
            rb_deploy_lib(ld +"libtorrent-rasterbar.8.dylib")
            rb_deploy_lib(ld +"libtorrent-rasterbar.dylib")
            rb_deploy_lib(ld +"libtorrent-rasterbar.a")


        rb_deploy_headers(dir = rb_install_get_dir() +"include/libtorrent", subdir = "libtorrent")


                
            



