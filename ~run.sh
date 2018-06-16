#!/bin/bash

while :
do
    clear
    date -Iseconds
    ./rmonth.py

    inotifywait -e close_write *.py
done
