import arcpy

# uses the mxd that is running this code
mxd = arcpy.mapping.MapDocument("CURRENT")
# df is the dataframe, Layers is used to run through all the layers within the mxd. Leave Layers as is
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
# lyr sets the layer, needs to be spelt exactly as the layer sits in ArcMap
lyr = arcpy.mapping.ListLayers(mxd, "BOCO.PARCELS.PARCELS_OWNER", df)[0]
arcpy.env.overwriteOutput = True

# sets the parameters, this must be setup in the toolbox script
arcpy.AddMessage("Workspace added")
FClass = arcpy.GetParameterAsText(0)
Field = arcpy.GetParameterAsText(1)
Feature = arcpy.GetParameterAsText(2)
Feature1 = arcpy.GetParameterAsText(3)
Feature2 = arcpy.GetParameterAsText(4)
Feature3 = arcpy.GetParameterAsText(5)
Feature4 = arcpy.GetParameterAsText(6)
Feature5 = arcpy.GetParameterAsText(7)
Feature6 = arcpy.GetParameterAsText(8)

# sets the Feature parameter equal to the user input string
# I have added extra pair of single quotes for selecting strings
where_clause = """{} = '{}'""".format(arcpy.AddFieldDelimiters(FClass, Field),
                                      Feature)

where_clause1 = """{} IN ('{}','{}','{}','{}','{}','{}')""".format(arcpy.AddFieldDelimiters(FClass, Field),
                                      Feature1, Feature2, Feature3, Feature4, Feature5, Feature6)

where_clause2 = """{} IN ('{}','{}','{}','{}','{}','{}','{}')""".format(arcpy.AddFieldDelimiters(FClass, Field),
                                      Feature, Feature1, Feature2, Feature3, Feature4, Feature5, Feature6)

arcpy.AddMessage(where_clause)
arcpy.AddMessage(where_clause1)
arcpy.AddMessage(where_clause2)

# selects the attribute using the string the user input
arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", where_clause)
arcpy.CopyFeatures_management(lyr, 'Subject')
arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")

arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", where_clause1)
arcpy.CopyFeatures_management(lyr, 'Comps')
newlayer = arcpy.mapping.Layer(r'C:\ArcMap\Res_Boulder.gdb\Subject')
newlayer1 = arcpy.mapping.Layer(r'C:\ArcMap\Res_Boulder.gdb\Comps')
arcpy.mapping.AddLayer(df, newlayer, "AUTO_ARRANGE")
arcpy.mapping.AddLayer(df, newlayer1, "AUTO_ARRANGE")
arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")
arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", where_clause2)
# zooms to selected feature
df.zoomToSelectedFeatures()
# great job!
arcpy.RefreshActiveView()

sym = arcpy.mapping.ListLayers(mxd, "Subject", df)[0]
sym1 = arcpy.mapping.ListLayers(mxd, "Comps", df)[0]
sourceLayer1 = arcpy.mapping.Layer(r"C:\ArcMap\Subject.lyr")
sourceLayer2 = arcpy.mapping.Layer(r"C:\ArcMap\Comps.lyr")
# Apply the symbology from the symbology layer to the input layer
arcpy.mapping.UpdateLayer(df, sym, sourceLayer1, False)
arcpy.mapping.UpdateLayer(df, sym1, sourceLayer2, False)

relateFC = r"Subject"
relateFC1 = r"Comps"
relateFieldsList = ["StrNum", "Street", "StrSuf", "StrUnit", "AccountNo", "Comp_Num"]

for df in arcpy.ListFeatureClasses("Comps"):
    arcpy.AddField_management(df, "Comp_Num", "TEXT", field_length= 10)
    arcpy.CalculateField_management(df, "Comp_Num", "AccountNo")

with arcpy.da.UpdateCursor(relateFC1, ["AccountNo", "Comp_Num"]) as cursor:
    for acc, comp in cursor:
        if acc == Feature1:
            comp = 1
        if acc == Feature2:
            comp = 2
        if acc == Feature3:
            comp = 3
        if acc == Feature4:
            comp = 4
        if acc == Feature5:
            comp = 5
        if acc == Feature6:
            comp = 6
        row = (acc, comp)
        cursor.updateRow(row)
del row
del cursor

for lyr in arcpy.mapping.ListLayers(mxd, "Comps"):
    print lyr.name
    if lyr.supports("SHOWLABELS"):
        print lyr.name + " supports label classes"
        for lblClass in lyr.labelClasses:
            print lblClass.className
            lblClass.expression = lblClass.expression = '"{}" & "Comp #" & [Comp_Num] & ": " & [AccountNo] & vbNewLine & ' \
                                                        '[StrNum] & " " & ' \
                                                        '[Street] & " " & [StrSuf] & " " & [StrUnit] ' \
                                                        '& "{}"'.format("<FNT size = '10'>","</FNT>")
            if lblClass.showClassLabels:
                print "    Class Name:  " + lblClass.className
                print "    Expression:  " + lblClass.expression

        lyr.showLabels = True

for lyr in arcpy.mapping.ListLayers(mxd, "Subject"):
     print lyr.name
     if lyr.supports("SHOWLABELS"):
        print lyr.name + " supports label classes"
        for lblClass in lyr.labelClasses:
             print lblClass.className
             lblClass.expression = lblClass.expression = '"{}" & "Subject: " & [AccountNo] & vbNewLine & [StrNum] & " " &' \
                                                         ' [Street] & " " & [StrSuf] & " " & [StrUnit] ' \
                                                         '& "{}"'.format("<FNT size = '10'>","</FNT>")
             if lblClass.showClassLabels:
                print "    Class Name:  " + lblClass.className
                print "    Expression:  " + lblClass.expression

        lyr.showLabels = True

# your title has to have "title" in the element name box (right-click on it \properties\size and position)
titleItem = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "title")[0]

relateFC = r"Subject"
relateFC1 = r"Comps"
relateFieldsList = ["StrNum", "Street", "StrSuf", "StrUnit", "AccountNo", "Comp_Num"]
relateFieldsList1 = ["StrNum", "Street", "StrSuf", "StrUnit", "AccountNo"]

with arcpy.da.UpdateCursor(relateFC, relateFieldsList1) as cursor1:
    for row in cursor1:
        if row[3] == None:
            row[3] = " "
            cursor1.updateRow(row)

with arcpy.da.SearchCursor(relateFC, relateFieldsList1) as cursor:
    for row in cursor:
        titleItem.text = "COMPARABLE SALES FOR ID # " + \
                        Feature + '\n' + '{} {} {} {}'.format(row[0], row[1], row[2], row[3])

del mxd
arcpy.RefreshActiveView()
arcpy.AddMessage("All done!")
