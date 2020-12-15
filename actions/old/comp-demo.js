const composer = require('openwhisk-composer')

module.exports = composer.if(
    composer.action('authenticate', { action: function ({ password }) { return { value: password === 'abc123' } } }),
    composer.action('success', { action: function () { return { message: 'success' } } }),
    composer.action('failure', { action: function () { return { message: 'failure' } } }))
