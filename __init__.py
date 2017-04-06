# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AzimuthSwath
                                 A QGIS plugin
 Create a polygon based on a coordinate, direction, and direction variance.
                             -------------------
        begin                : 2017-04-06
        copyright            : (C) 2017 by Little Earth GIS Consulting Inc.
        email                : popkinj@littleearth.ca
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load AzimuthSwath class from file AzimuthSwath.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .azimuth_swath import AzimuthSwath
    return AzimuthSwath(iface)
