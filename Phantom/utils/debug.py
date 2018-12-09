# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

"""Debug functions & decorators that provide call tracing etc
This is a base file and therefore needs to be import-clean, or at least 1-level import clean
"""

from Phantom.constants import dbg_name, phantom_dir, debug
import os
import sys

def exception_str(exception):
    return '{}: {}'.format(exception.__class__.__name__, exception)

def clear_log():
    try:
        writeto = os.path.join(phantom_dir, 'utils', dbg_name)
        with open(writeto, 'w') as f:
            f.write('')
    except Exception as e:
        log_msg('Exception {} in clear_log, unable to clear'.format(exception_str(e)), 1, err=True)

def set_debug(new_level):
    # 671: need to either import the cfg object from constants, or
    #      read the cfg file again
    from Phantom.constants import cfg, cfg_file_name
    cfg.set('debug', 'level', str(new_level))
    with open(os.path.join(phantom_dir, cfg_file_name), 'w') as f:
        cfg.write(f)
    import Phantom.constants
    reload(Phantom.constants)
    log_msg('Set debugger level to {}'.format(new_level), new_level + 1, p='>')
    return new_level

def get_debug():
    from Phantom.constants import cfg
    return cfg.getint('debug', 'level')

def run_debugged(f, level, *args, **kwargs):
    """Run function `f` with `*args, **kwargs` under debug level `level`.
    run_debugged(f, level, *args, **kwargs)"""
    original_debug_level = debug
    set_debug(level)
    ret = f(*args, **kwargs)
    set_debug(original_debug_level)
    return ret

def log_msg(msg, level, **kwargs):
    err = kwargs.get('err', False)
    write = kwargs.get('write', True)
    mark = kwargs.get('mark', False)
    p = kwargs.get('p', '')
    if err and mark:
        mark = False

    if (level > debug) and (not err):
        return False
    ret = True

    if err:
         pm = '!'
    elif mark:
        pm = 'x'
    elif p:
        pm = p[0]
    else:
        pm = ' '
    msg = pm + msg

    #if len(msg) >= 88:
    #    msg = msg[:88] + '\n -' + msg[88:]

    writeto = os.path.join(phantom_dir, 'utils', dbg_name)

    # noinspection PyBroadException
    try:
        if write:
            with open(writeto, 'a') as f:
                f.write(msg + '\n')
    except Exception:
        log_msg("Exception {} in log_msg, couldn't write to file", level, write=False)
        ret = False

    sys.stdout.write("### {}\n".format(msg))

    return ret


class call_trace (object):

    def __init__(self, level, name=None):
        self.level = level
        self.name = name

    def __call__(self, f, *args, **kwargs):

        def call_trace_wrapped(*args, **kwargs):
            log_msg('{} called with args ({}, {})'.format(f.__name__, args, kwargs), self.level, p='{')
            returned = f(*args, **kwargs)
            log_msg('{} returned {}'.format(f.__name__, returned), self.level, p='}')
            return returned

        # keep the same function name to make life easier
        # *Should* use the Phantom.utils.decorators.named() decorator - but this file
        # has to be import clean, so we can't import it
        call_trace_wrapped.__name__ = self.name or f.__name__

        return call_trace_wrapped