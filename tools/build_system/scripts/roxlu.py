import os
from base import *

class Roxlu(Base):
    
    def __init__(self):
        self.name = "roxlu"
        self.version = "0.0.0.2"
        self.compilers = [Base.COMPILER_WIN_MSVC2010, Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG] 
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.info = "roxlu is only added to compile all libraries in the build system"
        self.dependencies = ["autoconf", "automake", "libtool", "pkgconfig", "curl", "ffi", "gettext", "iconv", 
                             "glew", "glfw", "glib", "flac", "freetype", "jansson", "jpeg", "lamemp3",
                             "mysql-c-connector", "ogg", "openssl", "pcre", "png", "portaudio", "sndfile", 
                             "speex", "theora", "tiff", "uv", "vorbis", "x264", "yasm", "zlib", "rtmp", "gnuplot"]

    def download(self):
        return True

    def build(self):
        return True

    def is_build(self):
        return True

    def deploy(self):
        return True



                
            



