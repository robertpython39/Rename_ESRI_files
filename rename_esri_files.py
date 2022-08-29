# -------------------------------------------------------------------------------
# Name:        Rename Files from directory
# Purpose:     intern
#
# Author:      rnicolescu
#
# Created:     29/08/2022
# Copyright:   (c) rnicolescu 2022
# Licence:     <your license here>
# -------------------------------------------------------------------------------
print 'Loading arcpy'
from arcpy import env
import arcpy
import os
import glob

print 'Arcpy loaded!'

class Rename(object):
    print "Changes the name of a dataset. This includes a wide variety of data types, among them feature dataset, raster, table, and shapefile."

    CWD = os.getcwd()

    def __init__(self, path):
        self.path = path

    def get_extension(self):
        extensions = []
        with open(os.path.join(Rename.CWD, 'extensions.txt'), 'r') as file:
            for line in file:
                extensions.append(line.replace("\n", ""))
        file.close()
        return extensions

    def folder_path(self):
        # Create the environment of the folder path
        # List all the elements from the path
        # Create a list/tuple with the elements of the path

        env.workspace = self.path
        env.overwriteOutput = True

        shapes = []
        for file in glob.glob(self.path + '\\*'):
            fn = os.path.basename(file)
            shapes.append(fn)

        return shapes

    def rename_management(self, shapes, extension):
        # Set the environment of the folder for processing
        # List all elements from the folder
        # Ask the user wich element he/she wants to rename
        # Apply the changes with arcpy.manangement.rename() function

        env.workspace = self.path
        env.overwriteOutput = True

        print 'The shapefiles from the folder:'
        for shp in shapes:
            print shp

        shape_rename = raw_input('Wich file you want to rename?:\n').upper()
        new_name = raw_input('Enter new name for file:').upper()

        for shp in shapes:
            # for shapefiles (.shp, .cpg, .dbf, .prj, .sbn, .sbx, .shp, .shp.xml, .shx)
            if shp.endswith('.shp') and shp[:-4].upper() == shape_rename  and shp[-4:] in extension:
                arcpy.Rename_management(in_data=shp, out_data=new_name + shp[-4:])

            # for other ESRI file formats
            elif not shp.endswith(('.shp', '.cpg', '.dbf', '.prj', '.sbn', '.sbx', '.shp', '.shp.xml', '.shx')) \
                    and shp[:-4].upper() == shape_rename and shp[-4:] in extension:
                os.rename(shp, new_name + shp[-4:])


        return  'Script done!'

    def main(self):
        extension_list = self.get_extension()
        folder_add = self.folder_path()
        rename_file = self.rename_management(folder_add, extension_list)


if __name__ == "__main__":
    rename_file = Rename(raw_input(r'Please add the path of folder for processing:'))
    rename_file.main()
