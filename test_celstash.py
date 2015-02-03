import celstash

from SocketServer import UDPServer, BaseRequestHandler
from getpass import getuser
from os import makedirs
from os.path import isdir, join, isfile
from shutil import rmtree
from tempfile import gettempdir
from threading import Thread
from time import sleep
import json

messages = []


def make_test_dir():
    dirname = join(gettempdir(), 'celstash-test-%s' % getuser())
    if isdir(dirname):
        rmtree(dirname)

    makedirs(dirname)
    return dirname


class RequestHandler(BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        messages.append(data)


def run_server():
    # port 0 will choose a random free port
    server = UDPServer(('localhost', 0), RequestHandler)
    port = server.socket.getsockname()[1]
    thr = Thread(target=server.serve_forever)
    thr.daemon = True
    thr.start()

    return port


def test_log():
    logdir = make_test_dir()
    port = run_server()

    celstash.configure(logdir=logdir, logstash_port=port)
    log = celstash.new_logger('celstash-test')
    msg = 'Let sleeping dogs lie.'
    log.error(msg)

    # Let the message propagate
    sleep(0.1)

    logfile = join(logdir, 'celstash-test.json')
    assert isfile(logfile), 'no log file at %s' % logfile
    with open(logfile) as fo:
        record = json.loads(fo.readline())
    assert record['msg'] == msg, 'bad message in file'

    assert len(messages) == 1, 'no message in UDP'
    record = json.loads(messages[0])
    assert record['@message'] == msg, 'bad message in UDP'
