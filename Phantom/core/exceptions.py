# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

"""Exceptions used in Phantom."""

from Phantom.core.chessobj import PhantomObj

__all__ = []

class ChessError (Exception, PhantomObj):

    # 671: should call Exception.__init__ here? It's been working fine so I
    #      don't see a need to, but it could prevent future issues
    def __init__(self, msg='No error message supplied', caller=None):
        self.msg = self.message = msg
        self.name = self.__class__.__name__
        self.caller = caller

    def __str__(self):
        if self.caller:
            return '{} sourced at {}'.format(repr(self.msg), repr(self.caller))
        else:
            return '{} with no source'.format(repr(self.msg))

    def __repr__(self):
        return self.__str__()
__all__.append('ChessError')

class InvalidMove (ChessError): pass
__all__.append('InvalidMove')

class InvalidDimension (ChessError):pass
__all__.append('InvalidDimension')

class LogicError (ChessError): pass
__all__.append('LogicError')
