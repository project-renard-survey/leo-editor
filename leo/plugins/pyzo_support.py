# -*- coding: utf-8 -*-
#@+leo-ver=5-thin
#@+node:ekr.20190410171646.1: * @file pyzo_support.py
#@@first
'''
pyzo_support.py: Allow access to pyzo features within Leo.

This plugin is active only if pyzo modules import successfully.

To do:
    1. Support pyzo file browser.
    2. Support pyzo shell & debugger.
'''
#@+<< copyright >>
#@+node:ekr.20190412042616.1: ** << copyright >>
#@+at
# This file uses code from pyzo. Here is the pyzo copyright notice:
# 
# Copyright (C) 2013-2018, the Pyzo development team
# 
# Pyzo is distributed under the terms of the (new) BSD License.
# The full license can be found in 'license.txt'.
# 
# Yoton is distributed under the terms of the (new) BSD License.
# The full license can be found in 'license.txt'.
#@-<< copyright >>
import sys
import leo.core.leoGlobals as g
#@+<< set switches >>
#@+node:ekr.20190410200749.1: ** << set switches >>
#
# Only my personal copy of pyzo supports these switches:
#
# --pyzo is part 1 of the two-step enabling of traces.
#
# The unpatch pyzo will say that the file '--pyzo' does not exist.
if '--pyzo' not in sys.argv:
    sys.argv.append('--pyzo')
#
# These switches are part 2 of two-step enabling of traces.
# My personal copy of pyzo uses `getattr(g, 'switch_name', None)`
# to avoid crashes in case these vars do not exist.
g.pyzo = True
g.pyzo_trace = True
g.pyzo_trace_imports = True
#@-<< set switches >>
#@+others
#@+node:ekr.20190410171905.1: ** function: init
def init():
    '''Return True if the plugin has loaded successfully.'''
    if not g.isPython3:
        print('pyzo_support.py requires Python 3.6 or above.')
        return False
    if g.app.gui.guiName() != "qt":
        print('pyzo_support.py requires Qt gui')
        return False
    if not is_pyzo_loaded():
        print('pyzo_support.py requires pyzo')
        return False
    g.plugin_signon(__name__)
    # g.registerHandler('after-create-leo-frame',onCreate)
    return True
#@+node:ekr.20190410200453.1: ** function: is_pyzo_loaded
def is_pyzo_loaded():
    '''
    Return True if pyzo appears to be loaded,
    using the "lightest" possible imports.
    '''
    try:
        import pyzo
        assert pyzo
        from pyzo.tools import ToolManager
        assert ToolManager
        # Be explicit about where everything comes from...
            # import pyzo
            # import pyzo.core.editor
            # import pyzo.core.main
            # import pyzo.core.splash
            # import pyzo.util
        return True
    except Exception:
        g.es_exception()
        g.pyzo = False
        g.pyzo_trace = False
        g.pyzo_trace_imports = False
        return False
#@-others
#@-leo
