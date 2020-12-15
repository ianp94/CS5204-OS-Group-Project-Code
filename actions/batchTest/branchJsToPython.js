const composer = require('openwhisk-composer')

module.exports =  composer.if('randProb', 'ifTrue', 'ifFalse')