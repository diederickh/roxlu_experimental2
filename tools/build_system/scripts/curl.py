import os
from base import *

class Curl(Base):
    def __init__(self):
        self.name = "curl"
        self.version = "7.31.0"
        self.compilers = [Base.COMPILER_WIN_MSVC2010, Base.COMPILER_WIN_MSVC2012, Base.COMPILER_MAC_GCC]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = ["openssl", "zlib"]
        self.info = ""

    def download(self): 
        rb_download_and_extract(self, 
                                "http://curl.haxx.se/download/curl-" +self.version +".tar.gz",
                                "curl-" +self.version +".tar.gz", 
                                "curl-" +self.version)

    def build(self):
        if rb_is_mac_gcc():
            opt = (
                "--with-ssl=" +rb_install_get_dir(),
                "--enable-static=yes",
                "--disable-ldaps",
                "--disable-ldap",
                "--disable-rtsp",
                "--disable-dict",
                "--disable-telnet",
                "--disable-pop3",
                "--disable-imap",
                "--disable-smtp",
                "--disable-gopher",
                "--without-axtls",
                "--disable-ares"
                )
            rb_build_with_autotools(self, " ".join(opt));
            
        elif rb_is_msvc():

            # remove cached files
            rb_remove_download_dir(self, "builds")

            dd = rb_get_download_dir(self)

            debug_flag = "yes" if rb_is_debug() else "no"
            
            cmd = (
                "call " +os.path.normpath(rb_msvc_get_setvars()),
                "cd " +os.path.normpath(dd),
                "cd winbuild",
                "nmake /f Makefile.vc clean",
                "nmake /f Makefile.vc mode=dll WITH_DEVEL=" +rb_deploy_get_dir() +" WITH_SSL=DLL WITH_ZLIB=DLL DEBUG=" +debug_flag
                )

            rb_execute_shell_commands(self, cmd)
    
    def deploy(self):

        if rb_is_msvc():
            if rb_is_debug():
                dd = rb_get_download_dir(self) + "builds/libcurl-vc-x86-debug-dll-ipv6-sspi-spnego-winssl/"
                rb_deploy_headers(dir = dd +"include/curl/", subdir = "curl" )
                rb_deploy_lib(dd +"lib/libcurl_debug.lib")
                rb_deploy_dll(dd +"bin/libcurl_debug.dll")
            else:
                dd = rb_get_download_dir(self) + "builds/libcurl-vc-x86-release-dll-ipv6-sspi-spnego-winssl/"
                rb_deploy_headers(dir = dd +"include/curl/", subdir = "curl" )
                rb_deploy_lib(dd +"lib/libcurl.lib")
                rb_deploy_dll(dd +"bin/libcurl.dll")
        else:
            id = rb_install_get_dir();
            rb_deploy_lib(id +"lib/libcurl.a")
            rb_deploy_lib(id +"lib/libcurl.4.dylib")
            rb_deploy_headers(dir = id +"include/curl", subdir = "curl")
        
