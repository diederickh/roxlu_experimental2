# JPEG 

# Windows 

- You need to rename the correct `jconfig.XX` to `jconfig.h`
- MSVC2012 does not find the Win32.mak. This file can be found in the Windows 7 SDK  
  `C:\Program Files (x86)\Microsoft SDKs\Windows\v7.0A\Include`, I copied it to this directory
  so it's available.
- The install.txt file, contained in the source distribution describe how to create a DLL
  from the sources; note the mention about memory model

_MSVC 2010_

  - Open a VS2010 command prompt
  - Extract the sources
  - Rename `jconfig.vc` to `jconfig.h`
  - Release build: Compile with: `nmake /f Makefile.vc nodebug=1 /a`
  - Debug build: Compile with: `nmake /f Makefile.vc nodebug=0 /a`

_MSVC 2012_      

  - Open a VS2012 command prompt
  - Extract the sources
  - Rename `jconfig.vc` to `jconfig.h`
  - Release build: Compile with: `nmake /f Makefile.vc nodebug=1 /a`
  - Debug build: Compile with: `nmake /f Makefile.vc nodebug=0 /a`