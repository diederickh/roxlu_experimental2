import os
from sys import platform as _platform
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

       

# download a source file into the download dir for the given script
def rb_download(script, url, outfile):
    os.system("curl -L " +url +" -o " +rb_get_download_dir(script) +outfile)

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

# returns the directory into which the sources are downloaded
def rb_get_download_dir(script = None):
    if script is None:
        return Base.download_dir
    else:
        return Base.download_dir +"/" +script.name +"/"

# get the directory where the build scripts are stored; or the build script specific one when a script is given
def rb_get_script_dir(script = None):
    if script is None:
        return Base.script_dir
    else:
        return Base.script_dir +"/" +script.name +"/"

# return the full path to the download dir for the given script or just to the base download dir
def rb_get_download_path(script = None):
    if script is None:
        return Base.base_dir +"/" +Bsse.download_dir
    else:
        return Base.base_dir +"/" +Base.download_dir +"/" +script.name +"/"


# extracts and copies the files from the extracted directory into the download dir of a script
def rb_extract(script, file, extractedDirName = None):
    t = mimetypes.guess_type(rb_get_download_dir(script) +file)
    f = None

    if t[0] == "application/x-tar" and t[1] == "gzip":
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

    error = False
    if not os.path.exists(nasm_path):
        error = True
        rb_red_ln("Make sure to install nasm in tools\\nasm\\")
    if not os.path.exists(perl_path):
        error = True
        rb_red_ln("Make sure to install perl (from ActiveState) in tools\\perl\\")
    
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
    elif Base.compiler == Base.COMPILER_CLANG:
        return "clang"
    return "none"

def rb_is_msvc():
    return Base.compiler == Base.COMPILER_WIN_MSVC2010 or Base.compiler == Base.COMPILER_WIN_MSVC2012

def rb_is_vs2010():
    return Base.compiler == Base.COMPILER_WIN_MSVC2010

def rb_is_vs2012():
    return Base.compiler == Base.COMPILER_WIN_MSVC2012

def rb_is_macgcc():
    return Base.compiler == Base.COMPILER_MAC_GCC    

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

# the directory where the compiled libraries + headers are installed
def rb_install_get_dir():
    
    # debug build?
    flag = ""
    if Base.build_type == Base.BUILD_TYPE_DEBUG:
        flag = "d"

    return Base.install_prefix +"/" +rb_get_triplet() +flag + "/"


# get the full path to a lib file for the current install/build dir
def rb_install_get_lib_file(filename):
    return rb_install_get_dir() +"lib/" +filename

# get the full path to a header file for the current install/build dir
def rb_install_get_include_file(filename):
    return rb_install_get_dir() + "include/" +filename

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
    return rb_deploy_get_dir() +"include/"

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

def rb_get_lib_dir():
    rb_red_ln("THIS SHOULD BEE RENAMED TO rb_download_get_lib_dir")
    return rb_install_get_dir() +"/lib/"

def rb_get_cxxflags():
    cf = ""
    # i386 is used by linker; c/cpp flags use -m32, -m64
    """ 
    if Base.arch == Base.ARCH_M32:
        cf += "\" -archi386 \""
    """
    cf = ""
    if Base.arch == Base.ARCH_M32:
        cf = "-m32"
    elif Base.arch == Base.ARCH_M64:
        cf = "-m64"

    if rb_is_debug():
        cf += " -g -O0 "
            
    return cf


def rb_get_cflags():
    cf = ""
    if Base.arch == Base.ARCH_M32:
        cf = "-m32 "
    elif Base.arch == Base.ARCH_M64:
        cf = "-m64 "

    if rb_is_debug():
        cf += " -g -O0 "

    cf += " -I" +rb_install_get_include_dir() +" "

    return cf

def rb_get_ldflags():
    ld = ""
    if Base.arch == Base.ARCH_M32:
        # @todo the linker arch option may have a different name; -m32/-m64
        ld = "-arch i386 "
    elif Base.arch == Base.ARCH_M64:
        # @todo the linker arch option may have a different name; -m32/-m64
        ld = "-arch x86_64 "

    ld += " -L" +rb_install_get_lib_dir() +" "

    return ld

def rb_get_cppflags():
    cf = ""
    if rb_is_debug():
        cf = "-DDEBUG "
    return cf

def rb_get_configure_options():
    return "CXXFLAGS='" +rb_get_cxxflags() +"' CFLAGS='" +rb_get_cflags() +"' LDFLAGS='" +rb_get_ldflags() +"' CPPFLAGS='" +rb_get_cppflags() +"'"

