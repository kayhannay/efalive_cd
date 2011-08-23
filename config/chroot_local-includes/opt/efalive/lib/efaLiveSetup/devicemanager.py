#!/usr/bin/python
'''
Created on 11.01.2011

Copyright (C) 2011 Kay Hannay

This file is part of efaLiveSetup.

efaLiveSetup is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
efaLiveSetup is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with efaLiveSetup.  If not, see <http://www.gnu.org/licenses/>.
'''
import pygtk
pygtk.require('2.0')
import gtk
import gudev
import glib
import os
import sys
import subprocess
import re

from observable import Observable

import locale
import gettext
APP="deviceManager"
LOCALEDIR=os.path.join(os.path.dirname(sys.argv[0]), "locale")
DIR=os.path.realpath(LOCALEDIR)
gettext.install(APP, DIR, unicode=True)

import logging
LOG_FILENAME = 'deviceManager.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)

def print_device(device):
    print "Device:"
    #print "\tSubsystem: %s" % device.get_subsystem()
    #print "\tType: %s" % device.get_devtype()
    #print "\tName: %s" % device.get_name()
    #print "\tNumber: %s" % device.get_number()
    #print "\tSYS-fs path: %s" % device.get_sysfs_path()
    #print "\tDriver: %s" % device.get_driver()
    #print "\tAction: %s" % device.get_action()
    print "\tFile: %s" % device.get_device_file()
    #print "\tLinks: %s" % device.get_device_file_symlinks()
    #print "\tProperties: %s" % device.get_property_keys()
    #print "\tSYBSYSTEM: %s" % device.get_property("SUBSYSTEM")
    #print "\tDEVTYPE: %s" % device.get_property("DEVTYPE")
    print "\tID_VENDOR: %s" % device.get_property("ID_VENDOR")
    print "\tID_MODEL: %s" % device.get_property("ID_MODEL")
    #print "\tID_TYPE: %s" % device.get_property("ID_TYPE")
    print "\tID_BUS: %s" % device.get_property("ID_BUS")
    print "\tID_FS_LABEL: %s" % device.get_property("ID_FS_LABEL")
    print "\tID_FS_TYPE: %s" % device.get_property("ID_FS_TYPE")
    print "\tUDISKS_PARTITION_SIZE: %s" % device.get_property("UDISKS_PARTITION_SIZE")


class Device(object):
    def __init__(self, deviceFile, vendor=None, model=None, size=0, fsType=None, label=None, mounted=False):
        self.deviceFile = deviceFile
        self.vendor = vendor
        self.model = model
        self.size = size
        self.fsType = fsType
        self.label = label
        self.mounted = mounted

class DeviceManagerModel(object):
    def __init__(self):
        self._logger = logging.getLogger('devicemanager.DeviceManagerModel')
        self.client = gudev.Client(['block'])
        self.client.connect("uevent", self._handleDeviceEvent)
        self._addDeviceObservers = []
        self._removeDeviceObservers = []
        self._changeDeviceObservers = []

    def registerAddObserver(self, observerCb):
        self._addDeviceObservers.append(observerCb)

    def removeAddObserver(self, observerCb):
        self._addDeviceObservers.remove(observerCb)

    def __notifyAddObservers(self, device):
        for observerCb in self._addDeviceObservers:
            observerCb(device)

    def registerRemoveObserver(self, observerCb):
        self._removeDeviceObservers.append(observerCb)

    def removeRemoveObserver(self, observerCb):
        self._removeDeviceObservers.remove(observerCb)

    def __notifyRemoveObservers(self, device):
        for observerCb in self._removeDeviceObservers:
            observerCb(device)

    def registerChangeObserver(self, observerCb):
        self._changeDeviceObservers.append(observerCb)

    def removeChangeObserver(self, observerCb):
        self._changeDeviceObservers.remove(observerCb)

    def __notifyChangeObservers(self, device):
        for observerCb in self._changeDeviceObservers:
            observerCb(device)

    def _wrapDevice(self, device):
        wrappedDevice = Device(device.get_device_file())
        if device.has_property("ID_VENDOR"):
            wrappedDevice.vendor = device.get_property("ID_VENDOR")
        if device.has_property("ID_MODEL"):
            wrappedDevice.model = device.get_property("ID_MODEL")
        if device.has_property("UDISKS_PARTITION_SIZE"):
            byteSize = float(device.get_property_as_uint64("UDISKS_PARTITION_SIZE"))
            size = byteSize / 1024
            unit = "KB"
            if (size > 1024):
                size = size / 1024
                unit = "MB"
            if (size > 1024):
                size = size / 1024
                unit = "GB"
            if (size > 1024):
                size = size / 1024
                unit = "TB"
            wrappedDevice.size = "%.1f %s" % (size, unit)
        if device.has_property("ID_FS_TYPE"):
            wrappedDevice.fsType = device.get_property("ID_FS_TYPE")
        if device.has_property("ID_FS_LABEL"):
            wrappedDevice.label = device.get_property("ID_FS_LABEL")
        wrappedDevice.mounted = self._checkMounted(wrappedDevice)
        return wrappedDevice

    def _checkMounted(self, device):
        mount_output = self.commandOutput(["mount"])
        mounted = re.search(device.deviceFile, mount_output)
        if mounted:
            return True
        else:
            return False

    def commandOutput(self, args, **kwds):
        kwds.setdefault("stdout", subprocess.PIPE)
        kwds.setdefault("stderr", subprocess.STDOUT)
        p = subprocess.Popen(args, **kwds)
        return p.communicate()[0]

    def searchDevices(self):
        for device in self.client.query_by_subsystem("block"):
            if (device.get_devtype() != "partition"):
                continue
            if (device.get_property("ID_BUS") != "usb"):
                continue
            #print_device(device)
            self._handleDeviceEvent(self.client, "add", device)

    def _handleDeviceEvent(self, client, action, device):
        if (device.get_devtype() != "partition"):
            return
        if (device.get_property("ID_BUS") != "usb"):
            return
        wrappedDevice = self._wrapDevice(device)
        if action == "add":
            self.__notifyAddObservers(wrappedDevice)
        elif action == "remove":
            self.__notifyRemoveObservers(wrappedDevice)
        elif action == "change":
            self.__notifyChangeObservers(wrappedDevice)
        else:
            self._logger.warn("Unknown action: %s" % action)

    def toggleMount(self, device, mount):
        try:
            if mount:
                labelText = "Unknown"
                if device.label:
                    labelText = device.label
                elif device.model:
                    labelText = device.model
                self.commandOutput(["pmount", device.deviceFile, labelText])
            else:
                self.commandOutput(["pumount", device.deviceFile])
            return True
        except:
            return False

    def createBackup(self, device):
        try:
            self.commandOutput(["/opt/efalive/bin/autobackup.sh", device.deviceFile])
            return True
        except:
            return False


