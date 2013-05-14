import linux_uinput, ctypes, fcntl, os, sys
from cinput import *
from mapper import KeyMapper, parse_conf
from example_conf import config
from linux_input import timeval, input_event

import imp

try:
    import cPickle as pickle
except ImportError:
    import pickle


import optparse

parser = optparse.OptionParser(description='Create input devices. '
        'TODO')
parser.add_option('-C', '--compat', action='store_true',
        help='Enable compatibility mode; for Python < 2.7')

args, cfg = parser.parse_args()

# Unpickle from stdin ; currently this is the default and only way
f = pickle.Unpickler(sys.stdin)

conf = f.load()

for path in cfg:
    config_merge = imp.load_source('', path).config_merge
    config_merge(conf)

m = KeyMapper(conf)

d = UInputDevice()
m.expose(d)
d.setup('Example input device')


while True:
    if not args.compat:
        ev = f.load()
    else:
        ev_p = f.load()
        ti = timeval(ev_p[0], ev_p[1])
        ev = input_event(ti, ev_p[2], ev_p[3], ev_p[4])

    ev = m.map_event(ev)

    d.fire_event(ev)