# script = the compile script instance (pass self)
# flags = extra flags we add to the ./configure command
# options = CPP/CXX etc.. options
# environmentVars = dictionary with additional environment vars we set. e.g. envvars = {"CC":"clang", "CXX":"clang++"} etc.. 
def rb_build_with_autotools(script, flags = None, options = True, environmentVars = None):
    # extra custom flags
    ef = ""
    if not flags == None:
        ef = flags

    # add the CXX,CPP,LDFLAGS etc..
    opts = ""
    if options:
        opts = " " + rb_get_configure_options()

    cmd = []

    if rb_is_mac():
        cmd.append("export PATH=" +rb_install_get_bin_dir() +":${PATH}")
        cmd.append("export PKG_CONFIG_PATH=" +rb_install_get_lib_dir() +"pkgconfig")

    # add extra environment vars
    if environmentVars:
        for varname in environmentVars:
            if rb_is_mac():
                cmd.append("export " +varname +"=" +environmentVars[varname])
            else:
                rb_red_ln("error: setting environment vars not working with autotools on this platform yet")

    dbg_flags = ""
    if rb_is_debug():
        dbg_flags = " --enable-debug "
        
    #cmd.append("export CC=clang")
    #cmd.append("export CXX=clang++")
    cmd.append("cd " +rb_get_download_dir(script))
    cmd.append("set -x && ./configure --prefix=" +rb_install_get_dir() +" " +ef +" " +dbg_flags +" " +opts)
    cmd.append("make clean && make && make install")
    rb_execute_shell_commands(script, cmd)
    #os.system(" && ".join(cmd))

def rb_arch_string(arch):
    if arch == Base.ARCH_M32:
        return "32"
    elif arch == Base.ARCH_M64:
        return "64"
    else:
        return "-"

def rb_is_file_downloaded(script, file):
    return os.path.isfile(rb_get_download_dir(script) + file)

def rb_execute_shell_commands(script, commands):
    
    if rb_get_os_shortname() == "win":
        f = open("tmp.bat", "w+")
        f.write("\n".join(commands))
        f.close()
        subprocess.call("tmp.bat")
    else:
        d = rb_get_base_path()
        f = open(d + "tmp.sh", "w+")
        f.write("\n".join(commands))
        f.close()
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

# Copies a file from the script (sources) dir to the download dir for the given script
# The file is copied from scripts/[script.name]/[file], to downloads/[script.name], or 
# the other dest given
def rb_copy_to_download_dir(script, src, dest = None):
    s = rb_get_script_dir(script) +"/" +src
    if not os.path.exists(s):
        rb_red_ln("Cannot find the file: " +src)

    d = src
    if not dest == None:
        d = dest
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

    os.system(rb_get_copy_command() +" " +src +" " +dest)

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
    if os.path.exists(lib):
        d = rb_deploy_get_dir() +"/lib/"
        rb_ensure_dir(d)
        #shutil.copyfile(os.path.normpath(dll), os.path.normpath(d))
        os.system(rb_get_copy_command()  +os.path.normpath(lib) +" " +os.path.normpath(d))
        rb_yellow_ln(lib)
    else:
        rb_red_ln("File not found " +lib)
    

# copy one specific header
# rb_depoloy_header(rb_install_get_include_file("x264.h"))
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
                os.system("cp " +os.path.normpath(dir +"/*.h") +" " +os.path.normpath(d))
        else:
            for f in files:
                rb_deploy_header(dir +"/" +f, subdir)

    else:
        rb_red_ln("Headers dir not found " +dir)


def rb_deploy_create_headers_dir(dir):
    dd = rb_deploy_get_dir() +"/include/" +dir
    if not os.path.exists(dd):
        rb_ensure_dir(dd)

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

# get the path to the vcvars.bat file thats sets the compiler vars for vs2012
#def rb_vs2012_get_vcvars_path():
#    return rb_vs2012_get_path() +"\\VC\\bin\\vcvars32.bat"


#def rb_vs2012_get_msbuild_path():
#    return r"C:\Windows\Microsoft.NET\Framework\v4.0.30319\MSBuild.exe"

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
        return "/p:configuration=Debug"
    elif Base.build_type == Base.BUILD_TYPE_RELEASE:
        return "/p:configuration=Release"
    else:
        rb_red("Error: not build flag for this...")
        return ""
       
def rb_vs2010_get_msbuild_type_flag():
    if Base.build_type == Base.BUILD_TYPE_DEBUG:
        return "/p:configuration=Debug"
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
        shutil.copytree(src, dest)


# CMake helpers
# ---------------------------------------------------------------------------
def rb_cmake_build(script):
    
    # Create the cmake command
    cmd = rb_cmake_get_executable() +" --build . --target install "
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
        rb_execute_shell_commands(script, cmd)
      

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