class DeviceManagerView(gtk.Window):
    def __init__(self, type, controller=None):
        self._logger = logging.getLogger('devicemanager.DeviceManagerView')
        gtk.Window.__init__(self, type)
        self.set_title(_("Device Manager"))
        self.set_border_width(5)
        self._controller = controller

        self.initComponents()

    def initComponents(self):
        self.mainBox=gtk.VBox(False, 2)
        self.add(self.mainBox)
        self.mainBox.show()
        
        self.infoLabel = gtk.Label(_("USB storage devices"))
        self.mainBox.add(self.infoLabel)
        self.infoLabel.show()

        self.noDeviceLabel = gtk.Label(_("no devices found"))
        self.mainBox.add(self.noDeviceLabel)
        self.noDeviceLabel.show()

        self._deviceEntries = {}

    def addDevice(self, device):
        deviceEntry = self.createDeviceEntry(device)
        self.mainBox.add(deviceEntry)
	self.noDeviceLabel.hide()
        deviceEntry.show()
        self._deviceEntries[device.deviceFile] = deviceEntry

    def removeDevice(self, device):
        deviceEntry = self._deviceEntries[device.deviceFile]
        del self._deviceEntries[device.deviceFile]
        deviceEntry.destroy()
	if len(self._deviceEntries) == 0:
		self.noDeviceLabel.show()
        #TODO Does not work correctly yet
        self.queue_resize()

    def createDeviceEntry(self, device):
        mainBox = gtk.VBox(False, 2)
        
        separator = gtk.HSeparator()
        mainBox.add(separator)
        separator.show()

        hBox = gtk.HBox(False, 5)
        mainBox.add(hBox)
        hBox.show()

        labelText = "Unknown"
        if device.label:
            labelText = device.label
        elif device.model:
            labelText = device.model
        label = gtk.Label(labelText)
        label.set_tooltip_text(_("Vendor: %s") % device.vendor + "\n" +
                _("Model: %s") % device.model + "\n" +
                _("Device: %s") % device.deviceFile + "\n" +
                _("Size: %s") % device.size + "\n" +
                _("Filesystem: %s") % device.fsType + "\n" +
                _("Mount point: %s") % "/media/" + labelText)
        hBox.pack_start(label, True, True)
        label.show()

        backupButton = gtk.Button(_("Backup"))
        #theme = gtk.icon_theme_get_default()
        #print theme.list_icons()
        backupButton.set_sensitive(not device.mounted)
        hBox.pack_end(backupButton, False, False)
        backupButton.show()

        mountButton = gtk.ToggleButton(_("Mount"))
        mountButton.set_active(device.mounted)
        if device.mounted:
            mountButton.set_label(_("Unmount"))
        hBox.pack_end(mountButton, False, False)
        mountButton.show()

        mountButton.connect("toggled", self._controller.toggleMount, device, backupButton)
        backupButton.connect("clicked", self._controller.createBackup, device)
        
        return mainBox

class DeviceManagerController(object):
    def __init__(self, argv, model=None, view=None, standalone=True):
        self._logger = logging.getLogger('devicemanager.DeviceManagerController')
        if(model==None):
            self._model=DeviceManagerModel()
        else:
            self._model=model
        if(view==None):
            self._view=DeviceManagerView(gtk.WINDOW_TOPLEVEL, self)
        else:
            self._view=view
        self.initEvents(standalone)
        self._view.show()
        self._model.searchDevices()

    def initEvents(self, standalone):
        if standalone:
            self._view.connect('clicked', gtk.main_quit)
        self._model.registerAddObserver(self.onDeviceAdd)
        self._model.registerRemoveObserver(self.onDeviceRemove)
        self._model.registerChangeObserver(self.onDeviceChange)

    def toggleMount(self, button, device, backupButton):
        if button.get_active():
            self._model.toggleMount(device, True)
            button.set_label(_("Unmount"))
            backupButton.set_sensitive(False)
        else:
            self._model.toggleMount(device, False)
            button.set_label(_("Mount"))
            backupButton.set_sensitive(True)

    def createBackup(self, widget, device):
        if not self._model.createBackup(device):
            self._logger.error("Could not create backup!")

    def onDeviceAdd(self, device):
        self._view.addDevice(device)
    
    def onDeviceRemove(self, device):
        self._view.removeDevice(device)
    
    def onDeviceChange(self, device):
        pass
        

if __name__ == '__main__':
    controller = DeviceManagerController(sys.argv)
    gtk.main();

