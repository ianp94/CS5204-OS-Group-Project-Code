#!/bin/bash
wsk action update branchWarm branchWarm.js -a conductor true
wsk action update leftWarm   leftWarm.js   -a conductor true
wsk action update rightWarm  rightWarm.js  -a conductor true

