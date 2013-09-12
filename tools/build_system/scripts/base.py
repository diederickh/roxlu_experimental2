import os
from sys import platform as _platform
from os.path import expanduser
import sys
import mimetypes
import shutil
import subprocess

from colorama import init, Fore, Back, Style
init()

mimetypes.init()

class Base(object): 
    # Global settings
    base_dir = ""         # path to the rbs.py file
    download_dir = ""
    script_dir = ""
    tools_dir = ""        # where perl/nasm/etc.. are stored 
    install_prefix = ""
    deploy_prefix = ""
    
    build_type = 0

    # Per script settings
    name = ""
    version = 0.0
    compilers = []
    arch = []
    dependencies = []

    # Compilers
    COMPILER_WIN_MSVC2010 = 1
    COMPILER_WIN_MSVC2012 = 2 
    COMPILER_MAC_GCC  = 3
    COMPILER_MAC_CLANG = 4

    # Build type
    BUILD_TYPE_DEBUG = 1
    BUILD_TYPE_RELEASE = 2

    # Architectures
    ARCH_M32 = 1
    ARCH_M64 = 2

    # Building specific settings
    include_dirs = []
    linker_dirs = []
    linker_libs = [] 
    
    def __init__(self):
        print version

    def download(self):
        print "Not implemented"

    def build(self):
        rb_red_ln("@todo implement build")

    def is_build(self):
        rb_red_ln("@todo implement build")

       

# download a source file into the download dir for the given script
def rb_download(script, url, outfile):
    rb_yellow_ln("Downloading: " +url)
    os.system("curl -L " +url +" -o " +rb_get_download_dir(script) +outfile)
    rb_green_ln("--------")

def rb_move_file(src, dest):
    #if os.path.exists(src) and not os.path.exists(dest):
    if os.path.exists(dest):
        rb_green_ln(dest)
        os.remove(dest)
    rb_yellow_ln(src +" --> " +dest)
    shutil.move(src, dest)

# make sure that the given directory exists
# recreate: when set to `True` we will first remove the directory if exists
def rb_ensure_dir(dir, recreate = False):
    if os.path.exists(dir) and recreate == True:
        shutil.rmtree(dir)

    if not os.path.exists(os.path.normpath(dir)):
        os.makedirs(os.path.normpath(dir))

# creates a directory in the given scripts download dir
def rb_ensure_download_dir(script, dir = None, recreate = False):
    if dir == None:
        rb_ensure_dir(rb_get_download_dir() +"/" +script.name +"/", recreate)
    else: 
        rb_ensure_dir(rb_get_download_dir() +"/" +script.name +"/" +dir, recreate)

def rb_ensure_tools_dir(dirname):
    dir = rb_get_tools_path() +dirname;
    rb_ensure_dir(dir)

# returns the directory into which the sources are downloaded
def rb_get_download_dir(script = None):
    if script is None:
        return os.path.abspath(Base.download_dir) +"/"
    else:
        return os.path.abspath(Base.download_dir +"/" +script.name) +"/"

# get the directory where the build scripts are stored; or the build script specific one when a script is given
def rb_get_script_dir(script = None):
    if script is None:
        return os.path.abspath(Base.script_dir)
    else:
        return os.path.abspath(Base.script_dir +"/" +script.name ) +"/"

# returns a path to a file in a script specific directory
# the script specificy directory is a dir in "scripts" with the same
# name as the script name, eg.. scripts/portaudio
# calling rb_script_get_file(self, "Makefile-x86_64.patch") will return the full path to [somepath]/scripts/portaudio/Makefile-x86_64.patch
def rb_script_get_file(script, file):
    return rb_get_script_dir(script) +file;

# return the full path to the download dir for the given script or just to the base download dir
def rb_get_download_path(script = None):
    if script is None:
        return os.path.abspath(Base.base_dir +"/" +Base.download_dir) +"/"
    else:
        return os.path.abspath(Base.base_dir +"/" +Base.download_dir +"/" +script.name ) +"/"


# extracts and copies the files from the extracted directory into the download dir of a script
def rb_extract(script, file, extractedDirName = None):
    t = mimetypes.guess_type(rb_get_download_dir(script) +file)
    f = None
    if t[0] == None:
        parts = file.split(".")
        if len(parts) >= 2:
            ext0 = parts[len(parts)-1]
            ext1 = parts[len(parts)-1]
            if ext0 == "tar" and ext1 == "gzip":
                f = "tar.gz"
            elif ext0 == "xz":
                f = "xz"
        else:
            rb_red_len("@todo we need to handle this type")

    elif t[0] == "application/x-tar" and t[1] == "gzip":
        f = "tar.gz"
    elif t[0] == "application/x-tar" and t[1] == "bzip2":
        f = "tar.bz2"
    else:
        print "Unknown file type"
        print t 
        sys.exit(2)


    if f == "tar.gz":
        os.system("cd " +rb_get_download_dir(script) + " && " +"tar -zxvf " +file )
    elif f == "tar.bz2":
        os.system("cd " +rb_get_download_dir(script) + " && " +"tar -jxvf " +file )
    elif f == "xz":
        if rb_is_win():
            tarfile = file.replace(".xz","")
            cmd = (
                "cd " +rb_get_download_dir(script),
                "xz -d " +file,
                "tar -xvf " +tarfile
                )
            rb_mingw_execute_shell_commands(script, cmd)
        

    if not extractedDirName == None:
        extracted_dir = rb_get_download_dir(script) +extractedDirName;
        if os.path.exists(extracted_dir):
            os.system("mv " +extracted_dir +"/* " +rb_get_download_dir(script) +"")

