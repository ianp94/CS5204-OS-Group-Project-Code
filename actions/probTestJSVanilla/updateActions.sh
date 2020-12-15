#!/bin/bash
wsk action update branchVanilla branchVanilla.js -a conductor true
wsk action update leftVanilla   leftVanilla.js   -a conductor true
wsk action update rightVanilla  rightVanilla.js  -a conductor true

