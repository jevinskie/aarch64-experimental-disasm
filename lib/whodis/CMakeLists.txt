set(WHODIS_SRC
    whodis.cpp
)

set(WHODIS_HDR_STANDALONE
)

set(WHODIS_HDR)
foreach(HDR ${WHODIS_HDR_STANDALONE})
    set(HDR "${CMAKE_CURRENT_SOURCE_DIR}/../../include/whodis/${HDR}")
    list(APPEND WHODIS_HDR ${HDR})
endforeach()

foreach(SRC ${WHODIS_SRC})
    get_filename_component(HDR_NAME ${SRC} NAME_WLE)
    set(HDR "${CMAKE_CURRENT_SOURCE_DIR}/../../include/whodis/${HDR_NAME}.h")
    if(EXISTS ${HDR})
        list(APPEND WHODIS_HDR ${HDR})
    endif()
endforeach()

set(WHODIS_PUBLIC_LIBS
)

set(WHODIS_PRIVATE_LIBS
    fmt
)

# WHODIS_HDR added for Xcode project generation
add_library(whodis STATIC ${WHODIS_SRC} ${WHODIS_HDR})
add_library(whodis-shared SHARED ${WHODIS_SRC} ${WHODIS_HDR})
set_target_properties(whodis whodis-shared PROPERTIES PUBLIC_HEADER "${WHODIS_HDR}")

target_link_libraries(whodis
PUBLIC
    ${WHODIS_PUBLIC_LIBS}
PRIVATE
    ${WHODIS_PRIVATE_LIBS}
)
target_compile_options(whodis PRIVATE -Wall -Wextra -Wpedantic)

target_include_directories(whodis
    PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/../../include
    PRIVATE ${CMAKE_CURRENT_BINARY_DIR}
)

target_link_libraries(whodis-shared
PUBLIC
    ${WHODIS_PUBLIC_LIBS}
PRIVATE
    ${WHODIS_PRIVATE_LIBS}
)
target_compile_options(whodis-shared PRIVATE -Wall -Wextra -Wpedantic)

target_include_directories(whodis-shared
    PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/../../include
    PRIVATE ${CMAKE_CURRENT_BINARY_DIR}
)


install(TARGETS whodis whodis-shared
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib
    PUBLIC_HEADER DESTINATION include/whodis
)
