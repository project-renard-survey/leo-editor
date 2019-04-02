# -*- coding: utf-8 -*-
#@+leo-ver=5-thin
#@+node:ekr.20190330100032.1: * @file ../core/pyzo_shims.py
#@@first
'''Shims to adapt pyzo classes to Leo.'''
#@+<< copyright notices >>
#@+node:ekr.20190401023314.1: ** << copyright notices >>
#
# Portions of this file are based on pyzo's source code:
# Copyright (C) 2013-2018 by Almar Klein.
#
# Search for the above copyright to see the relevant code.
#@-<< copyright notices >>
import leo.core.leoGlobals as g
if g.pyzo_trace_imports:
    print('\npyzo_shims.py\n')
#@+<< non-pyzo imports (pyzo_shims.py) >>
#@+node:ekr.20190330101646.1: **  << non-pyzo imports (pyzo_shims.py) >>
import os
import sys
import time
from leo.core.leoQt import QtCore, QtWidgets
#@-<< non-pyzo imports (pyzo_shims.py) >>

# Be explicit about where everything comes from...
import pyzo
import pyzo.core.main
import pyzo.core.splash
import pyzo.util

#@+others
#@+node:ekr.20190330100939.1: **  function: loadFile (pyzo_shims.py)
def loadFile(self, filename, updateTabs=True):
    '''
    A monkey-patched replacement for pyzo.core.editorTabs.EditorTabs.loadFile.
    '''
    # Not used, and will probably never be used.
    print('----- patched loadFile: filename:', filename)
    if filename.endswith('leo'):
        print('----- ignoring .leo file')
        return None
    try:
        return old_loadFile(self, filename, updateTabs)
    except Exception:
        g.es_exception()
        return None
#@+node:ekr.20190317082751.1: ** class ConfigShim
new_config = True
    # Works when False.
    
config_shim_seen = {}
    # Keys are bunches.

try:  # pragma: no cover
    from collections import OrderedDict as _dict
except ImportError:
    _dict = dict
    
from pyzo.util.zon import Dict

# config_base = _dict if new_config else Dict

config_base = _dict if new_config else Dict
    # The old code needs _dict, not dict.

