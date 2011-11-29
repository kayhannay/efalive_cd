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

def get_icon_path(icon_name):
    path = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(path, "icons/%s" % icon_name)
    self._logger.debug("Icon path is: %s" % icon_path)
    return icon_path

class DeviceWidget(gtk.VBox):
    def __init__(self, device, homogeneous=False, spacing=2):
        super(DeviceWidget, self).__init__(homogeneous, spacing)
        self.device = device
        separator = gtk.HSeparator()
        self.add(separator)
        separator.show()

        hBox = gtk.HBox(False, 5)
        self.add(hBox)
        hBox.show()

        label_text = "Unknown"
        if self.device.label:
            label_text = self.device.label
        elif self.device.model:
            label_text = self.device.model
        self.label = gtk.Label(label_text)
        hBox.pack_start(self.label, True, True)
        self.label.show()

        self.backup_button = gtk.Button()
        backup_icon = gtk.image_new_from_file(get_icon_path("backup.png"))
        self.backup_button.set_image(backup_icon)
        self.backup_button.set_tooltip_text(_("Create backup of efaLive on USB device"))
        hBox.pack_end(self.backup_button, False, False)
        self.backup_button.show()

        self.mount_button = gtk.ToggleButton()
        hBox.pack_end(self.mount_button, False, False)
        self.mount_button.show()
        

class Device(object):
    def __init__(self, device_file, vendor=None, model=None, size=0, fs_type=None, label=None, mounted=False):
        self.device_file = device_file
        self.vendor = vendor
        self.model = model
        self.size = size
        self.fs_type = fs_type
        self.label = label
        self.mounted = mounted

class DeviceManagerModel(object):
    def __init__(self):
        self._logger = logging.getLogger('devicemanager.DeviceManagerModel')
        self.client = gudev.Client(['block'])
        self.client.connect("uevent", self._handle_device_event)
        self._add_device_observers = []
        self._remove_device_observers = []
        self._change_device_observers = []

    def register_add_observer(self, observer_cb):
        self._add_device_observers.append(observer_cb)

    def remove_add_observer(self, observer_cb):
        self._add_device_observers.remove(observer_cb)

    def _notify_add_observers(self, device):
        for observer_cb in self._add_device_observers:
            observer_cb(device)

    def register_remove_observer(self, observer_cb):
        self._remove_device_observers.append(observer_cb)

    def remove_remove_observer(self, observer_cb):
        self._remove_device_observers.remove(observer_cb)

    def _notify_remove_observers(self, device):
        for observer_cb in self._remove_device_observers:
            observer_cb(device)

    def register_change_observer(self, observer_cb):
        self._change_device_observers.append(observer_cb)

    def remove_change_observer(self, observer_cb):
        self._change_device_observers.remove(observer_cb)

    def _notify_change_observers(self, device):
        for observer_cb in self._change_device_observers:
            observer_cb(device)

    def _wrap_device(self, device):
        wrapped_device = Device(device.get_device_file())
        if device.has_property("ID_VENDOR"):
            wrapped_device.vendor = device.get_property("ID_VENDOR")
        if device.has_property("ID_MODEL"):
            wrapped_device.model = device.get_property("ID_MODEL")
        if device.has_property("UDISKS_PARTITION_SIZE"):
            byte_size = float(device.get_property_as_uint64("UDISKS_PARTITION_SIZE"))
            size = byte_size / 1024
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
            wrapped_device.size = "%.1f %s" % (size, unit)
        if device.has_property("ID_FS_TYPE"):
            wrapped_device.fs_type = device.get_property("ID_FS_TYPE")
        if device.has_property("ID_FS_LABEL"):
            wrapped_device.label = device.get_property("ID_FS_LABEL")
        wrapped_device.mounted = self._check_mounted(wrapped_device)
        return wrapped_device

    def _check_mounted(self, device):
        try:
            mount_output = self._command_output(["mount"])
        except OSError as (errno, strerror):
            self._logger.error("Could not execute mount command to check mount status: %s" % strerror)
            raise
        mounted = re.search(device.device_file, mount_output)
        if mounted:
            return True
        else:
            return False

    def _command_output(self, args, **kwds):
        kwds.setdefault("stdout", subprocess.PIPE)
        kwds.setdefault("stderr", subprocess.STDOUT)
        process = subprocess.Popen(args, **kwds)
        output = process.communicate()[0]
        return output

    def search_devices(self):
        for device in self.client.query_by_subsystem("block"):
            if (device.get_devtype() != "partition"):
                continue
            if (device.get_property("ID_BUS") != "usb"):
                continue
            #print_device(device)
            self._handle_device_event(self.client, "add", device)

    def _handle_device_event(self, client, action, device):
        if (device.get_devtype() != "partition"):
            return
        if (device.get_property("ID_BUS") != "usb"):
            return
        wrapped_device = self._wrap_device(device)
        if action == "add":
            self._notify_add_observers(wrapped_device)
        elif action == "remove":
            self._notify_remove_observers(wrapped_device)
        elif action == "change":
            self._notify_change_observers(wrapped_device)
        else:
            self._logger.warn("Unknown action: %s" % action)

    def toggle_mount(self, device, mount):
        if mount:
            label_text = "Unknown"
            if device.label:
                label_text = device.label
            elif device.model:
                label_text = device.model
            self._command_output(["pmount", device.device_file, label_text])
        else:
            self._command_output(["pumount", device.device_file])

    def create_backup(self, device):
        self._command_output(["/opt/efalive/bin/autobackup.sh", device.device_file])


