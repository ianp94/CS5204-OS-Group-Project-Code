#!/bin/bash
wsk action create leftWarm   leftWarm.js
wsk action create rightWarm  rightWarm.js
wsk action create branchWarm branchWarm.js -a conductor true