class ConfigShim(config_base):
    
    def __init__(self):
        config_base.__init__(self)
        print('\n===== ConfigShim: new_config: %s\n' % new_config)
    
    if new_config:
        #@+<< define bunch settings >>
        #@+node:ekr.20190331082353.1: *3* << define bunch settings >>
        # '(\w+)': With: \1 = 

        advanced = g.Bunch(
            autoCompDelay=200,
            fileExtensionsToLoadFromDir='py,pyw,pyx,txt,bat',
            find_autoHide_timeout=10,
            homeAndEndWorkOnDisplayedLine=0,
            shellMaxLines=10000,
            titleText='{fileName} ({fullPath}) - Interactive Editor for Python',
        )

        settings = g.Bunch(   
            allowFloatingShell=0,
            autoCallTip=1,
            autoClose_Brackets=1,
            autoClose_Quotes=1,
            autoComplete=1,
            autoComplete_acceptKeys='Tab',
            autoComplete_caseSensitive=0,
            autoComplete_fillups='\n',
            autoComplete_keywords=1,
            autoIndent=1,
            changeDirOnFileExec=0,
            defaultIndentUsingSpaces=1,
            defaultIndentWidth=4,
            defaultLineEndings='CRLF',
            defaultStyle='python',
            justificationWidth=70,
            language='English (US)',
            removeTrailingWhitespaceWhenSaving=0,
        )

        shellConfigs2 = [
            g.Bunch(
                argv = '',
                environ = '',
                exe = 'c:\\anaconda3\\python.exe',
                gui = 'auto',
                ipython = 'yes',
                name = 'Python',
                projectPath = '',
                pythonPath = '',
                scriptFile = '',
                startDir = '',
                startupScript = '',
                )
        ]

        shortcuts2 = g.bunch(
            #@+<< define bunch shortcuts2 >>
            #@+node:ekr.20190331082549.1: *4* << define bunch shortcuts2 >>
            edit__comment = 'Ctrl+R,',
            edit__copy = 'Ctrl+C,Ctrl+Insert',
            edit__cut = 'Ctrl+X,Shift+Delete',
            edit__dedent = 'Shift+Tab,',
            edit__delete_line = 'Ctrl+D,',
            edit__duplicate_line = 'Ctrl+Shift+D,',
            edit__find_next = 'Ctrl+G,F3',
            edit__find_or_replace = 'Ctrl+F,',
            edit__find_previous = 'Ctrl+Shift+G,Shift+F3',
            edit__find_selection = 'Ctrl+F3,',
            edit__find_selection_backward = 'Ctrl+Shift+F3,',
            edit__indent = 'Tab,',
            edit__justify_commentdocstring = 'Ctrl+J,',
            edit__paste = 'Ctrl+V,Shift+Insert',
            edit__paste_and_select = 'Ctrl+Shift+V',
            edit__redo = 'Ctrl+Y,',
            edit__select_all = 'Ctrl+A,',
            edit__toggle_breakpoint = 'Ctrl+B,',
            edit__uncomment = 'Ctrl+T,',
            edit__undo = 'Ctrl+Z,',
            file__close = 'Ctrl+W,',
            file__new = 'Ctrl+N,',
            file__open = 'Ctrl+O,',
            file__save = 'Ctrl+S,',
            run__execute_cell = 'Ctrl+Return,Ctrl+Enter',
            run__execute_cell_and_advance = 'Ctrl+Shift+Return,Ctrl+Shift+Enter',
            run__execute_file = 'Ctrl+E,F5',
            run__execute_main_file = 'Ctrl+M,F6',
            run__execute_selection = 'Alt+Return,F9',
            run__execute_selection_and_advance = 'Shift+F9,Shift+Alt+Return',
            run__run_file_as_script = 'Ctrl+Shift+E,Ctrl+F5',
            run__run_main_file_as_script = 'Ctrl+Shift+M,Ctrl+F6',
            shell__clear_screen = 'Ctrl+L,',
            shell__close = 'Alt+K,',
            shell__create_shell_1_ = 'Ctrl+1,',
            shell__create_shell_2_ = 'Ctrl+2,',
            shell__create_shell_3_ = 'Ctrl+3,',
            shell__create_shell_4_ = 'Ctrl+4,',
            shell__create_shell_5_ = 'Ctrl+5,',
            shell__create_shell_6_ = 'Ctrl+6,',
            shell__create_shell_7_ = 'Ctrl+7,',
            shell__create_shell_8_ = 'Ctrl+8,',
            shell__interrupt = 'Ctrl+I,Meta+C',
            shell__postmortem_debug_from_last_traceback = 'Ctrl+P,',
            shell__restart = 'Ctrl+K,',
            shell__terminate = 'Ctrl+Shift+K,',
            view__select_editor = 'Ctrl+9,F2',
            view__select_previous_file = 'Ctrl+Tab,',
            view__select_shell = 'Ctrl+0,F1',
            view__zooming__zoom_in = 'Ctrl+=,Ctrl++',
            view__zooming__zoom_out = 'Ctrl+-,',
            view__zooming__zoom_reset = 'Ctrl+\\,'
            #@-<< define bunch shortcuts2 >>
        )

        state = g.Bunch(
            editorState2=[
                #@+<< define editorState2 >>
                #@+node:ekr.20190331082353.2: *4* << define editorState2 >>
                [
                    'C:\\apps\\pyzo\\source\\pyzo\\codeeditor\\highlighter.py',
                    3279,
                    96
                ],
                [
                    'C:\\apps\\pyzo\\source\\pyzo\\core\\editorTabs.py',
                    22913,
                    693
                ],
                [
                    'C:\\apps\\pyzo\\source\\pyzo\\codeeditor\\highlighter.py',
                    'hist'
                ],
                [
                    'C:\\apps\\pyzo\\source\\pyzo\\core\\editorTabs.py',
                    'hist'
                ]
                #@-<< define editorState2 >>
            ],
            find_autoHide=1,
            find_matchCase=0,
            find_regExp=0,
            find_show=0,
            find_wholeWord=1,
            loadedTools=['pyzofilebrowser', 'pyzologger', 'pyzosourcestructure'],
            newUser=1,
            windowGeometry='AdnQywACAAAAAAGjAAAA2AAABv0AAANWAAABqwAAAPcAAAb1AAADTgAAAAAAAAAAB4A=\n',
            windowState=(
                'AAAA/wAAAAD9AAAAAgAAAAAAAACeAAACRPwCAAAAAfwAAAAUAAACRAAAAYgA/////AIAAAAC+wAA\n'
                'AB4AcAB5AHoAbwBmAGkAbABlAGIAcgBvAHcAcwBlAHIBAAAAFAAAAWEAAAEIAP////sAAAAmAHAA\n'
                'eQB6AG8AcwBvAHUAcgBjAGUAcwB0AHIAdQBjAHQAdQByAGUBAAABewAAAN0AAAB6AP///wAAAAEA\n'
                'AAGEAAACRPwCAAAABvsAAAAMAHMAaABlAGwAbABzAQAAABQAAAD/AAAAcwD////7AAAAFABwAHkA\n'
                'egBvAGwAbwBnAGcAZQByAQAAARkAAAE/AAAAWQD////7AAAAGgBwAHkAegBvAHcAbwByAGsAcwBw\n'
                'AGEAYwBlAAAAAT4AAAEaAAAAAAAAAAD7AAAAJgBwAHkAegBvAGkAbgB0AGUAcgBhAGMAdABpAHYA\n'
                'ZQBoAGUAbABwAAAAAnkAAAB6AAAAAAAAAAD7AAAAIgBwAHkAegBvAGgAaQBzAHQAbwByAHkAdgBp\n'
                'AGUAdwBlAHIAAAACGgAAAVsAAAAAAAAAAPsAAAAcAHAAeQB6AG8AdwBlAGIAYgByAG8AdwBzAGUA\n'
                'cgAAAAKwAAAAxQAAAAAAAAAAAAADHQAAAkQAAAAEAAAABAAAAAgAAAAI/AAAAAA=\n'
            )
        )

        tools = g.Bunch(
            pyzofilebrowser = g.Bunch(),
            pyzofilebrowser2 = g.Bunch(
                expandedDirs = ['c:\\apps\\pyzo\\source\\pyzo'],
                nameFilter = '!*.pyc',
                path = 'c:\\apps\\pyzo\\source\\pyzo',
                searchMatchCase = 0,
                searchRegExp = 0,
                searchSubDirs = 1,
                starredDirs =[
                    g.Bunch(
                        addToPythonpath = 0,
                        name = 'Pyzo sources',
                        path = 'c:\\apps\\pyzo\\source',
                    )
                ]
            ),
            pyzohistoryviewer = g.Bunch(),
            pyzointeractivehelp = g.Bunch(
                fontSize = 14,
                noNewlines = 1,
                smartNewlines = 1
            ),
            pyzologger = g.Bunch(),
            pyzosourcestructure = g.Bunch(
                level = 1,
                showTypes = ['class', 'def', 'cell', 'todo'],
            ),
            pyzowebbrowser = g.Bunch(
                bookMarks = [
                    'docs.python.org',
                    'scipy.org',
                    'doc.qt.nokia.com/4.5/',
                    'pyzo.org',
                ],
                zoomFactor = 1.0,
            ),
            pyzoworkspace = g.Bunch(
                hideTypes = [],
                typeTranslation = g.Bunch(
                    builtin_function_or_method = 'function',
                    method = 'function'
                )
            )
        ) 

        view = g.Bunch(
            autoComplete_popupSize=[300, 100],
            codeFolding=0,
            doBraceMatch=1,
            edgeColumn=80,
            fontname='DejaVu Sans Mono',
            highlightCurrentLine=1,
            highlightMatchingBracket=1,
            qtstyle='fusion',
            showIndentationGuides=1,
            showLineEndings=0,
            showStatusbar=0,
            showWhitespace=0,
            showWrapSymbols=0,
            tabWidth=4,
            wrap=1,
            zoom=2
        )
        #@-<< define bunch settings >>
        #@+<< new config methods >>
        #@+node:ekr.20190331052308.1: *3* << new config methods >>
        #@+others
        #@+node:ekr.20190331052308.2: *4* ConfigShim.__repr__
        def __repr__(self):
            
            return 'ConfigShim'
            # return g.obj2string(self)
                # Can't do this: it calls repr!
        #@+node:ekr.20190331052308.3: *4* ConfigShim.__getattribute__ 
        def __getattribute__(self, key):
            '''The usual shinanigans...'''
            ### return object.__getattribute__(self, key)
            try:
                val = object.__getattribute__(self, key)
            except AttributeError:
                if key in self:
                    val = self[key]
                else:
                    raise
            if key not in config_shim_seen:
                config_shim_seen [key] = True
                print('\n===== ConfigShim.__getattribute__', key, val)
            return val
        #@+node:ekr.20190331052308.4: *4* ConfigShim.__setattr__ (not used)
        # def __setattr__(self, key, val):
            # if key in Dict.__reserved_names__:
                # # Either let OrderedDict do its work, or disallow
                # if key not in Dict.__pure_names__:
                    # return _dict.__setattr__(self, key, val)
                # else:
                    # raise AttributeError('Reserved name, this key can only ' +
                                         # 'be set via ``d[%r] = X``' % key)
            # else:
                # # if isinstance(val, dict): val = Dict(val) -> no, makes a copy!
                # self[key] = val
        #@-others
        #@-<< new config methods >>
    else:
        #@+<< old config methods >>
        #@+node:ekr.20190331052251.1: *3* << old config methods >>
        #@+others
        #@+node:ekr.20190317082751.2: *4* ConfigShim.__repr__
        def __repr__(self):

            from pyzo.util.zon import isidentifier
                # Changed import.
            identifier_items = []
            nonidentifier_items = []
            for key, val in self.items():
                if isidentifier(key):
                    identifier_items.append('%s=%r' % (key, val))
                else:
                    nonidentifier_items.append('(%r, %r)' % (key, val))
            if nonidentifier_items:
                return 'Dict([%s], %s)' % (', '.join(nonidentifier_items),
                                           ', '.join(identifier_items))
            else:
                return 'Dict(%s)' % (', '.join(identifier_items))
        #@+node:ekr.20190317082751.3: *4* ConfigShim.__getattribute__
        def __getattribute__(self, key):
            try:
                ### return object.__getattribute__(self, key)
                val = object.__getattribute__(self, key)
                if False and key not in ('advanced', 'shortcuts2', 'settings'):
                    # print('===== LeoPyzoConfig 1: %r: %r' % (key, val))
                    print('===== LeoPyzoConfig 1: %r' % key)
                return val
            except AttributeError:
                if key in self:
                    if False and key not in ('advanced', 'shortcuts2', 'settings'):
                        # print('===== LeoPyzoConfig 1: %r: %r' % (key, g.truncate(self[key], 50)))
                        print('===== LeoPyzoConfig 2: %r' % key)
                    return self[key]
                else:
                    raise
        #@+node:ekr.20190317082751.4: *4* ConfigShim.__setattr__
        def __setattr__(self, key, val):
            if key in Dict.__reserved_names__:
                # Either let OrderedDict do its work, or disallow
                if key not in Dict.__pure_names__:
                    return _dict.__setattr__(self, key, val)
                else:
                    raise AttributeError('Reserved name, this key can only ' +
                                         'be set via ``d[%r] = X``' % key)
            else:
                # if isinstance(val, dict): val = Dict(val) -> no, makes a copy!
                self[key] = val
        #@-others
        #@-<< old config methods >>

    #@+others
    #@-others
