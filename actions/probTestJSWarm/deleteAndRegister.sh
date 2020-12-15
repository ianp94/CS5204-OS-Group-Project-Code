#!/bin/bash
wsk action delete branchWarm
wsk action delete leftWarm 
wsk action delete rightWarm 

wsk action create leftWarm   leftWarm.js
wsk action create rightWarm  rightWarm.js
wsk action create branchWarm branchWarm.js -a conductor true

