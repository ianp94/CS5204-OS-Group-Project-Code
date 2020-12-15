import composer
from random import randint

composer.action('rands', {
    'action': {
        'kind': 'python:3',
        'code': "from random import randint\ndef function(env, args):\n        return { 'value' : randint(0,100) }"
    }
})
composer.action('prob', {
    'action': {
        'kind': 'python:3',
        'code': "def function(env, args):\n        return { 'prob' : args['value'] > 70 }"
    }
})
composer.action('ifTrue', {
    'action': {
        'kind': 'python:3',
        'code': "def function(env, args):\n        return { 'messge' : 'your random was greater than 70' }"
    }
})
composer.action('ifFalse', {
    'action': {
        'kind': 'python:3',
        'code': "def function(env, args):\n        return { 'messge' : 'your random was less than 70' }"
    }
})
composer.action('randProb', { 'sequence' : ['rands', 'prob']})

def main():
    return composer.when('randProb', 'ifTrue', 'ifFalse')
