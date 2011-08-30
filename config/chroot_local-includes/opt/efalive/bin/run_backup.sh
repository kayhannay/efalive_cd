#!/bin/bash
#
####
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2008-2011 Kay Hannay <klinux@hannay.de>
#
###
#
# Create backup of efa data to a ZIP file
# Usage: run_backup.sh <PATH_TO_STORE_BACKUP>
#
EFA_BACKUP_PATHS="/opt/efa/ausgabe/layout /opt/efa/daten /home/efa/efa"
BACKUP_FILE=Sicherung_`/bin/date +%Y%m%d_%H%M%S`.zip

if [ -f ~/.efalive/backup.conf ]
then
    . ~/.efalive/backup.conf
else
    /bin/echo "efa has not been configured yet!"
    exit 1
fi

if [ ! $1 ]
then
	/bin/echo "Error, no backup path specified!"
	exit 1
fi

if [ ! -d $1 ]
then
	/bin/echo "Error, specified path does not exist!"
	exit 1
fi

### Create backup
cd /
/usr/bin/zip -r $1/$BACKUP_FILE $EFA_BACKUP_PATHS

if [ ! -e $1/$BACKUP_FILE ]
then
	/bin/echo "Error, backup was not successful"
    exit 1
fi