# clone the given git url into the download directory of the script when it doesnt exit
# eg. rb_git_clone(self, "git@github.com/glfw/glfw.git", "asdfwefsdfafasfasdfsdf")
def rb_git_clone(script, url, revision = None):
    if not os.path.exists(os.path.normpath(rb_get_download_dir(script))):
        rb_ensure_download_dir(script)
        cmd = ["cd " +rb_get_download_dir(script),
               "git clone " +url +" . "]
        if revision:
               cmd.append("git reset --hard " +revision)
        os.system(" && ".join(cmd))

# checks out a svn url
def rb_svn_checkout(script, url, revision = None):
    dd = rb_get_download_dir(script)

    if not os.path.exists(dd):

        rb_ensure_download_dir(script)

        cmd = (
            "cd " +dd,
            "svn co " +(" -r " +revision +" " if not revision == None else "") +url +" ."
            )
        rb_execute_shell_commands(script, cmd)
    
    
# script: eg. the jansson, glfw, etc.. script
# url: url to the file you want to download
# dest: the name of the file we downlaod (from the url)
# extractedDirName: the name of the directory after extracting
def rb_download_and_extract(script, url, dest, extractedDirName):
    if not rb_is_file_downloaded(script, dest):
        rb_ensure_dir(rb_get_download_dir(script))
        rb_download(script, url, dest)
        rb_extract(script, dest, extractedDirName)

# checks if all the necessary tools have been installed on windows systems
def rb_check_windows_setup():
    if not rb_is_win():
        return True

    nasm_path = rb_get_tools_path() +"\\nasm\\"
    perl_path = rb_get_tools_path() +"\\perl\\"
    mingw_path = rb_get_tools_path() +"\\mingw\\"

    error = False
    if not os.path.exists(nasm_path):
        error = True
        rb_red_ln("Make sure to install nasm in tools\\nasm\\")
    if not os.path.exists(perl_path):
        error = True
        rb_red_ln("Make sure to install perl (from ActiveState) in tools\\perl\\")
    if not os.path.exists(mingw_path):
        error = True
        rb_red_ln("Make sure to install MinGW to tools\\mingw\\")

    if not error:
        perl_version = subprocess.check_output(["perl", "--version"])
        if "activestate" not in perl_version.lower():
            rb_red_ln("You must install the ActiveState perl version")
            error = True

    if error:
        sys.exit()

# returns the compiler duolet
def rb_compiler_string(comp): 
    if comp == Base.COMPILER_MAC_GCC:
        return "mac-gcc"
    elif comp == Base.COMPILER_MAC_CLANG:
        return "mac-clang"
    elif comp == Base.COMPILER_WIN_MSVC2010:
        return "win-vs2010"
    elif comp == Base.COMPILER_WIN_MSVC2012:
        return "win-vs2012"

def rb_get_compiler_shortname():
    if Base.compiler == Base.COMPILER_MAC_GCC:
       return "gcc"
    elif Base.compiler == Base.COMPILER_WIN_MSVC2010:
        return "vs2010"
    elif Base.compiler == Base.COMPILER_WIN_MSVC2012:
        return "vs2012"
    elif Base.compiler == Base.COMPILER_MAC_CLANG:
        return "clang"
    return "none"

def rb_is_msvc():
    return Base.compiler == Base.COMPILER_WIN_MSVC2010 or Base.compiler == Base.COMPILER_WIN_MSVC2012

def rb_is_vs2010():
    return Base.compiler == Base.COMPILER_WIN_MSVC2010

def rb_is_vs2012():
    return Base.compiler == Base.COMPILER_WIN_MSVC2012

def rb_is_mac_gcc():
    return Base.compiler == Base.COMPILER_MAC_GCC    

def rb_is_mac_clang():
    return Base.compiler == Base.COMPILER_MAC_CLANG

def rb_is_clang():
    return rb_is_mac_clang()

def rb_is_gcc():
    return rb_is_mac_gcc()

def rb_is_debug():
    return Base.build_type == Base.BUILD_TYPE_DEBUG

def rb_is_release():
    return Base.build_type == Base.BUILD_TYPE_RELEASE

def rb_is_win():
    return rb_get_os_shortname() == "win"

def rb_is_mac():
    return rb_get_os_shortname() == "mac"

def rb_is_linux():
    return rb_get_os_shortname() == "linux"

def rb_is_unix():
    return rb_is_mac() or rb_is_linux()

def rb_is_32bit():
    return Base.arch == Base.ARCH_M32

def rb_is_64bit():
    return Base.arch == Base.ARCH_M64

def rb_get_copy_command():
    if rb_is_win():
        return "copy "
    elif rb_is_mac():
        return "cp "
    elif rb_is_linux():
        return "cp "

def rb_get_architecture_shortname():
    if Base.arch == Base.ARCH_M32:
        return "i386"
    elif Base.arch == Base.ARCH_M64:
        return "x86_64"
    else:
        return ""

def rb_get_os_shortname():
    if _platform == "linux" or _platform == "linux2":
        return "linux"
    elif _platform == "darwin":
        return "mac"
    elif _platform == "win32":
        return "win"
    
def rb_get_triplet():
    return rb_get_os_shortname() +"-" +rb_get_compiler_shortname() +"-" +rb_get_architecture_shortname()


def rb_solve_dependencies(script, scripts, result):
    for name in script.dependencies:
        sc = rb_find_script(scripts, name)
        if sc:
            result.append(sc)
            rb_solve_dependencies(sc, scripts, result)

        
# find a script object in 'scripts' with the given 'name'
def rb_find_script(scripts, name):
    for s in scripts:
        if s.name == name:
            return s
    return None

