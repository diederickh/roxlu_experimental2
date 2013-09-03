#!/usr/bin/env python 

import os
import sys, getopt
sys.path.append("./libs/")

from scripts.glfw import GLFW
from scripts.base import *
from scripts.jansson import Jansson
from scripts.jpeg import JPEG
from scripts.tiff import Tiff
from scripts.png import PNG
from scripts.zlib import ZLib
from scripts.openssl import OpenSSL
from scripts.lamemp3 import LameMP3
from scripts.yasm import Yasm
from scripts.uv import UV
from scripts.curl import Curl
from scripts.pcre import PCRE
from scripts.ogg import Ogg
from scripts.vorbis import Vorbis
from scripts.theora import Theora
from scripts.speex import Speex
from scripts.mysql_c_connector import MySQLCConnector
from scripts.freetype import FreeType
from scripts.autoconf import AutoConf
from scripts.automake import AutoMake
from scripts.libtool import LibTool
from scripts.x264 import x264
from scripts.glew import Glew
from scripts.portaudio import PortAudio
from scripts.sndfile import SndFile
from scripts.pkgconfig import PkgConfig
from scripts.glib import Glib
from scripts.ffi import FFI
from scripts.gettext import GetText
from scripts.iconv import Iconv
from scripts.flac import Flac
from scripts.rtmp import Rtmp

from scripts.roxlu import Roxlu

from colorama import init, Fore, Back, Style
init()

TASK_LIST = 1
TASK_BUILD = 2
TASK_DOWNLOAD = 3

Base.base_dir = os.path.dirname(os.path.realpath(__file__)) +"/"
Base.download_dir = "./downloads"
Base.script_dir = "./scripts"
Base.tools_dir = "./tools"
Base.compiler = Base.COMPILER_MAC_CLANG
Base.arch = Base.ARCH_M32
Base.install_prefix = Base.base_dir +"build"
Base.deploy_prefix = Base.base_dir +"../../extern/"
Base.build_type  = Base.BUILD_TYPE_RELEASE

ins_glfw = GLFW()
ins_jansson = Jansson()
ins_jpeg = JPEG()
ins_tiff = Tiff()
ins_png = PNG()
ins_zlib = ZLib()
ins_openssl = OpenSSL()
ins_lamemp3 = LameMP3()
ins_yasm = Yasm()
ins_uv = UV()
ins_curl = Curl()
ins_pcre = PCRE()
ins_ogg = Ogg()
ins_vorbis = Vorbis()
ins_theora = Theora()
ins_speex = Speex()
ins_mysqlc = MySQLCConnector()
ins_freetype = FreeType()
ins_autoconf = AutoConf()
ins_automake = AutoMake()
ins_libtool = LibTool()
ins_x264 = x264()
ins_glew = Glew()
ins_portaudio = PortAudio()
ins_sndfile = SndFile()
ins_pkgconfig = PkgConfig()
ins_glib = Glib()
ins_ffi = FFI()
ins_gettext = GetText()
ins_iconv = Iconv()
ins_flac = Flac()
ins_roxlu = Roxlu()
ins_rtmp = Rtmp()

installers = [ins_glfw, ins_jansson, ins_jpeg, ins_tiff, ins_png, ins_zlib, 
              ins_openssl, ins_lamemp3, ins_yasm, ins_uv, ins_curl, ins_pcre,
              ins_ogg, ins_vorbis, ins_theora, ins_speex, ins_mysqlc,
              ins_freetype, ins_autoconf, ins_automake, ins_libtool, ins_x264,
              ins_glew, ins_portaudio, ins_sndfile, ins_pkgconfig, ins_glib, ins_ffi,
              ins_gettext, ins_iconv, ins_flac, ins_rtmp,
              ins_roxlu]

#installers.sort(key=lambda i:i.name)

if rb_is_win():
    os.environ["PATH"] = os.environ["PATH"] +";" +Base.base_dir +"tools\\curl\\";


# State vars; get set by getopt
installer = None
task = None             # what task do you want to perform

# On windows systems we need to check if perl and nasm have been installed
rb_check_windows_setup()

# Getopts
try:
    opts,args = getopt.getopt(sys.argv[1:], "a:s:t:c:b:", ["arch=", "script=", "task=", "compiler=","build_type="])
except getopt.GetoptError:
    rb_print_usage()
    sys.exit(2)

# Handle arguments
for opt, arg in opts:
    if opt in ("-a", "--arch"):
        if arg == "32":
            Base.arch = Base.ARCH_M32
        elif arg == "64":
            Base.arch = Base.ARCH_M64
    elif opt in ("-s", "--script"):
        for ins in installers:
            if ins.name == arg:
                installer = ins
    elif opt in ("-t", "--task"):
        if arg == "list":
            task = TASK_LIST
        elif arg == "build":
            task = TASK_BUILD
        elif arg == "download":
            task = TASK_DOWNLOAD
        else:
            print "Unknown task: " +arg
            sys.exit(2)
    elif opt in ("-b", "--build_type"):
        if arg == "release":
            Base.build_type = Base.BUILD_TYPE_RELEASE
        elif arg == "debug":
            Base.build_type = Base.BUILD_TYPE_DEBUG
        else:
            rb_red("Unknown build type " +arg +"\n")

    elif opt in ("-c", "--compiler"):
        if arg == "vs2010":
            Base.compiler = Base.COMPILER_WIN_MSVC2010
        elif arg == "vs2012":
            Base.compiler = Base.COMPILER_WIN_MSVC2012
        elif arg == "gcc":
            if rb_is_mac():
                Base.compiler = Base.COMPILER_MAC_GCC
        elif arg == "clang":
            if rb_is_mac():
                Base.compiler = Base.COMPILER_MAC_CLANG
        else:
            rb_red("No compiler found.\n")
            sys.exit(2)




if task == None:
    rb_print_usage()
    sys.exit(2)

if task == TASK_BUILD:
    if not installer:
        print "No installer found"
        sys.exit(2)

    # build dependencies
    rs = []
    rb_solve_dependencies(installer, installers, rs)
    rs = rs[::-1]
    for r in rs:
        if not r.is_build():
            rb_red_ln("Found dependency: "+r.name)
            r.build()
            r.deploy()

    installer.build()
    installer.deploy()

elif task == TASK_LIST:
    print ""
    for ins in installers:
        rb_print_script_info(ins)

         #print Fore.RED +ins.name +" - " +ins.version;
elif task == TASK_DOWNLOAD:
    for ins in installers:
        ins.download()



"""
for ins in installers:
    print ins.version


def rbs_download(installers):
    for ins in installers:
        ins.download()

def rbs_build(installers):
    for ins in installers:
        ins.build()

# rbs_download(installers)
rbs_build([ins_glfw])
"""

"""
class aap:
    name ="tester"

a = aap()

x = scripts.glfw()
#__import__("scripts.glfw")
scripts = os.listdir("./scripts")
for d in scripts:
    script_dir = "./" +d +"/" +d +".py"
    print script_dir
    #imp.load_source(d, script_dir)




#for dirname, dirnames, filenames in os.walk("./scripts"):
#    print dirname


"""
