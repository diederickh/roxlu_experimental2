- make sure that all the build() functions use the rb_deploy_get_include_dir(), 
  rb_deploy_get_lib_dir(), rb_deploy_get_bin_dir(), and not rb_get_include_dir(),
  rb_get_lib_dir(), because when building we want to use the correct libs, dlls,
  headers, etc.. for the current build version (debug, release, etc)
- Every windows script that uses msbuild.exe should add the "rb_msvc_get_toolset_flag()"
  see the vorbis script for an example
- Add a clang/clang++ build, see the theora script where where we set CC and CXX
- On unices, maybe add symbolic links (e.g. for linbpng16)
