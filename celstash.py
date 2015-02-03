'''Logging from Celery both to logstash and structured log (JSON) file.'''

from celery.utils.log import get_task_logger
import celery
import logstash

from logging.handlers import TimedRotatingFileHandler
from os import makedirs
from os.path import expanduser, isdir, join
import json
import logging


class config:
    class logstash:
        host = 'localhost'
        port = 5959
    logdir = expanduser('~/.local/log/celstash')


class TaskCtxAdapter(logging.LoggerAdapter):
    '''Adapter to add current task context to "extra" log fields'''
    def process(self, msg, kwargs):
        if not celery.current_task:
            return msg, kwargs

        kwargs = kwargs.copy()
        kwargs.setdefault('extra', {})['celery'] = \
            vars(celery.current_task.request)
        return msg, kwargs


class JSONFormatter(logging.Formatter):
    '''Format message as one line of JSON'''
    def format(self, record):
        obj = vars(record)

        # msg might be any Python object, make sure json doesn't blow up
        try:
            json.dumps(obj['msg'])
        except TypeError:
            obj['msg'] = repr(obj['msg'])

        # json can't dump exc_info, use default format as string
        if obj['exc_info']:
            obj['exc_info'] = self.formatException(obj['exc_info'])

        return json.dumps(obj)


def configure(logstash_host=None, logstash_port=None, logdir=None):
    '''Configuration settings.'''

    if not (logstash_host or logstash_port or logdir):
        raise ValueError('you must specify at least one parameter')

    config.logstash.host = logstash_host or config.logstash.host
    config.logstash.port = logstash_port or config.logstash.port
    config.logdir = logdir or config.logdir

    create_logdir(config.logdir)  # Fail close to setting


def create_logdir(logdir):
    if not isdir(logdir):
        makedirs(logdir)


def new_logger(name):
    '''Return new logger which will log both to logstash and to file in JSON
    format.

    Log files are stored in <logdir>/name.json
    '''

    log = get_task_logger(name)

    handler = logstash.LogstashHandler(
        config.logstash.host, config.logstash.port)
    log.addHandler(handler)

    create_logdir(config.logdir)
    handler = TimedRotatingFileHandler(
        '%s.json' % join(config.logdir, name),
        when='midnight',
        utc=True,
    )
    handler.setFormatter(JSONFormatter())
    log.addHandler(handler)

    return TaskCtxAdapter(log, {})
