cmake_minimum_required(VERSION 3.16.3...3.19.7 FATAL_ERROR)

project(TutorialMaker)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://github.com/SlicerLatinAmerica/SlicerTutorialMaker")
set(EXTENSION_CATEGORY "Developer Tools")
set(EXTENSION_CONTRIBUTORS
    "Douglas Goncalves (USP)"
    "Enrique Hernandez (UAEM)"
    "Joao Januario (USP)"
    "Lucas Silva (USP)"
    "Paulo Pereira (USP)"
    "Victor Montano (UAEM)"
    )
set(EXTENSION_DESCRIPTION "Tools for creating tutorials for 3D Slicer that can be automatically translated to multiple languages.")
set(EXTENSION_ICONURL "https://raw.githubusercontent.com/SlicerLatinAmerica/SlicerTutorialMaker/main/TutorialMaker.png")
set(EXTENSION_SCREENSHOTURLS
    "https://raw.githubusercontent.com/SlicerLatinAmerica/SlicerTutorialMaker/main/DOCS/annotations.png"
    "https://raw.githubusercontent.com/SlicerLatinAmerica/SlicerTutorialMaker/main/DOCS/annotations2.png"
    "https://raw.githubusercontent.com/SlicerLatinAmerica/SlicerTutorialMaker/main/DOCS/GUIdeveloped.png"
    "https://raw.githubusercontent.com/SlicerLatinAmerica/SlicerTutorialMaker/main/DOCS/pdf.png"
    )
set(EXTENSION_DEPENDS "NA") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(TutorialMaker)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
