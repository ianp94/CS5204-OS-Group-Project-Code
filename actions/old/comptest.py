mport composer
from random import randint

def rands(env, params):
    value = randint(0,100)
    print(value)
    return {"value" : value}

def prob(env, params):
    return { 'prob' : params['value'] > 70}

def printTrue(env, params):
    print("Results were true")
    return { 'result' : params['prob']}

def printFalse(env, params):
    print("Results were False")
    return { 'result' : params['prob']}


composer.composition('rands', composer.function(rands))
composer.composition('prob', composer.function(prob))
composer.composition('printTrue', composer.function(printTrue))
composer.composition('printFalse', composer.function(printFalse))
composer.composition('getRands', composer.sequence('rands', 'prob'))
composer.composition('test', composer.when('getRands', 'printTrue', 'printFalse'))
