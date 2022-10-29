cmake_minimum_required(VERSION 3.22)

project(whodis CXX)

option(FORCE_COLORED_OUTPUT "Always produce ANSI-colored output (GNU/Clang only)." ON)

if (${FORCE_COLORED_OUTPUT})
    if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
       add_compile_options(-fdiagnostics-color=always)
    elseif ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang" OR "${CMAKE_CXX_COMPILER_ID}" STREQUAL "AppleClang")
       add_compile_options(-fcolor-diagnostics)
    endif ()
endif ()

add_compile_options(-ggdb3)
# add_compile_options(-g0)

# add_compile_options(-O0 -fno-omit-frame-pointer)

# add_compile_options(-Os -fvisibility=hidden -fvisibility-inlines-hidden -ffunction-sections -fdata-sections)
# add_link_options(-Os -Wl,-dead_strip)

add_compile_options(-Og)
add_link_options(-Og)

add_compile_options(-fsanitize=address)
add_link_options(-fsanitize=address)

# add_compile_options(-Ofast)
# add_link_options(-Ofast)

# add_compile_options(-flto=full -fwhole-program-vtables -fvirtual-function-elimination)
# add_link_options(-flto=full)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_EXTENSIONS YES)

add_subdirectory(3rdparty)
add_subdirectory(lib)
add_subdirectory(tests)
add_subdirectory(tools)
