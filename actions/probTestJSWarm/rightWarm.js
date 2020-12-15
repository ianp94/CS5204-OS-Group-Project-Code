function main({params}) { 

    let prob = params.prob
    let rand = params.rand

    // If we find a warmup indicator, just return
    var doWarmup = ('warmup' in params);

    if(doWarmup){
        return {msg: "Warming Up Right Branch!", prob, rand, warm:true}
    }
    // This is just the normal activation
    else {

        // This object should not have a property called 'prob' becasue that's 
        // how we check if the branching is done. Make sure to not include that
        // property for this return object
        return { msg: "Right branch hit! "+rand.toString()+" < "+prob.toString()}
    }
}

