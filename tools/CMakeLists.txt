add_executable(whodis-tool whodis-tool.cpp)

target_link_libraries(whodis-tool PRIVATE whodis fmt)
target_compile_options(whodis-tool PRIVATE -Wall -Wextra -Wpedantic)

install(TARGETS whodis-tool
    RUNTIME DESTINATION bin
)
