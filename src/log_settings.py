import logging



class DebugLog(logging.Filter):
    def filter(self, record):       
        return  record.levelname == 'DEBUG'

class ErrorLog(logging.Filter):
    def filter(self, record):       
        return  record.levelname == 'ERROR'

class ErrorHandler(logging.Handler):
    def __init__(self, filename):
        logging.Handler.__init__(self)
        self.filename = filename
    
    def emit(self, record):
        msg = self.format(record)
        try:
            with open('logs/' + self.filename, 'a') as f:
                f.write(msg + '\n')
        except FileNotFoundError:
            with open(self.filename, 'a') as f:
                f.write(msg + '\n')



logger_config = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'std_format': {
            'format': "{asctime} - {levelname:<8} - {name:<8} - {message}",
            'style': '{'
        },
        'debug_format': {
            'format': "{asctime} - {levelname:<8} - {name:<8} - {module}: {funcName}:{lineno} {message}",
            'style': "{"
        },
        'error_format': {
            'format': "{asctime} - {levelname:<8} - {name:<8} - {module}: {message}",
            'style': "{"
        }

    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'std_format'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'level': 'DEBUG',
            'formatter': 'debug_format',
            'filters': ['debug_filter']
        },
        'custom': {
            '()': ErrorHandler,
            'filename': 'error.log',
            'level': 'ERROR',
            'formatter': 'error_format',
            'filters': ['error_filter']
        }
    },

    'loggers': {
        'app_logger': {
            'level': 'DEBUG',
            'handlers': ['custom'], 
            'propagate': False
        }
    },

    'filters': {
        'debug_filter': {
            '()': DebugLog
        },
        'error_filter': {
            '()': ErrorLog
        }
    },
}