# the directory where the compiled libraries + headers are installed
def rb_install_get_dir():
    
    # debug build?
    flag = ""
    if Base.build_type == Base.BUILD_TYPE_DEBUG:
        flag = "d"

    return os.path.normpath(Base.install_prefix +"/" +rb_get_triplet() +flag) +"/"


# get the full path to a lib file for the current install/build dir
def rb_install_get_lib_file(filename):
    return os.path.normpath(rb_install_get_dir() +"lib/" +filename)

def rb_install_lib_file_exists(filename):
    return os.path.exists(os.path.normpath(rb_install_get_lib_file(filename)))

def rb_install_get_bin_file(filename):
    return os.path.normpath(rb_install_get_bin_dir() +"/" +filename)

def rb_install_bin_file_exists(filename):
    return os.path.exists(rb_install_get_bin_file(filename))


# get the full path to a header file for the current install/build dir
def rb_install_get_include_file(filename):
    return os.path.normpath(rb_install_get_dir() + "include/" +filename)

# the deploy dir is where all the compiled files are copied to using the script.copy() function
# this is different from the rb_install_get_dir(), as the rb_install_get_dir() is used as 
# --prefix when compiling/installing

def rb_deploy_get_dir():
    # debug build?
    flag = ""
    if Base.build_type == Base.BUILD_TYPE_DEBUG:
        flag = "d"

    return Base.deploy_prefix +"/" +rb_get_triplet() +flag + "/"

# if you library needs to find some includes, make sure to use this,
# and not e.g. rb_get_include_dir
def rb_deploy_get_include_dir():
    return os.path.normpath(rb_deploy_get_dir() +"include") +"/"

# if you need to add an extra library path in your build() function, 
# use this function to get the correct path for the current build
def rb_deploy_get_lib_dir():
    return rb_deploy_get_dir() +"lib/"
    
# get the include dir where all the headers are saved for the compiled scripts
# DO NOT USE FOR ADDING INCLUDE DIRS IN YOUR build() FUNCTION, your build needs to use the deployed dirs
def rb_install_get_include_dir():
    return rb_install_get_dir() +"/include/"

def rb_get_include_dir():
    rb_red_ln("THIS SHOULD BE RENAMED TO rb_install_get_include_dir")
    return rb_install_get_dir() +"/include/"

# get the lib dir where all the libs are saved for the compiled scripts
# DO NOT USE FOR ADDING LIB DIRS IN YOUR build() FUNCTION, your build needs to use the deployed dirs
def rb_install_get_lib_dir():
    return rb_install_get_dir() +"/lib/"

def rb_install_get_bin_dir():
    return rb_install_get_dir() +"/bin/"

# check if a lib file exists in the install directory; this can be used 
# to check if a file has been build
def rb_install_lib_exists(file):
    return os.path.exists(rb_install_get_lib_dir()+file)

def rb_get_lib_dir():
    rb_red_ln("THIS SHOULD BEE RENAMED TO rb_download_get_lib_dir")
    return rb_install_get_dir() +"/lib/"

def rb_get_cxxflags():
    # i386 is used by linker; c/cpp flags use -m32, -m64
    cf = ""
    if Base.arch == Base.ARCH_M32:
        cf = "-m32"
    elif Base.arch == Base.ARCH_M64:
        cf = "-m64"

    if rb_is_debug():
        cf += " -g -O0 "
            
    if rb_is_win():
        cf += " -I" +os.path.normpath(rb_deploy_get_include_dir()) +" "
    else:
        cf += " -I" +rb_install_get_include_dir() +" "

    return cf


def rb_get_cflags():
    cf = ""
    if Base.arch == Base.ARCH_M32:
        cf = "-m32 "
    elif Base.arch == Base.ARCH_M64:
        cf = "-m64 "

    if rb_is_debug():
        cf += " -g -O0 "
        
    # on windows we use the deploy as our local development dir, on unices we can use the install dir
    if rb_is_win():
        cf += " -I" +os.path.normpath(rb_deploy_get_include_dir()) +" "
    else:
        cf += " -I" +rb_install_get_include_dir() +" "

    return cf

def rb_get_cc():
    if rb_is_clang():
        return "clang"
    elif rb_is_gcc():
        return "gcc"
    else:
        return ""

    

def rb_get_cxx():
    if rb_is_clang():
        return "clang++"
    elif rb_is_gcc():
        return "g++"
    else:
        return ""

# when this function is called on windows, we assume mingw and we don't return -arch flag but use the defualt ones 
def rb_get_ldflags():
    ld = ""
    if rb_is_32bit():
        # @todo the linker arch option may have a different name; -m32/-m64
        if not rb_is_win():
            ld = "-arch i386 "
    elif rb_is_64bit():
        # @todo the linker arch option may have a different name; -m32/-m64
        if not rb_is_win():
            ld = "-arch x86_64 "

    # on windows we use the deploy dir as our local development root
    if rb_is_unix():
        ld += " -L" +rb_install_get_lib_dir() +" "
    elif rb_is_win():
        ld += " -L" +os.path.normpath(rb_deploy_get_lib_dir()) +" "

    return ld

def rb_get_cppflags():
    cf = ""
    if rb_is_debug():
        cf = "-DDEBUG "
    return cf

def rb_get_configure_options():
    return " CXXFLAGS=\"" +rb_get_cxxflags() +"\" CFLAGS=\"" +rb_get_cflags() +"\" LDFLAGS=\"" +rb_get_ldflags() +"\" CPPFLAGS=\"" +rb_get_cppflags() +"\""

def rb_get_configure_flags():
    return rb_get_configure_prefix_flag()

def rb_get_configure_prefix_flag():
   return " --prefix=\"" +rb_install_get_dir() +"\" "

