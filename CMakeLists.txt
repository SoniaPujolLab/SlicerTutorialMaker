cmake_minimum_required(VERSION 3.16.3...3.19.7 FATAL_ERROR)

project(TutorialMaker)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://github.com/SoniaPujolLab/SlicerTutorialMaker")
set(EXTENSION_CATEGORY "Utilities")
set(EXTENSION_CONTRIBUTORS "Douglas Gonçalves (Universidade de São Paulo), Enrique Hernández (Universidad Autónoma del Estado de México),
                                    João Januário (Universidade de São Paulo), Lucas Silva (Universidade de São Paulo),
                                    Paulo Pereira (Universidade de São Paulo), Victor Montaño (Universidad Autónoma del Estado de México),
                                    Paulo Eduardo de Barros Veiga (Universidade de São Paulo), Lucas Miranda Mendonça Rezende (Universidade de São Paulo), 
                                    Valeria Gomez-Valdes (Universidad Autónoma del Estado de México), Monserrat Rıos-Hernandez (Universidad Autónoma del Estado de México), 
                                    Fatou Bintou Ndiaye (University Cheikh Anta Diop),Mohamed Alalli Bilal (University Cheikh Anta Diop), 
                                    Steve Pieper (Isomics Inc.), Adriana Vilchis-Gonzalez (Universidad Autónoma del Estado de México), 
                                    Luiz Otavio Murta Junior (Universidade de São Paulo), Andras Lasso (Queen’s University), 
                                    Sonia Pujol (Brigham and Women’s Hospital, Harvard Medical School)")
set(EXTENSION_DESCRIPTION "<strong>Tutorial Maker</strong> allows you to build and share tutorials and documentations multi-lingual automatically.
                           <p>Workflow:</p>
                           <ul>
                              <li>Create a Python script defining the tutorial steps.</li>
                              <li>Run this module to execute the tutorial and generate screenshots.</li>
                              <li>Annotate the tutorial.</li>
                              <li>Apply translations (manual or Weblate) to produce localized versions.</li>
                           </ul>")
set(EXTENSION_ICONURL "https://raw.githubusercontent.com/SoniaPujolLab/SlicerTutorialMaker/main/TutorialMaker.png")
set(EXTENSION_SCREENSHOTURLS "https://raw.githubusercontent.com/SoniaPujolLab/SlicerTutorialMaker/main/DOCS/aibasedseg_demo1.png https://raw.githubusercontent.com/SoniaPujolLab/SlicerTutorialMaker/main/DOCS/aibasedseg_demo2.png https://raw.githubusercontent.com/SoniaPujolLab/SlicerTutorialMaker/main/DOCS/aibasedseg_demo3.png https://raw.githubusercontent.com/SoniaPujolLab/SlicerTutorialMaker/main/DOCS/aibasedseg_demo4.png")
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
