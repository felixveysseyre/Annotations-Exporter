cmake_minimum_required(VERSION 2.8.9)

project(AnnotationsExporter)

#-----------------------------------------------------------------------------
set(EXTENSION_HOMEPAGE "http://www.slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/AnnotationsExporter")
set(EXTENSION_CATEGORY "Utilities")
set(EXTENSION_CONTRIBUTORS "Felix Veysseyre (Kitware, Inc.),)")
set(EXTENSION_DESCRIPTION "Annotations Exporter")
set(EXTENSION_ICONURL "http://viewvc.slicer.org/viewvc.cgi/Slicer4/trunk/Extensions/Testing/AnnotationsExporter/LandmarksExporter.png?revision=21747&view=co")
set(EXTENSION_SCREENSHOTURLS "http://wiki.slicer.org/slicerWiki/images/e/e2/Slicer-r19441-AnnotationsExporter-screenshot.png")

#-----------------------------------------------------------------------------
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
add_subdirectory(AnnotationsExporter)

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_CPACK})