class DeviceManagerView(gtk.Window):
    def __init__(self, type, controller=None):
        self._logger = logging.getLogger('devicemanager.DeviceManagerView')
        gtk.Window.__init__(self, type)
        self.set_title(_("Device Manager"))
        self.set_border_width(5)
        self._controller = controller

        self._init_components()

    def _init_components(self):
        self.main_box=gtk.VBox(False, 2)
        self.add(self.main_box)
        self.main_box.show()
        
        self.info_label = gtk.Label(_("USB storage devices"))
        self.main_box.add(self.info_label)
        self.info_label.show()

        self._device_entries = {}

    def add_device(self, device):
        device_entry = self.create_device_entry(device)
        self.main_box.add(device_entry)
        device_entry.show()
        self._device_entries[device.device_file] = device_entry

    def remove_device(self, device):
        device_entry = self._device_entries[device.device_file]
        del self._device_entries[device.device_file]
        device_entry.destroy()
        #TODO Does not work correctly yet
        self.queue_resize()

    def create_device_entry(self, device):
        device_entry = DeviceWidget(device)
        self.set_device_mounted(device_entry)

        device_entry.mount_button.connect("toggled", self._controller.toggle_mount, device_entry)
        device_entry.backup_button.connect("clicked", self._controller.create_backup, device)
        
        return device_entry

    def set_device_mounted(self, device_entry):
        if device_entry.device.mounted:
            unmount_icon = gtk.image_new_from_file(get_icon_path("unmount.png"))
            device_entry.mount_button.set_image(unmount_icon)
            device_entry.mount_button.set_tooltip_text(_("Unmount USB device"))
            device_entry.backup_button.set_sensitive(False)
            device_entry.label.set_tooltip_text(_("Vendor: %s") % device_entry.device.vendor + "\n" +
                _("Model: %s") % device_entry.device.model + "\n" +
                _("Device: %s") % device_entry.device.device_file + "\n" +
                _("Size: %s") % device_entry.device.size + "\n" +
                _("Filesystem: %s") % device_entry.device.fs_type + "\n" +
                _("Mouned to: %s") % "/media/" + device_entry.label.get_text())
        else:
            mount_icon = gtk.image_new_from_file(get_icon_path("mount.png"))
            device_entry.mount_button.set_image(mount_icon)
            device_entry.mount_button.set_tooltip_text(_("Mount USB device"))
            device_entry.backup_button.set_sensitive(True)
            device_entry.label.set_tooltip_text(_("Vendor: %s") % device_entry.device.vendor + "\n" +
                _("Model: %s") % device_entry.device.model + "\n" +
                _("Device: %s") % device_entry.device.device_file + "\n" +
                _("Size: %s") % device_entry.device.size + "\n" +
                _("Filesystem: %s") % device_entry.device.fs_type)


class DeviceManagerController(object):
    def __init__(self, argv, standalone=False, model=None, view=None):
        self._logger = logging.getLogger('devicemanager.DeviceManagerController')
        if(model==None):
            self._model=DeviceManagerModel()
        else:
            self._model=model
        if(view==None):
            self._view=DeviceManagerView(gtk.WINDOW_TOPLEVEL, self)
        else:
            self._view=view
        self._init_events(standalone)
        self._view.show()
        self._model.search_devices()

    def _init_events(self, standalone):
        if standalone:
            self._view.connect("destroy", self._destroy)
        self._model.register_add_observer(self.on_device_add)
        self._model.register_remove_observer(self.on_device_remove)
        self._model.register_change_observer(self.on_device_change)

    def _destroy(self, widget):
        gtk.main_quit()

    def toggle_mount(self, button, device_entry):
        if button.get_active():
            try:
                self._model.toggle_mount(device_entry.device, True)
                device_entry.device.mounted = True
                self._view.set_device_mounted(device_entry)
            except OSError as (errno, errstr):
                self._logger.error("Could not mount device: %s" % errstr)
                error_dialog = gtk.MessageDialog(self._view, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, _("Could not mount device:\n%s") % errstr)
                error_dialog.run()
                error_dialog.destroy()
        else:
            try:
                self._model.toggle_mount(device_entry.device, False)
                device_entry.device.mounted = False
                self._view.set_device_mounted(device_entry)
            except OSError as (errno, errstr):
                self._logger.error("Could not unmount device: %s" % errstr)
                error_dialog = gtk.MessageDialog(self._view, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, _("Could not unmount device:\n%s") % errstr)
                error_dialog.run()
                error_dialog.destroy()

    def create_backup(self, widget, device):
        try:
            self._model.create_backup(device)
        except OSError as (errno, errstr):
            self._logger.error("Could not create backup: %s" % errstr)
            error_dialog = gtk.MessageDialog(self._view, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, _("Could not create backup:\n%s") % errstr)
            error_dialog.run()
            error_dialog.destroy()

    def on_device_add(self, device):
        self._view.add_device(device)
    
    def on_device_remove(self, device):
        self._view.remove_device(device)
    
    def on_device_change(self, device):
        pass
        

if __name__ == '__main__':
    logging.basicConfig(filename='deviceManager.log',level=logging.INFO)
    controller = DeviceManagerController(sys.argv, True)
    gtk.main()

