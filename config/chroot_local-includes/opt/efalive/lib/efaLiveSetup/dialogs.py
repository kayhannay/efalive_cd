import pygtk
pygtk.require('2.0')
import gtk
import os
import sys

import locale
import gettext
APP="efaLiveSetup"
LOCALEDIR=os.path.join(os.path.dirname(sys.argv[0]), "locale")
DIR=os.path.realpath(LOCALEDIR)
gettext.install(APP, DIR, unicode=True)

def show_confirm_dialog(widget, message):
    dialog = gtk.MessageDialog(widget, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, message)
    response = dialog.run()
    dialog.destroy()
    if response == gtk.RESPONSE_YES:
        return True
    else:
        return False

def show_error_dialog(widget, message):
    dialog = gtk.MessageDialog(widget, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, message)
    dialog.run()
    dialog.destroy()

def show_exception_dialog(widget, message, details):
    dialog = gtk.MessageDialog(widget, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, message)
    dialog.set_resizable(True)
    expander = gtk.Expander(_("Details"))
    dialog.vbox.pack_start(expander)
    expander.show()
    details_area = gtk.TextView()
    details_area.get_buffer().set_text(details)
    details_area.show()
    scroll_area = gtk.ScrolledWindow()
    scroll_area.set_shadow_type(gtk.SHADOW_NONE)
    scroll_area.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    if details_area.set_scroll_adjustments(scroll_area.get_hadjustment(),
                                           scroll_area.get_vadjustment()):
        scroll_area.add(details_area)
    else:
        scroll_area.add_with_viewport(details_area)
    expander.add(scroll_area)
    scroll_area.show()
    dialog.run()
    dialog.destroy()

