# test/CMakeLists.txt

add_executable(test_dlc_service test_dlc_service.cpp)

include_directories(/usr/src/googletest/googletest/include)
include_directories(/usr/src/googletest/googlemock/include)

target_link_libraries(test_dlc_service
  gtest gtest_main
  gmock
  pthread
  cfd
  cfdcore
  cfddlc
)

add_test(NAME CreateDLCTest COMMAND test_dlc_service)
