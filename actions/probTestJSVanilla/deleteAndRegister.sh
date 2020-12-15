#!/bin/bash
wsk action delete branchVanilla
wsk action delete leftVanilla
wsk action delete rightVanilla

wsk action create leftVanilla   leftVanilla.js
wsk action create rightVanilla  rightVanilla.js
wsk action create branchVanilla branchVanilla.js -a conductor true

