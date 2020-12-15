compose mergeruns.js > mergeRun.json
deploy mergeRun mergeRun.json -w --kind nodejs:14
compose branchJsToPython.js > branchJ2P.json
deploy branchJ2P branchJ2P.json -w --kind nodejs:14
