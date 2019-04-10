#!/bin/bash
python3 InitialRun.py
ret=$?
if [ $ret -ne 0 ]; then
     echo "Errors detected, trying fix"
     pip3 install -r requirements.txt -U
fi
python3 Test.py