const composer = require('openwhisk-composer')

module.exports = composer.merge(composer.action('branch'), composer.action('composition'))