# sometimes a make file does not use the environment CC and CXX flags; you can use this too, see the glew script
def rb_get_make_compiler_flags():
    return " CC='" +rb_get_cc() +"' CXX='" +rb_get_cxx() +"'"

# returns a dictionary with the environment build options that are used by autotools
# you can pass this into rb_execute_shell_commands
def rb_get_autotools_environment_vars():
    vars = { "CXXFLAGS"   : "\"" +rb_get_cxxflags()    +"\"", 
             "CFLAGS"     : "\"" +rb_get_cflags()      +"\"",
             "LDFLAGS"    : "\"" +rb_get_ldflags()     +"\"", 
             "CPPFLAGS"   : "\"" +rb_get_cppflags()    +"\"",
             "CC"         : "\"" +rb_get_cc()          +"\"",
             "CXX"        : "\"" +rb_get_cxx()         +"\"",
             "PKG_CONFIG_PATH" : "\"" +os.path.normpath(rb_install_get_lib_dir() +"pkgconfig") +"\""
             }


    if rb_is_mac():
        vars['PATH'] ="\"" +rb_install_get_bin_dir() +":${PATH}\""
#    vars['PKG_CONFIG_PATH'] = "\"" +rb_install_get_lib_dir() +"pkgconfig\""

    return vars

    
# script = the compile script instance (pass self)
# flags = extra flags we add to the ./configure command
# options = CPP/CXX etc.. options
# environmentVars = dictionary with additional environment vars we set. e.g. envvars = {"CC":"clang", "CXX":"clang++"} etc.. 

def rb_build_with_autotools(script, flags = None, options = True, environmentVars = None):
    # extra custom flags
    ef = "" if flags == None else flags

    # add the CXX,CPP,LDFLAGS etc..
    opts = "" if not options else  " " + rb_get_configure_options()

    cmd = []

    # merge environment vars
    env = {}
    if environmentVars:
        env = environmentVars

    auto_env = rb_get_autotools_environment_vars()
    for varname in auto_env:
        env[varname] = auto_env[varname]

    cmd.append("cd " +rb_get_download_dir(script))
    cmd.append("set -x && ./configure " +rb_get_configure_flags() +ef +" " +" " +opts)
    cmd.append("make clean && make && make install")
    rb_execute_shell_commands(script, cmd, env)


def rb_arch_string(arch):
    if arch == Base.ARCH_M32:
        return "32"
    elif arch == Base.ARCH_M64:
        return "64"
    else:
        return "-"

def rb_is_file_downloaded(script, file):
    return os.path.isfile(rb_get_download_dir(script) + file)

# will merge the given commands with environment vars; based on the OS/shell we will set 
# the environment vars
# style: 0 = platform specific
# style: 1 = use "export"
def rb_merge_shell_commands_with_envvars(commands, envvars, style = 0):
    # make sure we have a list
    cmd_input = list(commands)
    cmd = []

    if style == 0:
        if rb_is_mac():
            style = 1

    # add extra environment vars
    if envvars:
        for varname in envvars:
            if style == 1:
                cmd.append("export " +varname +"=" +envvars[varname])
            else:
                rb_red_ln("error: setting environment vars not working with autotools on this platform yet")

    for el in cmd_input:
        cmd.append(el)
        
    return cmd

# environmentVars: dictionary with environment vars we set
def rb_execute_shell_commands(script, commands, environmentVars = None):
    
    cmd = rb_merge_shell_commands_with_envvars(commands, environmentVars)

    # create the shell script
    if rb_get_os_shortname() == "win":
        f = open("tmp.bat", "w+")
        f.write("\n".join(cmd))
        f.close()
        subprocess.call("tmp.bat")
    else:
        d = rb_get_base_path()
        f = open(d + "tmp.sh", "w+")
        f.write("\n".join(cmd))
        f.close()
        os.chmod(d + "tmp.sh", 0777)
        os.system(d + "tmp.sh")


# sets path for e.g. nasm, perl etc..
def rb_set_environment_vars():
    if rb_get_os_shortname() == "win":
        env_paths = (
            os.path.normpath(rb_get_tools_path()+"perl/perl/bin/"),
            os.path.normpath(rb_get_tools_path()+"nasm/")
        )

        env_includes = (
            os.path.normpath(rb_deploy_get_dir() +"include/")
        )

        os.environ["PATH"] += ";" +";".join(env_paths)
        os.environ["INCLUDE"] += ";" +";".join(env_includes)
        rb_green_ln(os.environ["PATH"])
    elif rb_is_mac():
        env_paths = (
            rb_install_get_bin_dir()
        )
        os.environ["PATH"] += ";" +";".join(env_paths)

def rb_get_tools_path():
    return Base.base_dir +Base.tools_dir +"/"

def rb_get_base_path():
    return Base.base_dir

# check if a file exists in the tool dir
def rb_tools_file_exists(file):
    src = rb_get_tools_path() +file;
    return os.path.exists(src)

# Copies a file from the script (sources) dir to the download dir for the given script
# The file is copied from scripts/[script.name]/[file], to downloads/[script.name], or 
# the other destdir given
# eg. rb_copy_to_download_dir(self, "libFLAC_dynamic.vcxproj", dd +"src/libFLAC/")
def rb_copy_to_download_dir(script, src, destdir = None):
    s = rb_get_script_dir(script) +"/" +src
    if not os.path.exists(s):
        rb_red_ln("Cannot find the file: " +src)

    d = src
    if destdir:
        d = destdir +src
    else:
        d = rb_get_download_dir(script) +src

    if not os.path.exists(d):
        rb_red_ln(s)
        shutil.copyfile(s, d)
        rb_yellow_ln("Copied " +d)

