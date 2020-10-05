<h3> <a href="https://github.com/tkravits/CBOE-Map">County Board of Equalization Automated Map Creation</a></h3>

This ArcPy code is designed to automate the map creation process for the County Assessor's Office. It was developed using ArcMap 10.5. This code also assumes the individual knows how to create a toolbox in ArcGIS. If help is needed to create a toolbox see: https://desktop.arcgis.com/en/arcmap/10.3/analyze/managing-tools-and-toolboxes/creating-a-custom-toolbox.htm

The user will set up ahead of time the subject property and the comparable sales that are to be mapped. The process creates two layers, applies symbology that was pre-set up ahead of time, zooms to the selected layers, and changes the title based on the subject input.

This completes the map making process with the exception of creating annotation (condos cause the labeling to be screwy) and cleaning up the scale bar. The code is found <a href="https://github.com/tkravits/CBOE-Map">here</a>
