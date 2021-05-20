# Find all source files in a single current directory
# Save the name to DIR_GUI_SRCS
aux_source_directory(. DIR_GUI_SRCS)

include_directories(../Config)

# Generate the link library
add_library(GUI ${DIR_GUI_SRCS})
target_link_libraries(GUI PUBLIC Config)