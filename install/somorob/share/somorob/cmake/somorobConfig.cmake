# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_somorob_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED somorob_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(somorob_FOUND FALSE)
  elseif(NOT somorob_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(somorob_FOUND FALSE)
  endif()
  return()
endif()
set(_somorob_CONFIG_INCLUDED TRUE)

# output package information
if(NOT somorob_FIND_QUIETLY)
  message(STATUS "Found somorob: 0.0.0 (${somorob_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'somorob' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${somorob_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(somorob_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${somorob_DIR}/${_extra}")
endforeach()
