#!/bin/bash
wsk action create leftVanilla   leftVanilla.js
wsk action create rightVanilla  rightVanilla.js
wsk action create branchVanilla branchVanilla.js -a conductor true
