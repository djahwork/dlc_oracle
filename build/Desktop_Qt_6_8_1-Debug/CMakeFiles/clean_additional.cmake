# Additional clean files
cmake_minimum_required(VERSION 3.16)

if("${CONFIG}" STREQUAL "" OR "${CONFIG}" STREQUAL "Debug")
  file(REMOVE_RECURSE
  "CMakeFiles/dlc_oracle_autogen.dir/AutogenUsed.txt"
  "CMakeFiles/dlc_oracle_autogen.dir/ParseCache.txt"
  "dlc_oracle_autogen"
  )
endif()
