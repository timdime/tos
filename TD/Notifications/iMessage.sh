#!/bin/bash

contact=$1
sentence=$2

osascript <<EOD                                                                                                                                                                           
    tell application "Messages"
      set targetService to 1st service whose service type = iMessage
      set targetBuddy to buddy "$contact" of targetService
      send "$sentence" to targetBuddy
    end tell
EOD
