#export JAVA_HOME=/opt/jre
#export PATH=$JAVA_HOME/bin:$PATH
XRANDR_CONFIG=~/.efalive/screen_setup.sh

if [ -x $XRANDR_CONFIG ]
then
    $XRANDR_CONFIG
fi
feh --bg-fill /usr/share/plymouth/themes/efa-live/efaLive.png
exec openbox &

start_efa()
{
    if [ ! -f ~/.efalive/settings.conf ]
    then
        /opt/efalive/bin/efaLiveSetup.sh
    fi

    . ~/.efalive/settings.conf

    #Set the correct efa start script
    if [ $EFA_VERSION -eq 2 ]
    then
        EFA_PROG=/opt/efa2/efaBths.sh
    else
        EFA_PROG=/opt/efa/efadirekt.sh
    fi

    start=`date +%s`
    $EFA_PROG >> ~/efa.log 2>&1
    stop=`date +%s`
    delta=$(($stop-$start))
    if [ $delta -lt 5 ]
    then
        zenity --question --text="Das elektronische Fahrtenbuch efa wurde unerwartet schnell beendet. Soll nun die Aktion beim Herunterfahren von efa gestartet werden?"
        if [ $? -ne 0 ]
        then
            exit 0
        fi
    fi
}

start_efa
while :
do
    $EFA_SHUTDOWN_ACTION
done

