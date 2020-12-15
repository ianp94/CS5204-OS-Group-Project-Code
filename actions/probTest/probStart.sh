#!/bin/bash
sudo wsk action create rands rands.py --kind python:3
sudo wsk action create prob prob.py --kind python:3
sudo wsk action create ifTrue ifTrue.py --kind python:3
sudo wsk action create ifFalse ifFalse.py --kind python:3
pycompose randProb.py > randProb.json
pydeploy randProb randProb.json -w
pycompose composition.py > composition.json
pydeploy composition composition.json -w
#end
