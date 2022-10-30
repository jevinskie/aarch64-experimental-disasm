if (NOT TARGET argparse)
    add_subdirectory(argparse)
endif ()

if (NOT TARGET fmt)
    option(FMT_DOC OFF)
    option(FMT_TEST OFF)
    add_subdirectory(fmt)
endif ()