#@+node:ekr.20190317084647.1: ** class MainWindowShim (pyzo.core.main.MainWindow)
class MainWindowShim(pyzo.core.main.MainWindow):
    
    #@+<< MainWindowShim switches >>
    #@+node:ekr.20190402104228.1: *3* << MainWindowShim switches >>
    initial_draw = False
        # True: do an initial draw.
        # Works either way.
    use_shell = True
        ### True: disables the Leo icon and adds the Pyzo menus!
        # However, there is no great flash when use_shell is True.
        
    use_menu = True
        # True: create pyzo menus.
    #@-<< MainWindowShim switches >>

    #@+others
    #@+node:ekr.20190317084647.2: *3* MainWindowShim.__init__
    def __init__(self, parent=None, locale=None):
        '''
        Important: do *all* inits here.  Do *not* call MainWindow.__init__.
        
        This allows us complete control over all aspects of the startup process.

        This method is based on pyzo code
        Copyright (C) 2013-2018 by Almar Klein.
        
        '''
        #
        # pylint: disable=non-parent-init-called, super-init-not-called
        QtWidgets.QMainWindow.__init__(self, parent)
            #
            # Do **not** call MainWindow.__init__: it calls _populate!
            #
        self.monkey_patch_leo()
        self._closeflag = 0
            # Used during closing/restarting
        #
        # Init window title and application icon
        # Set title to something nice. On Ubuntu 12.10 this text is what
        # is being shown at the fancy title bar (since it's not properly
        # updated)
        self.setWindowTitle('Leo Main Window')
        pyzo.core.main.loadAppIcons()
        g.app.gui.attachLeoIcon(self)
        #
        # Restore window geometry before drawing for the first time.
        self.resize(800, 600) # default size
        self.restoreGeometry()
        #
        # Show splash screen.
        w = SplashShim(parent)
        self.setCentralWidget(w)
        #
        # These do nothing, even when use_shell is True.
            # self.setStyleSheet("QMainWindow { background-color: #268bd2;}")
            # self.setStyleSheet("QMainWindow { background-color: red;}")
        #
        # Show empty window and disable updates for a while
        if self.initial_draw:
            self.show()
            self.paintNow()
        self.setUpdatesEnabled(False)
        #
        # Set locale of main widget, for translate.
        if locale:
            self.setLocale(locale)
        #
        # Store myself
        pyzo.main = self
        #
        # Init dockwidget settings
        self.setTabPosition(QtCore.Qt.AllDockWidgetAreas, QtWidgets.QTabWidget.South)
        self.setDockOptions(
                QtWidgets.QMainWindow.AllowNestedDocks |
                QtWidgets.QMainWindow.AllowTabbedDocks
                #|  QtWidgets.QMainWindow.AnimatedDocks
            )
        #
        # Set window atrributes
        self.setAttribute(QtCore.Qt.WA_AlwaysShowToolTips, True)
        #
        # Load pyzo icons and fonts.
        pyzo.core.main.loadIcons()
        pyzo.core.main.loadFonts()
        #
        # Set qt style and test success
        self.setQtStyle(None) # None means init!
        #    
        # Populate the window (imports more code)
        self._populate()
        #
        # Revert to normal background, and enable updates
        self.setStyleSheet('')
            # Required.
        self.setUpdatesEnabled(True)
        #
        # Restore window state, force updating, and restore again
        self.restoreState()
        if not self.initial_draw:
            self.show()
        self.paintNow()
        self.restoreState()
        #
        # Create new shell config if there is None
        if not pyzo.config.shellConfigs2:
            from pyzo.core.kernelbroker import KernelInfo
            pyzo.config.shellConfigs2.append( KernelInfo() )
        #
        # EKR: Set background.
        if getattr(pyzo.config.settings, 'dark_theme', None):
            bg = getattr(pyzo.config.settings, 'dark_background', '#657b83')
                # Default: solarized base00
            try:
                self.setStyleSheet("background: %s" % bg) 
            except Exception:
                print('oops: MainWindow.__init__')
        #
        # Put the focus on editor
        e = pyzo.editors.getCurrentEditor()
        if e is not None:
            e.setFocus()
        #
        # Handle any actions
        pyzo.core.commandline.handle_cmd_args()
    #@+node:ekr.20190317084647.3: *3* MainWindowShim._populate (5 shims)
    def _populate(self):
        '''
        This method is based on pyzo code
        Copyright (C) 2013-2018 by Almar Klein.
        '''
        
        trace = False and g.pyzo_trace_imports

        # Delayed imports, exactly as in MainWindow._populate.
        if trace:
            print('\n===== MainWindowShim._populate\n')
        from pyzo.core.editorTabs import EditorTabs
        from pyzo.core.shellStack import ShellStackWidget
        from pyzo.core import codeparser
        from pyzo.core.history import CommandHistory
        from pyzo.tools import ToolManager
        if trace:
            print('\n===== MainWindowShim._populate: end of delayed imports\n')

        # Instantiate tool manager
        pyzo.toolManager = ToolManager()

        # Instantiate and start source-code parser
        if pyzo.parser is None:
            pyzo.parser = codeparser.Parser()
            pyzo.parser.start()

        # Create editor stack and make the central widget
        pyzo.editors = EditorTabs(self)
        self.setCentralWidget(pyzo.editors)
            # EKR: QMainWindow.setCentralWidget

        # Create floater for shell
        self._shellDock = dock = QtWidgets.QDockWidget(self)
        if pyzo.config.settings.allowFloatingShell:
            dock.setFeatures(dock.DockWidgetMovable | dock.DockWidgetFloatable)
        else:
            dock.setFeatures(dock.DockWidgetMovable)
        dock.setObjectName('shells')
        dock.setWindowTitle('Shells')
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)

        # Create shell stack
        if self.use_shell:
            # Disabling the shell works.
            pyzo.shells = ShellStackWidget(self)
            dock.setWidget(pyzo.shells)
            pyzo.shells.menu = g.TracingNullObject(tag='pyzo.shells.menu')
                # To suppress menu events.
        else:
            pyzo.shells = g.TracingNullObject(tag='pyzo.shells')

        # Initialize command history
        pyzo.command_history = CommandHistory('command_history.py')

        # Create the default shell when returning to the event queue
        if self.use_shell:
            pyzo.core.main.callLater(pyzo.shells.addShell)
                # New: fully qualified.

        # Create statusbar
        if pyzo.config.view.showStatusbar:
            pyzo.status = self.statusBar()
        else:
            pyzo.status = None
            self.setStatusBar(None)

        # Create shells.
        if self.use_shell:
            from pyzo.core import menu
            pyzo.keyMapper = menu.KeyMapper()
            assert not isinstance(pyzo.keyMapper, (g.TracingNullObject, g.NullObject))
                # This should not be a Shim.
            menu.buildMenus(self.menuBar())
        else:
            # Shim:
            ###from pyzo.core import menu
            pyzo.menu = g.TracingNullObject(tag='pyzo.menu')
            pyzo.shells = g.TracingNullObject(tag='pyzo.shells')
            pyzo.keyMapper = g.TracingNullObject(tag='pyzo.keyMapper')
        #
        # Add the context menu to the editor
        if self.use_menu:
            pyzo.editors.addContextMenu()
            pyzo.shells.addContextMenu()
        else:
            pyzo.editors.addContextMenu = g.TracingNullObject(tag='pyzo.editors.addContextMenu()')
            pyzo.shells.addContextMenu = g.TracingNullObject(tag='pyzo.shells.addContextMenu()')
            
        #
        # Load tools
        if pyzo.config.state.newUser and not pyzo.config.state.loadedTools:
            pyzo.toolManager.loadTool('pyzosourcestructure')
            pyzo.toolManager.loadTool('pyzofilebrowser', 'pyzosourcestructure')
        elif pyzo.config.state.loadedTools:
            for toolId in pyzo.config.state.loadedTools:
                pyzo.toolManager.loadTool(toolId)
    #@+node:ekr.20190317084647.5: *3* MainWindowShim.closeEvent (traces)
    def closeEvent(self, event):
        """ Override close event handler. """
        import pyzo.core.commandline as commandline
            # New import.
        
        t1 = time.clock()

        # Are we restaring?
        restarting = time.time() - self._closeflag < 1.0

        # Save settings
        pyzo.saveConfig()
        pyzo.command_history.save()

        # Stop command server
        commandline.stop_our_server()

        # Proceed with closing...
        result = pyzo.editors.closeAll()
        if not result:
            self._closeflag = False
            event.ignore()
            return
        else:
            self._closeflag = True
            
        t2 = time.clock()

        # Proceed with closing shells
        pyzo.localKernelManager.terminateAll() # pylint: disable=no-member
        for shell in pyzo.shells:
            shell._context.close()
            
        t3 = time.clock()

        # Close tools
        for toolname in pyzo.toolManager.getLoadedTools():
            tool = pyzo.toolManager.getTool(toolname)
            tool.close()
            
        t4 = time.clock()

        # Stop all threads (this should really only be daemon threads)
        import threading
        for thread in threading.enumerate():
            if hasattr(thread, 'stop'):
                try:
                    thread.stop(0.1)
                except Exception:
                    pass
                    
        t5 = time.clock()

        if 1: # EKR
            print('===== MainWindowShim.closeEvent')
            print('stage 1:          %5.2f' % (t2-t1))
            print('stage 2: shells:  %5.2f' % (t3-t2))
            print('stage 3: tools:   %5.2f' % (t4-t3))
            print('stage 4: threads: %5.2f' % (t5-t4))

        # Proceed as normal
        QtWidgets.QMainWindow.closeEvent(self, event)

        # Harder exit to prevent segfault. Not really a solution,
        # but it does the job until Pyside gets fixed.
        if sys.version_info >= (3,3,0) and not restarting:
            if hasattr(os, '_exit'):
                os._exit(0)
    #@+node:ekr.20190402101635.1: *3* MainWindowShim.monkey_patch_leo
    old_loadFile = None
        # Set by monkey_patch.
        # Save a permanent reference.

    def monkey_patch_leo(self):

        global old_loadFile
        
        g.trace('=====')
            
        # Use a Leonine pyzo.config.
        if 0:
            # Works, but uses light theme.
            pyzo.config = ConfigShim()

        pyzo.loadConfig()
            # To be replaced by LeoPyzoConfig.loadConfig.
        #
        # Probably will never be needed: it's fine to load .leo files for now.
        if 0:
            # Ignore .leo files.
            from pyzo.core.editorTabs import EditorTabs
            self.old_loadFile = EditorTabs.loadFile
            g.funcToMethod(loadFile, EditorTabs)
    #@+node:ekr.20190331173436.1: *3* MainWindowShim.setMainTitle
    def setMainTitle(self, path=None):
        """ Set the title of the main window, by giving a file path.
        """
        self.setWindowTitle('Leo Main Window')
        ### From MainWindow
            # if not path:
                # # Plain title
                # title = "Interactive Editor for Python"
            # else:
                # # Title with a filename
                # name = os.path.basename(path)
                # if os.path.isfile(path):
                    # pass
                # elif name == path:
                    # path = translate("main", 'unsaved')
                # else:
                    # pass  # We hope the given path is informative
                # # Set title
                # tmp = { 'fileName':name, 'filename':name, 'name':name,
                        # 'fullPath':path, 'fullpath':path, 'path':path }
                # title = pyzo.config.advanced.titleText.format(**tmp)
        
            # # Set
            # self.setWindowTitle(title)
    #@+node:ekr.20190317084647.4: *3* MainWindowShim.setStyleSheet (override)
    firstStyleSheet = True

    def setStyleSheet(self, style, *args, **kwargs):
        # print('MainWindowShim.setStyleSheet', style, args, kwargs)
        # A hack: Ignore the first call.
        if self.firstStyleSheet:
            self.firstStyleSheet = False
            return
        QtWidgets.QMainWindow.setStyleSheet(self, style)
    #@-others
