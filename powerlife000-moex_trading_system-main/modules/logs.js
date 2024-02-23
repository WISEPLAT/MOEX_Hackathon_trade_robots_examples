var log4js = require('log4js'); // include log4js

log4js.configure({ // configure to use all types in different files.
    appenders: {
        'error' : {   type: 'file',
            filename: "./logs/error.log", // specify the path where u want logs folder error.log
            category: 'error',
            maxLogSize: 20480,
            backups: 10
        },
        'info' : {   type: "file",
            filename: "./logs/info.log", // specify the path where u want logs folder info.log
            category: 'info',
            maxLogSize: 20480,
            backups: 10
        },
        'debug' : {   type: 'file',
            filename: "./logs/debug.log", // specify the path where u want logs folder debug.log
            category: 'debug',
            maxLogSize: 20480,
            backups: 10
        }
    },
    categories: {
        default: { appenders: ['error','info', 'debug'], level: 'trace' }
    }
});

var loggerinfo = log4js.getLogger('info'); // initialize the var to use.
var loggererror = log4js.getLogger('error'); // initialize the var to use.
var loggerdebug = log4js.getLogger('debug'); // initialize the var to use.

module.exports = {
    loggerinfo: loggerinfo,
    loggererror: loggererror,
    loggerdebug: loggerdebug
};