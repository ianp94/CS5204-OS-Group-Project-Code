#!/bin/bash
wsk action create triple triple.js
wsk action create increment increment.js
wsk action create tripleAndIncrement tripleAndIncrement.js -a conductor true
wsk action invoke tripleAndIncrement -r -p value 3