# this will copy one directory from a downlaod dir the one given (all inside
# the same dir of the given script's directory. Quite some libraries provide
# a VS2010 project which we need to copy and then upgrade to VS2012; this
# helps you to copy that directory
# e.g. see the vorbis script for an example
def rb_download_dir_copy_internal(script, src, dest):
    dd = rb_get_download_dir(script)
    src = dd +src
    dest = dd +dest
    if not os.path.exists(dest):
        shutil.copytree(src, dest)

# copy one file from the download dir of the given script to the other file
# rb_download_dir_copy_file_internal(self, "jconfig.vc", "jconfig.h")
def rb_download_dir_copy_file_internal(script, src, dest):
    dd = rb_get_download_dir(script)
    src = os.path.normpath(dd +src)
    dest = os.path.normpath(dd +dest)
    rb_yellow_ln(src +" --> " +dest)
    os.system(rb_get_copy_command() +" " +src +" " +dest)

# returns a file relative to the download dir for the given script
def rb_download_get_file(script, file):
    return rb_get_download_dir(script) +file;

# remove a directory from a script specific download dir
# this will not remove the download dir itself; but only a 
# subdir of the download dir for the given script; this
# might be handy if you need to clear caches between 
# builds
def rb_remove_download_dir(script, dir):
    d = rb_get_download_dir(script) +"/" +dir
    if os.path.exists(d):
        shutil.rmtree(d)
    else:
        rb_red_ln("Cannot remove dir because we didn't find it " +d)

# Deploying is the processing of copying the generated files, such as
# dylibs, static libs, dll, headers, etc.. to the correct deploy dir
# This is similar to the install dir/files, but this contains only a 
# part of the install dir
# ---------------------------------------------------------------------------

def rb_deploy_dll(dll):
    if os.path.exists(dll):
        d = rb_deploy_get_dir() +"/bin/"
        rb_ensure_dir(d)
        #shutil.copyfile(os.path.normpath(dll), os.path.normpath(d))
        os.system("copy " +os.path.normpath(dll) +" " +os.path.normpath(d))
        rb_yellow_ln(dll)
    else:
        rb_red_ln("File not found " +dll)

def rb_deploy_lib(lib):
    to_copy = lib
    if  "*" in lib:
        to_copy = lib 
    elif not os.path.exists(lib):
        rb_red_ln("File not found " +lib)
        return 


    d = rb_deploy_get_dir() +"/lib/"
    rb_ensure_dir(d)
    #shutil.copyfile(os.path.normpath(dll), os.path.normpath(d))
    os.system(rb_get_copy_command()  +os.path.normpath(to_copy) +" " +os.path.normpath(d))
    rb_yellow_ln(to_copy +" >> " +os.path.normpath(to_copy) +" " +os.path.normpath(d))


# copy one specific header
# rb_deploy_header(rb_install_get_include_file("x264.h"))
def rb_deploy_header(hdr, subdir = None):
    if os.path.exists(hdr):
        sd = ""
        if not subdir == None:
            sd = subdir +"/"
        d = rb_deploy_get_dir() +"/include/" +sd
        rb_ensure_dir(d)
        #shutil.copyfile(os.path.normpath(dll), os.path.normpath(d))
        os.system(rb_get_copy_command() +os.path.normpath(hdr) +" " +os.path.normpath(d))
        rb_yellow_ln(hdr)
    else:
        rb_red_ln("File not found " +hdr)

# copy all .h files from the given directory
# eg. rb_deploy_headers("/some/path/")
# eg. rb_deploy_headers("/some/path/openssl/", subdir="openssl")  // copy to the deploy dir: include/openssl/
# eg. rb_deploy_headers(dir = rb_install_get_include_dir() +"ogg", subdir = "ogg")
def rb_deploy_headers(dir, files = None, subdir = None):    
    if os.path.exists(dir):

        sd = ""
        if not subdir == None:
            sd = subdir +"/"

        d = rb_deploy_get_dir() +"/include/" +sd
        rb_ensure_dir(d)

        #shutil.copyfile(os.path.normpath(dll), os.path.normpath(d))
        if files == None:
            if rb_is_win():
                os.system("xcopy /y " +os.path.normpath(dir +"/*.h") +" " +os.path.normpath(d))
                rb_yellow_ln("xcopy /y " +os.path.normpath(dir +"\*.h") +"  " +os.path.normpath(d))
                rb_yellow_ln(dir)
            else:
                os.system("cp -r " +os.path.normpath(dir) +"/ " +os.path.normpath(d)) 

        else:
            for f in files:
                rb_deploy_header(dir +"/" +f, subdir)

    else:
        rb_red_ln("Headers dir not found " +dir)


def rb_deploy_create_headers_dir(dir):
    dd = rb_deploy_get_dir() +"/include/" +dir
    if not os.path.exists(dd):
        rb_ensure_dir(dd)

def rb_deploy_get_lib_file(filename):
    return rb_deploy_get_lib_dir() +filename;

def rb_deploy_lib_file_exists(filename):
    rb_yellow_ln(os.path.normpath(rb_deploy_get_lib_file(filename)))
    return os.path.exists(os.path.normpath(rb_deploy_get_lib_file(filename)))

# Console output
# ---------------------------------------------------------------------------

def rb_print_script_info(script):
    rb_green(script.name.ljust(10))                                            # name 
    rb_yellow(" " +script.version + " ")                                       # version
    rb_gray("(" +", ".join(map(rb_arch_string, script.arch)) +")")             # architectures
    rb_gray(", (" +", ".join(map(rb_compiler_string, script.compilers)) +")")  # compilers
    sys.stdout.write("\n")

