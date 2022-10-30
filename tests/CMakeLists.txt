add_executable(whodis-test whodis-test.cpp)
target_link_libraries(whodis-test PRIVATE whodis argparse fmt)
target_compile_options(whodis-test PRIVATE -Wall -Wextra -Wpedantic)

install(TARGETS whodis-test
    RUNTIME DESTINATION bin
)
