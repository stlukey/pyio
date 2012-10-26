#!/usr/bin/env python
#
# Copyright (c) 2012, Luke Southam <luke@devthe.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# - Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# - Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
# - Neither the name of the DEVTHE.COM LIMITED nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
"""
Shell based logging
"""

from os import system, getpgrp
from sys import stdout, stderr, argv

__author__ = "Luke Southam <luke@devthe.com>"
__copyright__ = "Copyright 2012, DEVTHE.COM LIMITED"
__license__ = "The BSD 3-Clause License"
__status__ = "Development"

# the message structure
MESSAGE = """{color}[{cmd};{pid}]: ({type_}) - '{msg}'{color_end}\n"""

# Color codes
purple = '\033[95m'
blue = '\033[94m'
green = '\033[92m'
orange = '\033[93m'
red = '\033[91m'

colors = {
    """
    Colored message; to add a bit of (consistent) style to messages.
    """
    'DEBUG': blue,
    'LOG': green,
    'WARNING': orange,
    'ERROR': red,
    'UNKNOWN': purple,
}


class Log(object):
    """
    Instance return from getLog; it stores original settings and
    splits logging methods to make log() easier and less repetitive.
    """
    def __init__(self, debug=False, out=stdout, errors=True):
        if not errors:
            errors = out
        self.out = (errors, out)
        self.proc = argv[0]
        self.pid = getpgrp()
        return self

    def logger(self, type_, msg):
        log(slef.proc, self.pid, self.debug, type_, msg, self.out)
        return self

    def debug(self, msg):
        logger("DEBUG", msg)
        return self

    def log(self, msg):
        logger("LOG", msg)
        return self

    def error(self, msg):
        logger("ERROR", msg)
        return self

    def warn(self, msg):
        logger("WARNING", msg)
        return self

def log(cmd, pid, debug, type_, msg, out=(True, stdout)):
    """
    prints out message in MESSAGE format and prints to out.
    """
    type_ = type_.upper()

    type_ = type_ if type_ in colors else "UNKNOWN"
    if type_ == "DEBUG" and not debug:
        return
    elif type_ == "ERROR" and out[1] is True:
        out = stderr
    elif type_ == "ERROR":
        out = out[1]
    elif out[0] is True:
        out = out[1]

    color = colors[type_]
    color_end = "\033[0m"

    print >> out, MESSAGE.format(**locals())


def getLog(debug, out=stdout, errors=True):
    """
    returns an instance of Log.
    """
    if not errors:
        errors = out
    out = (errors, out)
    return lambda type_, msg: log(debug, type_, msg, out)

def main():
    log(argv[1], argv[2], argv[3], argv[4])


if __name__ == '__main__':
    main()
