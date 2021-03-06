# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AzimuthSwath
                                 A QGIS plugin
 Create a polygon based on a coordinate, direction, and direction variance.
                              -------------------
        begin                : 2017-04-06
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Little Earth GIS Consulting Inc.
        email                : popkinj@littleearth.ca
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from azimuth_swath_dialog import AzimuthSwathDialog
import os.path
import math
from qgis.core import *
from qgis.gui import QgsGenericProjectionSelector, QgsProjectionSelector
# from qgis.core import QgsMessageLog, QgsVectorLayer


class AzimuthSwath:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        self.dlg = AzimuthSwathDialog()


        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'AzimuthSwath_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Azimuth Swath')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'AzimuthSwath')
        self.toolbar.setObjectName(u'AzimuthSwath')

        # self.dlg.pushButton.clicked.connect(self.dlg.show)
        # QgsMessageLog.logMessage(str(type(self.dlg.pushButton)), "mine")
        # button = QPushButton("blah")
        # QgsMessageLog.logMessage(str(type(button)), "mine")

        self.dlg.crsButton.clicked.connect(lambda:
            QgsMessageLog.logMessage("yo", "mine")
        )

        # self.dlg.distance.keyPressEvent.connect(lambda:
        #     QgsMessageLog.logMessage("yoyo", "mine")
        # )
        # QgsMessageLog.logMessage(repr(self.dlg.pushButton), "mine")

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('AzimuthSwath', message)

    def selectcrs (self):
        QgsMessageLog.logMessage('Yo yo', 'Azimuth Swath')
        # QgsMessageLog.logMessage("message", "name")


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = AzimuthSwathDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/AzimuthSwath/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Azimuth Swath Creator'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Azimuth Swath'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):

        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()

        # Run the dialog event loop
        result = self.dlg.exec_()

        # self.dlg.pushButton.clicked.connect(self.selectcrs)
        # QgsMessageLog.logMessage(repr(self.selectcrs), "mine")

        # See if OK was pressed
        if result:


            epsg = "epsg:2193" 
            epsg = self.dlg.epsg.text()
            lon = float(self.dlg.longitude.text())
            lat = float(self.dlg.latitude.text())
            length = float(self.dlg.distance.text())
            angle = math.radians(float(self.dlg.direction.text()))
            variance = math.radians(float(self.dlg.variance.text()))
            resolution = int(self.dlg.resolution.text())

            # QgsMessageLog.logMessage(distance, 'Azimuth Swath')


            # Calculate the fan points
            start = angle - variance
            diff = variance * 2
            inc = diff / resolution
            vertices = [ # The vertex array
                QgsPoint(lon,lat)
            ]

            for i in range(resolution + 1):
                a = i*inc+start
                x = lon + (math.sin(a) * length)
                y = lat + (math.cos(a) * length)
                vertices.append(QgsPoint(x,y))

            # Close polygon
            vertices.append(QgsPoint(lon,lat))


            vl = QgsVectorLayer("Polygon?crs="+epsg, "Swath", "memory")
            pr = vl.dataProvider()
            vl.startEditing()

            # Origin is given
            origin = QgsFeature()
            origin.setGeometry(QgsGeometry.fromPolygon([vertices]))

            pr.addFeatures([origin])

            vl.commitChanges()
            vl.updateExtents()

            QgsMapLayerRegistry.instance().addMapLayer(vl)
            pass
