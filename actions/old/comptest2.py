import composer
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


composer.composition('getRands', composer.sequence(composer.function(rands), composer.function(prob)))
composer.composition('test', composer.when('getRands', 'printTrue', 'printFalse'))

def main():
    return composer.when('getRands', 'printTrue', 'printFalse')
