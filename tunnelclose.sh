#!/usr/bin/bash

sudo su <<HERE
kill -9 $(lsof -t -i:8006)
exit 0
HERE
