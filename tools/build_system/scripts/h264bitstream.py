import os
from base import *

class H264BitStream(Base):

    def __init__(self):
        self.name = "h264bitstream"
        self.version = "0.1.9"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG]        
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []

    def download(self): 
        rb_download_and_extract(self, 
                                "http://sourceforge.net/projects/h264bitstream/files/h264bitstream/" +self.version +"/h264bitstream-" +self.version +".tar.gz/download",
                                "h264bitstream-" +self.version +".tar.gz", 
                                "h264bitstream-" +self.version)
    def build(self):
        if rb_is_unix():
            rb_build_with_autotools(self);


    def is_build(self):
        return True
    
    def deploy(self):
        return True
                
        
