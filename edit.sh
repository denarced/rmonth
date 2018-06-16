#!/bin/bash

updateTags() {
    while :
    do
        ctags *.py
        inotifywait -q -e close_write *.py
    done
}

updateTags &
updateTagsPid=$!
vim *.py *.sh
# First kill inotify running inside background process
pkill -P $updateTagsPid inotifywait
# Then kill the background process itself
kill $updateTagsPid
