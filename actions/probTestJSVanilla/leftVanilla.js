function main({params}) { 
    let prob = params.prob
    let rand = params.rand

    // This object should not have a property called 'prob' becasue that's 
    // how we check if the branching is done. Make sure to not include that
    // property for this return object
    return { msg: "Vanilla Left branch hit! "+rand.toString()+" < "+prob.toString()}
}

