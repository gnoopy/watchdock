#!/bin/bash
#

#

# OSX only
[ `uname -s` != "Darwin" ] && return
CONT_ID=$1
SHELL=$2
VGRNT_ID=$3
function iterm () {
osascript &>/dev/null <<EOF
    tell application "iTerm2"
        create window with default profile command "docker exec -it $CONT_ID $SHELL;exit"
        --create window with default profile command "bash"
    end tell
EOF
}

function terminal () {
osascript  &>/dev/null <<EOF
tell application "Terminal"
    set old to default settings
    set default settings to settings set "Basic"
    do script "clear  && docker exec -it $CONT_ID $SHELL;exit"
    tell app "Terminal" to set custom title of tab 1 of front window to "Container ($CONT_ID)"
    set default settings to old
    activate
end tell
EOF
}

function vterminal () {
osascript  &>/dev/null <<EOF
tell application "Terminal"
    set old to default settings
    set default settings to settings set "Basic"
    do script "clear && vagrant ssh -c 'docker exec -it $CONT_ID $SHELL' $VGRNT_ID;exit" 
    set default settings to old
    activate
    tell app "Terminal" to set custom title of tab 1 of front window to "Vagrant ($VGRNT_ID)_> Container($CONT_ID)"
    
end tell
EOF
}


# function appleterm () {
# osascript  &>/dev/null <<EOF
# tell application "Terminal"
#     do script "echo -n -e "\033]0;$title\007";$DOCKER exec -it $CONT_ID bash;exit"
#     set current settings of selected tab of window 1 to settings set "Basic"
#     activate
# end tell
# EOF
# }
if [ -z $VGRNT_ID ]; then
    echo "------------------"
    terminal $@
else
    echo "##################"
    vterminal $@
fi


