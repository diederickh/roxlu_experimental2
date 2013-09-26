import os
from base import *

class RapidXML(Base):
    
    def __init__(self):
        self.name = "rapidxml"
        self.version = "1.13"
        self.compilers = [Base.COMPILER_MAC_GCC, Base.COMPILER_MAC_CLANG]
        self.arch = [Base.ARCH_M32, Base.ARCH_M64]
        self.dependencies = []

    def download(self):
        rb_download_and_extract(self, 
#                                  http://sourceforge.net/projects/rapidxml/files/rapidxml/rapidxml%201.13/rapidxml-1.13.zip/download
                                "https://sourceforge.net/projects/rapidxml/files/rapidxml/rapidxml%20" +self.version +"/rapidxml-" +self.version +".zip/download",
                                "rapidxml-" +self.version +".zip", 
                                "rapidxml-" +self.version)

    def build(self):
        # header based library
        return True

    def is_build(self):
        return rb_install_include_file_exists("rapidxml.hpp")       

    def deploy(self):
        rb_deploy_header(rb_download_get_file(self, "rapidxml.hpp"))
        rb_deploy_header(rb_download_get_file(self, "rapidxml_iterators.hpp"))
        rb_deploy_header(rb_download_get_file(self, "rapidxml_print.hpp"))
        rb_deploy_header(rb_download_get_file(self, "rapidxml_utils.hpp"))





                
            



