cmake_minimum_required(VERSION 2.8)

set(rtmp_lib_name "librtmp")
set(rtmp_base_dir ${CMAKE_CURRENT_LIST_DIR})
set(rtmp_src_dir ${rtmp_base_dir})
set(rtmp_extern_dir ${rtmp_base_dir}/../../../../extern/)
set(rtmp_arch "i386")
set(rtmp_platform "win")

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
  set(rtmp_arch "${rtmp_arch}d")
endif()

if("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
  set(rtmp_compiler "clang")
elseif("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
  set(rtmp_compiler "gcc")
elseif("${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC")
  if(MSVC10)
    set(rtmp_compiler "vs2010")
  else()
    set(rtmp_compiler "vs2012")
  endif()
endif()

set(rtmp_triplet "${rtmp_platform}-${rtmp_compiler}-${rtmp_arch}")
set(rtmp_extern_inc_dir ${rtmp_extern_dir}/${rtmp_triplet}/include)
set(rtmp_extern_lib_dir ${rtmp_extern_dir}/${rtmp_triplet}/lib)
set(rtmp_extern_bin_dir ${rtmp_extern_dir}/${rtmp_triplet}/bin)

include_directories(${rtmp_extern_inc_dir})

set(rtmp_source_files
  ${rtmp_src_dir}/librtmp/amf.c
  ${rtmp_src_dir}/librtmp/hashswf.c
  ${rtmp_src_dir}/librtmp/log.c
  ${rtmp_src_dir}/librtmp/parseurl.c
  ${rtmp_src_dir}/librtmp/rtmp.c
)

add_library(${rtmp_lib_name} STATIC ${rtmp_source_files})

set(rtmp_headers
  ${rtmp_src_dir}/librtmp/amf.h
  ${rtmp_src_dir}/librtmp/bytes.h
  ${rtmp_src_dir}/librtmp/dh.h
  ${rtmp_src_dir}/librtmp/dhgroups.h
  ${rtmp_src_dir}/librtmp/handshake.h
  ${rtmp_src_dir}/librtmp/http.h
  ${rtmp_src_dir}/librtmp/log.h
  ${rtmp_src_dir}/librtmp/rtmp.h
  ${rtmp_src_dir}/librtmp/rtmp_sys.h
  )

install(TARGETS ${rtmp_lib_name} DESTINATION lib)

install(FILES ${rtmp_headers} DESTINATION include/librtmp/)