# Windows
- Install cmake
- Install git
- Install VS2010 and VS2012 (express,pro)
- Install Windows 7/8 Development SDK
- Install Perl ( http://www.activestate.com/activeperl ) from activestate into build_system\tools\perl\ or somewhere into the PATH dirs 
- Install Nasm ( http://www.nasm.us/pub/nasm/releasebuilds/?C=M;O=D ) into build_system\tools\nasm\  (2.10.09), 
- Install cygwin ( 
  - devel > autoconf 2.69.2 
  - devel > automake 1.14.1
  - devel > gcc
  - devel > gcc-g++
  - devel > libtool 2.4.1
  - devel > make 3.x
  - devel > mingw64-i686-gcc
  - devel > mingw64-i686-gcc-g++

//- Install MingW into build_system\tools\mingw\ (make sure to also install the graphical tool)
//  Install these packages:
//   - msys-base
//   - mingw32-gcc-g++
//   - mingw-developer-toolkit

# Creating scripts for Windows
- We use the deploy dir as our local development root opposed to the install dir on unices