def rb_red(s):
    sys.stdout.write(Style.BRIGHT +Fore.MAGENTA +s +Style.RESET_ALL)
    
def rb_red_ln(s):
    rb_red(s +"\n")

def rb_green(s):
    sys.stdout.write(Style.BRIGHT +Fore.GREEN +s +Style.RESET_ALL)

def rb_green_ln(s):
    rb_green(s +"\n")

def rb_yellow(s):
    sys.stdout.write(Style.BRIGHT +Fore.YELLOW +s +Style.RESET_ALL)

def rb_yellow_ln(s):
    rb_yellow(s +"\n")

def rb_white(s):
    sys.stdout.write(Style.BRIGHT +Fore.WHITE +s +Style.RESET_ALL)

def rb_white_ln(s):
    rb_white(s +"\n")

def rb_gray(s):
    sys.stdout.write(Fore.WHITE +s +Style.RESET_ALL)

def rb_gray_ln(s):
    rb_gray(s +"\n")

def rb_print_usage():
    rb_green("rbs.py -a <arch:32,64> -t <task:list,build,download> -c <compiler-shortname:vs2010,vs2012,gcc,clang> -b<build_type:release,debug> -s<scriptname>\n")



# Finding compilers
# ---------------------------------------------------------------------------
def rb_vs2010_is_installed():
    return len(rb_vs2010_get_path()) > 0

def rb_vs2012_is_installed():
    return len(rb_vs2012_get_path()) > 0

def rb_vs2010_get_path():
    paths = [r"C:\Program Files (x86)\Microsoft Visual Studio 10.0"]
    for p in paths:
        if os.path.exists(p):
            return p;
    return ""

def rb_vs2012_get_path():
    paths = ["C:\\Program Files (x86)\\Microsoft Visual Studio 11.0"]
    for p in paths:
        if os.path.exists(p):
            return p;
    return ""

def rb_msvc_get_toolset_flag():
   if rb_is_vs2010():
       return " /property:PlatformToolset=v100 "
   elif rb_is_vs2012():
       return " /property:PlatformToolset=v110 "

def rb_msvc_get_msbuild_type_flag():
    if Base.compiler == Base.COMPILER_WIN_MSVC2010:
        return rb_vs2010_get_msbuild_type_flag()
    elif  Base.compiler == Base.COMPILER_WIN_MSVC2012:
        return rb_vs2012_get_msbuild_type_flag()

def rb_vs2012_get_msbuild_type_flag():
    if Base.build_type == Base.BUILD_TYPE_DEBUG:
        return "/p:configuration=Debug "
    elif Base.build_type == Base.BUILD_TYPE_RELEASE:
        return "/p:configuration=Release"
    else:
        rb_red("Error: not build flag for this...")
        return ""
       
def rb_vs2010_get_msbuild_type_flag():
    if Base.build_type == Base.BUILD_TYPE_DEBUG:
        return "/p:configuration=Debug "

    elif Base.build_type == Base.BUILD_TYPE_RELEASE:
        return "/p:configuration=Release"
    else:
        rb_red_ln("Error: not build flag for this...")
        return ""

# this function will try to upgrade the solution (slndir/sln) to an
# vs2010 version using: "devenv solution.sln /upgrade"
# see the vorbis script for an example
def rb_vs2010_upgrade_to_vs2012(script, slndir, sln):
    sln_file = slndir +"/" +sln
    if not os.path.exists(sln_file):
        rb_red_ln("Cannot find the solution file: " +sln_file)
        return False
    
    convert = (
        "call " +rb_msvc_get_setvars(), 
        "cd " +slndir,
        "devenv " +sln +" /upgrade"
    )

    rb_execute_shell_commands(script, convert)
    
def rb_msvc_setup_build_environment():
    # nasm
    rb_set_environment_vars()

    # add the deploy include dir so libs can find the installed headers
    os.environ["INCLUDE"] += ";" +rb_deploy_get_include_dir() 
    
# experimental; it seems the INCLUDE is not always used (didn't work when compiling flac)
def rb_msvc_get_environment_vars():
    env = (
        "SET CL=/I" +rb_deploy_get_include_dir() +" /Z7",
#        "SET INCLUDE=" +rb_deploy_get_include_dir() +";%INCLUDE%"
        )
    return env



def rb_msvc_get_setvars():
    if Base.compiler == Base.COMPILER_WIN_MSVC2010:
        return Base.base_dir +"/tools/vs2010_vcvars32.bat"
    elif Base.compiler == Base.COMPILER_WIN_MSVC2012:
        return Base.base_dir +"/tools/vs2012_vcvars32.bat"
    else:
        rb_red_ln("rb_msvc_get_setvars() cannot find vars file")

def rb_msvc_get_build_type_string():
    if Base.build_type == Base.BUILD_TYPE_DEBUG:
        return "Debug"
    elif Base.build_type == Base.BUILD_TYPE_RELEASE:
        return "Release"
    else:
        rb_red_ln("No build type string for this msvc build type")

# copies the custom visual studio project from the sub-scriptdir for the given sript
# the custom projects should exist in a vs2010 or vs2012 dir
# eg. rb_msvc_copy_custom_project(self, rb_get_download_dir(self) +"/vs2010")
# eg. rb_msvc_copy_custom_project(self, rb_get_download_dir(self) +"/vs2012")
# eg. rb_msvc_copy_custom_project(self, rb_get_download_dir(self) +"/" +rb_get_compiler_shortname())
def rb_msvc_copy_custom_project(script, dest):
    rb_yellow_ln(dest)
    if not os.path.exists(dest):
        src = rb_get_script_dir(script) +"/" +rb_get_compiler_shortname()
        shutil.copytree(os.path.normpath(src), os.path.normpath(dest))


