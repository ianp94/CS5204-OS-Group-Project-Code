// This function is called 3 times, once to start, once to try 
// and prewarm, and then again after branching 
// THIS APPROACH DOES NOT WORK FOR PREWARMING
function main(params) {

    // Check that we haven't branched yet
    // By seeing if the user gave us a probability
    // for branching. Otherwise it was one of
    // the branches returning into this function
    var canBranch = ('prob' in params);
    var warmedUp  = ('warm' in params);


    // If we can not perform branching, return
    // the results from the branch that returned to
    // this function.
    if (!canBranch){
	    return {result: params}
    }

    var prob = params.prob;
    
    if(canBranch && !warmedUp){
        // Generate a random value from a pseudo-uniform distribution
        var rand = Math.random() 
        var warmUpParams = {prob, rand, warmup:true}
        var branch = (rand<prob) ? 'leftWarm' : 'rightWarm'
        return {action: branch, params: {params: warmUpParams}, state: {branch: branch}}
    }

    // Since we're prewarmed, let's get the rand we originally generated
    var rand = params.rand

    // Create a new set of parameters to pass the branch
    var newParams = {prob, rand}

    // Perform the branching
    if(rand < prob){
        return {action: 'leftWarm', params: {params: newParams}, state: {branch: 'leftWarm'}}
    }
    else{
        return {action: 'rightWarm', params: {params: newParams}, state: {branch: 'rightWarm'}}
    }
}
