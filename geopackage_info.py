# -*- coding:utf-8 -*-
# -----------------------------------------------------
# Project Name: gpkg
# Name: geopackage_info
# Filename: geopackage_info.py
# Author: mbegma
# Create data: 20.06.2025
# Description: ArcGIS Pro tools for getting information about *.geopackage files
#            
# Copyright: (c) mbegma, 2025
# History: 
#        - 20.06.2025: start of development
# -----------------------------------------------------
import arcpy
import os

def tab(n=1):
    """
    Функция возвращает указанное число табуляций:
    >> print(f"{tab(2)} test text")
    :param n:
    :return:
    """
    return "\t" * n

def _get_geopackage_workspace_info(description, lst: list):
    lst.append("\nWorkspace Information:")
    lst.append(f"type: {description.dataType}")
    lst.append(f"type workspace: {description.workspaceType}")
    lst.append(f"workspaceFactoryProgID: {description.workspaceFactoryProgID}")
    lst.append(f"connectionString: {description.connectionString}")
    lst.append(f"connectionProperties:") # authentication_mode, database, is_geodatabase, instance, server,
    lst.append(f"{tab()}authentication_mode: {description.connectionProperties.authentication_mode}")
    lst.append(f"{tab()}database: {description.connectionProperties.database}")
    lst.append(f"{tab()}is_geodatabase: {description.connectionProperties.is_geodatabase}")
    lst.append(f"{tab()}instance: {description.connectionProperties.instance}")
    lst.append(f"{tab()}server: {description.connectionProperties.server}")
    lst.append(f"currentRelease: {description.currentRelease}")
    lst.append(f"release: {description.release}")
    domains = description.domains
    lst.append("\nDomains:")
    if len(domains) > 0:
        for domain in domains:
            lst.append(f"{tab()}{domain}")
    else:
        lst.append(f"{tab()}No domains found")
    lst.append(f"\n{'-'*25}\n")


def _get_geopackage_layers_info(geopackage_filename: str, lst: list):
    lst.append("\nWorkspace Layers Information:")
    walk = arcpy.da.Walk(geopackage_filename)
    for path, names, layers in walk:
        for layer in layers:
            d = arcpy.da.Describe(os.path.join(path, layer))
            lst.append(f"layer name: {layer}")
            lst.append(f"{tab()}name: {d.get('name', '-')}")
            lst.append(f"{tab()}aliasName: {d.get('aliasName', '-')}")
            lst.append(f"{tab()}baseName: {d.get('baseName', '-')}")
            lst.append(f"{tab()}extension: {d.get('extension', '-')}")
            lst.append(f"{tab()}file: {d.get('file', '-')}")
            lst.append(f"{tab()}path: {d.get('path', '-')}")
            lst.append(f"{tab()}catalogPath: {d.get('catalogPath', '-')}")
            lst.append("")
            lst.append(f"{tab()}dataElementType: {d.get('dataElementType', '-')}")
            lst.append(f"{tab()}datasetType: {d.get('datasetType', '-')}")
            lst.append(f"{tab()}dataType: {d.get('dataType', '-')}")
            lst.append(f"{tab()}featureType: {d.get('featureType', '-')}")
            lst.append("")
            lst.append(f"{tab()}OIDFieldName: {d.get('OIDFieldName', '-')}")
            lst.append(f"{tab()}lengthFieldName: {d.get('lengthFieldName', '-')}")
            lst.append(f"{tab()}areaFieldName: {d.get('areaFieldName', '-')}")
            lst.append(f"{tab()}rasterFieldName: {d.get('rasterFieldName', '-')}")
            lst.append(f"{tab()}shapeFieldName: {d.get('shapeFieldName', '-')}")
            lst.append(f"{tab()}shapeType: {d.get('shapeType', '-')}")
            lst.append(f"{tab()}geometryStorage: {d.get('geometryStorage', '-')}")
            lst.append("")
            lst.append(f"{tab()}hasOID: {d.get('hasOID', '-')}")
            lst.append(f"{tab()}hasGlobalID: {d.get('hasGlobalID', '-')}")
            lst.append(f"{tab()}hasM: {d.get('hasM', '-')}")
            lst.append(f"{tab()}hasZ: {d.get('hasZ', '-')}")
            lst.append(f"{tab()}hasSpatialIndex: {d.get('hasSpatialIndex', '-')}")
            lst.append(f"{tab()}isTimeInUTC: {d.get('isTimeInUTC', '-')}")
            lst.append(f"{tab()}isVersioned: {d.get('isVersioned', '-')}")
            lst.append(f"{tab()}fullPropsRetrieved: {d.get('fullPropsRetrieved', '-')}")
            lst.append("")
            lst.append(f"{tab()}spatialReference:")
            lst.append(f"{tab(2)}name: {d['spatialReference'].name}")
            lst.append(f"{tab(2)}GCSCode: {d['spatialReference'].GCSCode}")
            lst.append("")
            lst.append(f"{tab()}extent:")
            lst.append(f"{tab(2)}XMax: {d['extent'].XMax}")
            lst.append(f"{tab(2)}XMin: {d['extent'].XMin}")
            lst.append(f"{tab(2)}YMax: {d['extent'].YMax}")
            lst.append(f"{tab(2)}YMin: {d['extent'].YMin}")
            lst.append("")
            lst.append(f"{tab()}fields:")
            _layer_fields_list = list()
            for item in d['fields']:
                _attr_list = [attr for attr in dir(item) if not attr.startswith('_')]
                _layer_fields = dict()
                for attr in _attr_list:
                    _layer_fields[attr] = getattr(item, attr)
                _layer_fields_list.append(_layer_fields)

            for field in _layer_fields_list:
                _s = list()
                for key, value in field.items():
                    _s.append(f"{key}: {value}")
                lst.append(f"{tab(2)}{' | '.join(f'{item:<20}' for item in _s)}")

            lst.append(f"\n{'-'*25}\n")


def main():
    geo_pkg_file = arcpy.GetParameterAsText(0)

    describe_list = list()
    desc = arcpy.Describe(geo_pkg_file)
    _get_geopackage_workspace_info(desc, describe_list)
    _get_geopackage_layers_info(geo_pkg_file, describe_list)
    for line in describe_list:
        arcpy.AddMessage(line)

    arcpy.AddMessage(f"{'='*50}")


if __name__ == "__main__":
    main()
