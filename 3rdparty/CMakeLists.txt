if (NOT TARGET argparse)
    add_subdirectory(argparse)
endif ()

if (NOT TARGET fmt)
    option(FMT_DOC OFF)
    option(FMT_TEST OFF)
    add_subdirectory(fmt)
endif ()

if (NOT TARGET cpptqdm)
    add_library(cpptqdm INTERFACE)
    target_include_directories(cpptqdm INTERFACE cpptqdm-scoped-include)
endif ()

if (NOT TARGET thread-pool)
    add_library(thread-pool INTERFACE)
    target_include_directories(cpptqdm INTERFACE thread-pool)
endif ()