#@+node:ekr.20190330100146.1: ** class MenuShim (object) (To do)
class MenuShim (object):
    '''Adaptor class standing between Leo and Pyzo menus.'''
    #@+others
    #@-others
#@+node:ekr.20190401085747.1: ** class OutlineEditorShim (object) (Experimental)
class OutlineEditorShim(object):
    '''A class to make a Leo outline a pyzo editor, residing in a pyzo editor tab.'''
    ### Completely experimental
#@+node:ekr.20190317082435.1: ** class SplashShim (QtWidgets.QWidget)
class SplashShim(QtWidgets.QWidget):
    '''A do-nothing splash widget.'''
    
    def __init__(self, parent, **kwargs):
        # This ctor is required, because it is called with kwargs.
        QtWidgets.QWidget.__init__(self, parent)
#@+node:ekr.20190401074804.1: ** class ToolShim (Needed???)
class ToolShim (object):
    '''
    A Shim to make a QWidget into a Pyzo Tool window.
    
    From the docstring in pyzo/tools.__init__.py:
    
    A tool consists of a module which contains a class:
    - The id of a tool is its lower-cased module name.
    - The module should contain a class corresponding to its id.
    
    The module may contain the following extra variables,
    which should be placed within the first 50 lines of code:
    
    - tool_name:      A readable name for the tool. May contain spaces.
    - tool_summary:   A single line short summary of the tool.
                      Will be displayed in the statusbar.
    '''
#@-others
#@-leo