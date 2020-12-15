// This function is called 3 times, once to start, and then twice for the 
// subsequent steps.
function main(params) {
    let step = params.$step || 0
    delete params.$step
    switch (step) {
        case 0: return { action: 'triple', params, state: { $step: 1 } }
        case 1: return { action: 'increment', params, state: { $step: 2 } }
        case 2: return { params }
    }
}