# MingW helpers
# ---------------------------------------------------------------------------

def rb_mingw_windows_path_to_cygwin_path(path):
    return "/cygdrive" +rb_mingw_windows_path_to_mingw_path(path)

def rb_mingw_windows_paths_to_cygwin_paths(paths):
    result = []
    for p in paths:
        result.append(rb_mingw_windows_path_to_cygwin_path(os.path.normpath(p)))
    return result

# converts a windows style dir/path to mingw path
# e.g. c:\roxlu\tools\build_system\
#      /c/roxlu/tools/build_system
def rb_mingw_windows_path_to_mingw_path(path): 
    fullpath = "/" +os.path.abspath(path)
    fullpath = fullpath.replace(":","");
    fullpath = fullpath.replace("\\", "/")
    return fullpath

# converts an array with paths to mingw like paths    
def rb_mingw_windows_paths_to_mingw_paths(paths):
    result = []
    for p in paths:
        result.append(rb_mingw_windows_path_to_mingw_path(os.path.normpath(p)))
    return result

# get the path to the yasm.exe dir that we should use in our PATH variable
def rb_mingw_get_yasm_path():
    if not rb_is_win():
        return ""
    if rb_is_32bit():
        return rb_get_tools_path() +"yasm\\win32\\"
    elif rb_is_64bit():
        return rb_get_tools_path() +"yasm\\win64\\"
    else:
        rb_red_ln("No yasm path for other then 32 and 64 bit")
        return ""

def rb_mingw_build_with_autotools(script, flags = None):
    ef = flags if flags else ""
    auto_env = rb_get_autotools_environment_vars()
    cmd = [
        "cd " +rb_mingw_windows_path_to_cygwin_path(os.path.abspath(rb_get_download_dir(script))),
        "./configure " +rb_get_configure_flags() +" " +ef,
        "make clean",
        "make",
        "make install"
        ]
    rb_mingw_execute_shell_commands(script, cmd, auto_env)


#def rb_mingw_get_msys_bin_path():
#    return os.path.normpath(rb_get_tools_path() +"msys\\bin") +"\\"

def rb_mingw_get_mingw_base_path():
    return os.path.normpath(rb_get_tools_path() +"mingw\\mingw32") +"\\"

def rb_mingw_get_mingw_bin_path():
    return os.path.normpath(rb_mingw_get_mingw_base_path() +"bin") +"\\"

def rb_mingw_get_cygwin_bin_path():
    return os.path.normpath(rb_get_tools_path() +"cygwin\\bin") +"\\"


# EXPERIMENTAL
def rb_mingw_create_pkgconfig_file(name, version, ldflags):
    str = (
        "prefix=" +rb_deploy_get_dir(),
        "exec_prefix=${prefix}",
        "libdir=${prefix}/lib",
        "includedir=${prefix}/include",
        "",
        "Name:" +name,
        "Description: " +name,
        "Version: " +version, 
        "Libs:-L${exec_prefix}/lib " +ldflags,
        "Cflags: -I${exec_prefix}/include"
           )

    fname = rb_mingw_get_pkgconfig_script_path() +name +".pc"
    f = open(fname, "w+")
    f.write("\n".join(str))
    f.close()
    rb_yellow_ln("\n".join(str))

def rb_mingw_get_pkgconfig_script_path():
    return os.path.normpath(rb_install_get_lib_dir() +"/pkgconfig") +"\\"

# run commands in a mingw shell where all mingw compilers and paths are available
# see the x264 which is the first script that uses this. we are using cygwin and 
# mingw32-w64 and make sure that all environment vars are setup for you
def rb_mingw_execute_shell_commands(script, commands, envvars = None):

    cmd = list(commands)

    curr_path = os.environ["PATH"] 

    # Make sure that we only use our installed mingw version (changing PATH here)
    yasm_path = rb_mingw_get_yasm_path()
#   mingw_base_dir = rb_mingw_get_mingw_base_path()
#   mingw_bin_dir =  rb_mingw_get_mingw_bin_path()
    cygwin_bin_dir = rb_mingw_get_cygwin_bin_path()
    install_dir = os.path.normpath(rb_install_get_bin_dir())

    env_paths = [
        cygwin_bin_dir,
#        mingw_base_dir,
#        mingw_bin_dir,
        yasm_path,
        install_dir
        ]

    mingw_paths = rb_mingw_windows_paths_to_cygwin_paths(env_paths)
    new_mingw_path = ":".join(mingw_paths)
    new_win_path = ";".join(env_paths);

    cmd.insert(0, "export PATH=" +new_mingw_path +"")

    base_commands = (
        "SET PATH=" +new_win_path +"",
        "SET SHELLOPTS=igncr",
        cygwin_bin_dir +"sh.exe -c \"./tmp.sh\"",
        "SET PATH=" +curr_path
        )

    cmd = rb_merge_shell_commands_with_envvars(cmd, envvars, 1)

    # create the shell script
    if rb_is_win():
        d = rb_get_base_path()

        # Just a tiny wrapper which makes sure that our `cmd` (commands) get execute by a `sh` shell
        f = open(d + "tmp.bat", "w+")
        f.write("\n".join(base_commands))
        f.close()
        os.chmod(d + "tmp.bat", 0777)
        
        # tmp.sh contains the shell commands
        msf = open(d +"tmp.sh", "w+")
        msf.write("\n".join(cmd))
        msf.close()

        subprocess.call("tmp.bat")

    else:
        rb_red_ln("rb_minw_execute_shell_commands is not support for non-win platforms")
    

# CMake helpers
# ---------------------------------------------------------------------------

