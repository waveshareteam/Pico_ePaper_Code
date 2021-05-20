# Find all source files in a single current directory
# Save the name to DIR_Fonts_SRCS
aux_source_directory(. DIR_Fonts_SRCS)

# Generate the link library
add_library(Fonts ${DIR_Fonts_SRCS})