# build, after calling rb_cmake_configure(), the target is the target you want to build;
# for most cases you can leave target "install"
def rb_cmake_build(script, target = "install"):
    
    # Create the cmake command
    cmd = rb_cmake_get_executable() +" --build . --target  " +target
    if Base.build_type == Base.BUILD_TYPE_RELEASE: 
        cmd += " --config Release "
    elif Base.build_type == Base.BUILD_TYPE_DEBUG:
        cmd += " --config Debug "
        
    if rb_is_msvc():
        commands = [
            "cd " +rb_get_download_dir(script) +rb_get_cmake_configure_dir(), 
            "call " +os.path.normpath(rb_msvc_get_setvars()),
            cmd
        ]
        rb_execute_shell_commands(script, commands)
    else:
        commands = [
            "cd " +rb_get_download_dir(script) +rb_get_cmake_configure_dir(), 
            cmd
        ]
        rb_execute_shell_commands(script, commands)


        
# configure using cmake using the current compiler, bits/arch, etc..
# opts is a list with custom options: ["-DBUILD_SHARED_LIBS=1", "--target install", "--config release"]
def rb_cmake_configure(script, opts = None):
    
    # make sure that the specific build dir for cmake exists
    rb_ensure_download_dir(script, rb_get_cmake_configure_dir()) 
    dd = rb_get_download_dir(script)
    dcmake = dd +rb_get_cmake_configure_dir()
    
    # the cmake command line command
    cmake_config = rb_cmake_create_configure_command(script, opts)
    cmake_config.append("..")
    cmake_command = " ".join(cmake_config)

    # configure for msvc
    if rb_is_msvc():
        cmd = [
            "call " +os.path.normpath(rb_msvc_get_setvars()),
            "cd " +dcmake,
            cmake_command
        ]
        rb_execute_shell_commands(script, cmd)
    else:
        cmd = [
            "cd " +dcmake,
            cmake_command
            ]
        rb_execute_shell_commands(script, cmd, rb_get_autotools_environment_vars())
      

    return cmd
    #rb_execute_shell_commands(script, cmd)
    """
    rb_ensure_download_dir(script, rb_get_cmake_configure_dir()) #, recreate=True)
    os.chdir(os.path.abspath(rb_get_download_dir(script)+ "/" +rb_get_cmake_configure_dir()));
    cmd = rb_cmake_create_configure_command(script, opts)
    cmd.append("..")
    subprocess.call(cmd)
    """

def rb_cmake_get_executable():
    if rb_is_win():
        return "cmake.exe"
    else:
        return "cmake"

def rb_get_cmake_configure_dir():
    flag = ""
    if Base.build_type == Base.BUILD_TYPE_DEBUG:
        flag = "d"
        
    return "compile_with_cmake_" +rb_get_triplet() +flag

# create a list that can be passed into subprocess.call() to execute a cmake configure
# process. we add the architecture, generator and install prefix flags
# opts: custom arguments
def rb_cmake_create_configure_command(script, opts = None):
    cmd = [rb_cmake_get_executable()]
    rb_cmake_append_architecture_flag(cmd)
    rb_cmake_append_install_prefix_flag(cmd)
    rb_cmake_append_build_type_flag(cmd)
    rb_cmake_append_generator_flag(cmd)
    if not opts == None:
        cmd = cmd + opts
    return cmd

def rb_cmake_append_architecture(con):
    con.append(rb_cmake_get_architecture_flag())

def rb_cmake_append_install_prefix_flag(con):
    con.append("-DCMAKE_INSTALL_PREFIX=" +os.path.normpath(rb_install_get_dir()))

def rb_cmake_append_generator_flag(con):
    if len(rb_cmake_get_generator_name()) > 0: 
        con.append("-G \"" +rb_cmake_get_generator_name() +"\"")
        

def rb_cmake_append_architecture_flag(con):
    con.append(rb_cmake_get_architecture_flag())

def rb_cmake_append_build_type_flag(con):
    if len(rb_cmake_get_build_type_flag()) > 0:
        con.append(rb_cmake_get_build_type_flag())

def rb_cmake_get_build_type_flag():
    if Base.build_type == Base.BUILD_TYPE_DEBUG:
        return " -DCMAKE_BUILD_TYPE=Debug "
    elif Base.build_type == Base.BUILD_TYPE_RELEASE:
        return " -DCMAKE_BUILD_TYPE=Release "
    else:
        rb_red(" Unhandled build type for cmake \n")
        return ""
        
# returns the cmake flag for the current set architecture
# on windows with msvc, the architeture flag is combined in the
# generator name
def rb_cmake_get_architecture_flag():
    if rb_get_os_shortname == "mac":
        if Base.arch == Base.ARCH_M32:
            return  " -DCMAKE_OSX_ARCHITECTURES=i386 "
        elif Base.arch == Base.ARCH_M64:
            return " -DCMAKE_OSX_ARCHITECTURES=x86_64 "
    return ""

# return the generator for the currently set compiler
# on windows,the generator contains the architure too
def rb_cmake_get_generator_name():
    if Base.compiler == Base.COMPILER_WIN_MSVC2010 and rb_vs2010_is_installed():
        if Base.arch == Base.ARCH_M64:
            return "Visual Studio 10 Win64"
        else:
            return "Visual Studio 10"
    elif Base.compiler == Base.COMPILER_WIN_MSVC2012 and rb_vs2012_is_installed():
        if Base.arch == Base.ARCH_M64:
            return "Visual Studio 11 Win64"
        else:
            return "Visual Studio 11"

    return ""

def rb_cmake_get_install_prefix():
    return " -DCMAKE_INSTALL_PREFIX='" +os.path.normpath(rb_install_get_dir()) +"' "

