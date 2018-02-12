#@+leo-ver=5-thin
#@+node:ekr.20031218072017.3630: * @file leoCompare.py
"""Leo's base compare class."""
import leo.core.leoGlobals as g
import difflib
import filecmp
import os
#@+others
#@+node:ekr.20031218072017.3631: ** choose
def choose(cond, a, b): # warning: evaluates all arguments
    if cond: return a
    else: return b
#@+node:ekr.20031218072017.3632: ** go
def go():
    compare = LeoCompare(
        commands=None,
        appendOutput=True,
        ignoreBlankLines=True,
        ignoreFirstLine1=False,
        ignoreFirstLine2=False,
        ignoreInteriorWhitespace=False,
        ignoreLeadingWhitespace=True,
        ignoreSentinelLines=False,
        limitCount=9, # Zero means don't stop.
        limitToExtension=".py", # For directory compares.
        makeWhitespaceVisible=True,
        printBothMatches=False,
        printMatches=False,
        printMismatches=True,
        printTrailingMismatches=False,
        outputFileName=None)
    if 1: # Compare all files in Tangle test directories
        path1 = "c:\\prog\\test\\tangleTest\\"
        path2 = "c:\\prog\\test\\tangleTestCB\\"
        compare.compare_directories(path1, path2)
    else: # Compare two files.
        name1 = "c:\\prog\\test\\compare1.txt"
        name2 = "c:\\prog\\test\\compare2.txt"
        compare.compare_files(name1, name2)
#@+node:ekr.20031218072017.3633: ** class LeoCompare
class BaseLeoCompare(object):
    """The base class for Leo's compare code."""
    #@+others
    #@+node:ekr.20031218072017.3634: *3* compare.__init__
    # All these ivars are known to the LeoComparePanel class.

    def __init__(self,
        # Keyword arguments are much convenient and more clear for scripts.
        commands=None,
        appendOutput=False,
        ignoreBlankLines=True,
        ignoreFirstLine1=False,
        ignoreFirstLine2=False,
        ignoreInteriorWhitespace=False,
        ignoreLeadingWhitespace=True,
        ignoreSentinelLines=False,
        limitCount=0, # Zero means don't stop.
        limitToExtension=".py", # For directory compares.
        makeWhitespaceVisible=True,
        printBothMatches=False,
        printMatches=False,
        printMismatches=True,
        printTrailingMismatches=False,
        outputFileName=None
    ):
        # It is more convenient for the LeoComparePanel to set these directly.
        self.c = commands
        self.appendOutput = appendOutput
        self.ignoreBlankLines = ignoreBlankLines
        self.ignoreFirstLine1 = ignoreFirstLine1
        self.ignoreFirstLine2 = ignoreFirstLine2
        self.ignoreInteriorWhitespace = ignoreInteriorWhitespace
        self.ignoreLeadingWhitespace = ignoreLeadingWhitespace
        self.ignoreSentinelLines = ignoreSentinelLines
        self.limitCount = limitCount
        self.limitToExtension = limitToExtension
        self.makeWhitespaceVisible = makeWhitespaceVisible
        self.printBothMatches = printBothMatches
        self.printMatches = printMatches
        self.printMismatches = printMismatches
        self.printTrailingMismatches = printTrailingMismatches
        # For communication between methods...
        self.outputFileName = outputFileName
        self.fileName1 = None
        self.fileName2 = None
        # Open files...
        self.outputFile = None
    #@+node:ekr.20031218072017.3635: *3* compare_directories (entry)
    # We ignore the filename portion of path1 and path2 if it exists.

    def compare_directories(self, path1, path2):
        # Ignore everything except the directory name.
        dir1 = g.os_path_dirname(path1)
        dir2 = g.os_path_dirname(path2)
        dir1 = g.os_path_normpath(dir1)
        dir2 = g.os_path_normpath(dir2)
        if dir1 == dir2:
            return self.show("Please pick distinct directories.")
        try:
            list1 = os.listdir(dir1)
        except Exception:
            return self.show("invalid directory:" + dir1)
        try:
            list2 = os.listdir(dir2)
        except Exception:
            return self.show("invalid directory:" + dir2)
        if self.outputFileName:
            self.openOutputFile()
        ok = self.outputFileName is None or self.outputFile
        if not ok: return None
        # Create files and files2, the lists of files to be compared.
        files1 = []
        files2 = []
        for f in list1:
            junk, ext = g.os_path_splitext(f)
            if self.limitToExtension:
                if ext == self.limitToExtension:
                    files1.append(f)
            else:
                files1.append(f)
        for f in list2:
            junk, ext = g.os_path_splitext(f)
            if self.limitToExtension:
                if ext == self.limitToExtension:
                    files2.append(f)
            else:
                files2.append(f)
        # Compare the files and set the yes, no and missing lists.
        yes = []; no = []; missing1 = []; missing2 = []
        for f1 in files1:
            head, f2 = g.os_path_split(f1)
            if f2 in files2:
                try:
                    name1 = g.os_path_join(dir1, f1)
                    name2 = g.os_path_join(dir2, f2)
                    val = filecmp.cmp(name1, name2, 0)
                    if val: yes.append(f1)
                    else: no.append(f1)
                except Exception:
                    self.show("exception in filecmp.cmp")
                    g.es_exception()
                    missing1.append(f1)
            else:
                missing1.append(f1)
        for f2 in files2:
            head, f1 = g.os_path_split(f2)
            if f1 not in files1:
                missing2.append(f1)
        # Print the results.
        for kind, files in (
            ("----- matches --------", yes),
            ("----- mismatches -----", no),
            ("----- not found 1 ------", missing1),
            ("----- not found 2 ------", missing2),
        ):
            self.show(kind)
            for f in files:
                self.show(f)
        if self.outputFile:
            self.outputFile.close()
            self.outputFile = None
        return None # To keep pychecker happy.
    #@+node:ekr.20031218072017.3636: *3* compare_files (entry)
    def compare_files(self, name1, name2):
        if name1 == name2:
            self.show("File names are identical.\nPlease pick distinct files.")
            return
        self.compare_two_files(name1, name2)
    #@+node:ekr.20180211123531.1: *3* compare_list_of_files (entry for scripts)
    def compare_list_of_files(self, aList1):
        
        aList = list(set(aList1))
        while len(aList) > 1:
            path1 = aList[0]
            for path2 in aList[1:]:
                g.trace('COMPARE', path1, path2)
                self.compare_two_files(path1, path2)
    #@+node:ekr.20180211123741.1: *3* compare_two_files
    def compare_two_files(self, name1, name2):
        '''A helper function.'''
        f1 = f2 = None
        try:
            f1 = self.doOpen(name1)
            f2 = self.doOpen(name2)
            if self.outputFileName:
                self.openOutputFile()
            ok = self.outputFileName is None or self.outputFile
            ok = 1 if ok and ok != 0 else 0
            if f1 and f2 and ok:
                # Don't compare if there is an error opening the output file.
                self.compare_open_files(f1, f2, name1, name2)
        except Exception:
            self.show("exception comparing files")
            g.es_exception()
        try:
            if f1: f1.close()
            if f2: f2.close()
            if self.outputFile:
                self.outputFile.close(); self.outputFile = None
        except Exception:
            self.show("exception closing files")
            g.es_exception()
    #@+node:ekr.20031218072017.3637: *3* compare_lines
    def compare_lines(self, s1, s2):
        if self.ignoreLeadingWhitespace:
            s1 = s1.lstrip()
            s2 = s2.lstrip()
        if self.ignoreInteriorWhitespace:
            k1 = g.skip_ws(s1, 0)
            k2 = g.skip_ws(s2, 0)
            ws1 = s1[: k1]
            ws2 = s2[: k2]
            tail1 = s1[k1:]
            tail2 = s2[k2:]
            tail1 = tail1.replace(" ", "").replace("\t", "")
            tail2 = tail2.replace(" ", "").replace("\t", "")
            s1 = ws1 + tail1
            s2 = ws2 + tail2
        return s1 == s2
    #@+node:ekr.20031218072017.3638: *3* compare_open_files
    def compare_open_files(self, f1, f2, name1, name2):
        # self.show("compare_open_files")
        lines1 = 0; lines2 = 0; mismatches = 0; printTrailing = True
        sentinelComment1 = sentinelComment2 = None
        if self.openOutputFile():
            self.show("1: " + name1)
            self.show("2: " + name2)
            self.show("")
        s1 = s2 = None
        #@+<< handle opening lines >>
        #@+node:ekr.20031218072017.3639: *4* << handle opening lines >>
        if self.ignoreSentinelLines:
            s1 = g.readlineForceUnixNewline(f1); lines1 += 1
            s2 = g.readlineForceUnixNewline(f2); lines2 += 1
            # Note: isLeoHeader may return None.
            sentinelComment1 = self.isLeoHeader(s1)
            sentinelComment2 = self.isLeoHeader(s2)
            if not sentinelComment1: self.show("no @+leo line for " + name1)
            if not sentinelComment2: self.show("no @+leo line for " + name2)
        if self.ignoreFirstLine1:
            if s1 is None:
                g.readlineForceUnixNewline(f1); lines1 += 1
            s1 = None
        if self.ignoreFirstLine2:
            if s2 is None:
                g.readlineForceUnixNewline(f2); lines2 += 1
            s2 = None
        #@-<< handle opening lines >>
        while 1:
            if s1 is None:
                s1 = g.readlineForceUnixNewline(f1); lines1 += 1
            if s2 is None:
                s2 = g.readlineForceUnixNewline(f2); lines2 += 1
            #@+<< ignore blank lines and/or sentinels >>
            #@+node:ekr.20031218072017.3640: *4* << ignore blank lines and/or sentinels >>
            # Completely empty strings denotes end-of-file.
            if s1:
                if self.ignoreBlankLines and s1.isspace():
                    s1 = None; continue
                if self.ignoreSentinelLines and sentinelComment1 and self.isSentinel(s1, sentinelComment1):
                    s1 = None; continue
            if s2:
                if self.ignoreBlankLines and s2.isspace():
                    s2 = None; continue
                if self.ignoreSentinelLines and sentinelComment2 and self.isSentinel(s2, sentinelComment2):
                    s2 = None; continue
            #@-<< ignore blank lines and/or sentinels >>
            n1 = len(s1); n2 = len(s2)
            if n1 == 0 and n2 != 0: self.show("1.eof***:")
            if n2 == 0 and n1 != 0: self.show("2.eof***:")
            if n1 == 0 or n2 == 0: break
            match = self.compare_lines(s1, s2)
            if not match: mismatches += 1
            #@+<< print matches and/or mismatches >>
            #@+node:ekr.20031218072017.3641: *4* << print matches and/or mismatches >>
            if self.limitCount == 0 or mismatches <= self.limitCount:
                if match and self.printMatches:
                    if self.printBothMatches:
                        z1 = "1." + str(lines1)
                        z2 = "2." + str(lines2)
                        self.dump(z1.rjust(6) + ' :', s1)
                        self.dump(z2.rjust(6) + ' :', s2)
                    else:
                        self.dump(str(lines1).rjust(6) + ' :', s1)
                if not match and self.printMismatches:
                    z1 = "1." + str(lines1)
                    z2 = "2." + str(lines2)
                    self.dump(z1.rjust(6) + '*:', s1)
                    self.dump(z2.rjust(6) + '*:', s2)
            #@-<< print matches and/or mismatches >>
            #@+<< warn if mismatch limit reached >>
            #@+node:ekr.20031218072017.3642: *4* << warn if mismatch limit reached >>
            if self.limitCount > 0 and mismatches >= self.limitCount:
                if printTrailing:
                    self.show("")
                    self.show("limit count reached")
                    self.show("")
                    printTrailing = False
            #@-<< warn if mismatch limit reached >>
            s1 = s2 = None # force a read of both lines.
        #@+<< handle reporting after at least one eof is seen >>
        #@+node:ekr.20031218072017.3643: *4* << handle reporting after at least one eof is seen >>
        if n1 > 0:
            lines1 += self.dumpToEndOfFile("1.", f1, s1, lines1, printTrailing)
        if n2 > 0:
            lines2 += self.dumpToEndOfFile("2.", f2, s2, lines2, printTrailing)
        self.show("")
        self.show("lines1:" + str(lines1))
        self.show("lines2:" + str(lines2))
        self.show("mismatches:" + str(mismatches))
        #@-<< handle reporting after at least one eof is seen >>
    #@+node:ekr.20031218072017.3644: *3* compare.filecmp
    def filecmp(self, f1, f2):
        val = filecmp.cmp(f1, f2)
        if 1:
            if val: self.show("equal")
            else: self.show("*** not equal")
        else:
            self.show("filecmp.cmp returns:")
            if val: self.show(str(val) + " (equal)")
            else: self.show(str(val) + " (not equal)")
        return val
    #@+node:ekr.20031218072017.3645: *3* compare.utils...
    #@+node:ekr.20031218072017.3646: *4* compare.doOpen
    def doOpen(self, name):
        try:
            f = open(name, 'r')
            return f
        except Exception:
            self.show("can not open:" + '"' + name + '"')
            return None
    #@+node:ekr.20031218072017.3647: *4* compare.dump
    def dump(self, tag, s):
        compare = self; out = tag
        for ch in s[: -1]: # don't print the newline
            if compare.makeWhitespaceVisible:
                if ch == '\t':
                    out += "["; out += "t"; out += "]"
                elif ch == ' ':
                    out += "["; out += " "; out += "]"
                else: out += ch
            else:
                if 1:
                    out += ch
                else: # I don't know why I thought this was a good idea ;-)
                    if ch == '\t' or ch == ' ':
                        out += ' '
                    else:
                        out += ch
        self.show(out)
    #@+node:ekr.20031218072017.3648: *4* compare.dumpToEndOfFile
    def dumpToEndOfFile(self, tag, f, s, line, printTrailing):
        trailingLines = 0
        while 1:
            if not s:
                s = g.readlineForceUnixNewline(f)
            if not s:
                break
            trailingLines += 1
            if self.printTrailingMismatches and printTrailing:
                z = tag + str(line)
                tag2 = z.rjust(6) + "+:"
                self.dump(tag2, s)
            s = None
        self.show(tag + str(trailingLines) + " trailing lines")
        return trailingLines
    #@+node:ekr.20031218072017.3649: *4* compare.isLeoHeader & isSentinel
    #@+at These methods are based on AtFile.scanHeader(). They are simpler
    # because we only care about the starting sentinel comment: any line
    # starting with the starting sentinel comment is presumed to be a
    # sentinel line.
    #@@c

    def isLeoHeader(self, s):
        tag = "@+leo"
        j = s.find(tag)
        if j > 0:
            i = g.skip_ws(s, 0)
            if i < j: return s[i: j]
            else: return None
        else: return None

    def isSentinel(self, s, sentinelComment):
        i = g.skip_ws(s, 0)
        return g.match(s, i, sentinelComment)
    #@+node:ekr.20031218072017.1144: *4* compare.openOutputFile
    def openOutputFile(self):
        if self.outputFileName is None:
            return
        theDir, name = g.os_path_split(self.outputFileName)
        if not theDir:
            self.show("empty output directory")
            return
        if not name:
            self.show("empty output file name")
            return
        if not g.os_path_exists(theDir):
            self.show("output directory not found: " + theDir)
        else:
            try:
                if self.appendOutput:
                    self.show("appending to " + self.outputFileName)
                    self.outputFile = open(self.outputFileName, "ab")
                else:
                    self.show("writing to " + self.outputFileName)
                    self.outputFile = open(self.outputFileName, "wb")
            except Exception:
                self.outputFile = None
                self.show("exception opening output file")
                g.es_exception()
    #@+node:ekr.20031218072017.3650: *4* compare.show
    def show(self, s):
        # g.pr(s)
        if self.outputFile:
            # self.outputFile is opened in 'wb' mode.
            s = g.toEncodedString(s + '\n')
            self.outputFile.write(s)
        elif self.c:
            g.es(s)
        else:
            g.pr(s)
            g.pr('')
    #@+node:ekr.20031218072017.3651: *4* compare.showIvars
    def showIvars(self):
        self.show("fileName1:" + str(self.fileName1))
        self.show("fileName2:" + str(self.fileName2))
        self.show("outputFileName:" + str(self.outputFileName))
        self.show("limitToExtension:" + str(self.limitToExtension))
        self.show("")
        self.show("ignoreBlankLines:" + str(self.ignoreBlankLines))
        self.show("ignoreFirstLine1:" + str(self.ignoreFirstLine1))
        self.show("ignoreFirstLine2:" + str(self.ignoreFirstLine2))
        self.show("ignoreInteriorWhitespace:" + str(self.ignoreInteriorWhitespace))
        self.show("ignoreLeadingWhitespace:" + str(self.ignoreLeadingWhitespace))
        self.show("ignoreSentinelLines:" + str(self.ignoreSentinelLines))
        self.show("")
        self.show("limitCount:" + str(self.limitCount))
        self.show("printMatches:" + str(self.printMatches))
        self.show("printMismatches:" + str(self.printMismatches))
        self.show("printTrailingMismatches:" + str(self.printTrailingMismatches))
    #@-others

class LeoCompare(BaseLeoCompare):
    """
    A class containing Leo's compare code.
    
    These are not very useful comparisons.
    """
    pass
#@+node:ekr.20180211170333.1: ** class CompareLeoOutlines
class CompareLeoOutlines:
    '''
    A class to do outline-oriented diffs of two or more .leo files.
    Similar to GitDiffController, adapted for use by scripts.
    '''
    
    def __init__ (self, c):
        '''Ctor for the LeoOutlineCompare class.'''
        self.c = c
        self.file_node = None
        self.open_commanders = [frame.c for frame in g.app.windowList]
        self.newly_opened_commanders = []
        self.root = None
        self.path1 = None
        self.path2 = None

    #@+others
    #@+node:ekr.20180211170333.2: *3* loc.diff_list_of_files (entry)
    def diff_list_of_files(self, aList, show_files=False):
        '''The main entry point for scripts.'''
        if len(aList) < 2:
            g.trace('Not enough files in', repr(aList))
            return
        self.root = self.create_root(aList)
        self.show_files = show_files
        while len(aList) > 1:
            self.path1 = aList[0]
            aList = aList[1:]
            for path2 in aList:
                self.path2 = path2
                self.diff_two_files(self.path1, self.path2)
        self.finish()
    #@+node:ekr.20180211170333.3: *3* loc.diff_two_files
    def diff_two_files(self, fn1, fn2):
        '''Create an outline describing the git diffs for fn.'''
        g.trace('DIFF:...\n%s\n%s' % (fn1, fn2))
        s1 = self.get_file(fn1)
        s2 = self.get_file(fn2)
        lines1 = g.splitLines(s1)
        lines2 = g.splitLines(s2)
        diff_list = list(difflib.unified_diff(lines1, lines2, fn1, fn2))
        diff_list.insert(0, '@language patch\n')
        self.file_node = self.create_file_node(diff_list, fn1, fn2)
        # These will be left open
        c1 = self.open_outline_only(fn1)
        c2 = self.open_outline_only(fn2)
        if c1 and c2:
            self.make_diff_outlines(c1, c2)
            self.file_node.b = '%s\n@language %s\n' % (
                self.file_node.b.rstrip(),
                c2.target_language)
    #@+node:ekr.20180211170333.4: *3* loc.Utils
    #@+node:ekr.20180211170333.5: *4* loc.compute_dicts
    def compute_dicts(self, c1, c2):
        '''Compute inserted, deleted, changed dictionaries.'''
        trace = False and not g.unitTesting
        d1 = {v.fileIndex: v for v in c1.all_unique_nodes()} 
        d2 = {v.fileIndex: v for v in c2.all_unique_nodes()}
        if trace:
            g.trace('len(d1)', len(d1.keys()))
            g.trace('len(d2)', len(d2.keys()))
        added   = {key: d2.get(key) for key in d2 if not d1.get(key)}
        deleted = {key: d1.get(key) for key in d1 if not d2.get(key)}
        changed = {}
        for key in d1:
            if key in d2:
                v1 = d1.get(key)
                v2 = d2.get(key)
                assert v1 and v2
                assert v1.context != v2.context
                if v1.h != v2.h or v1.b != v2.b:
                    changed[key] = (v1, v2)
        if trace:
            for kind, d in (('added', added), ('deleted', deleted), ('changed', changed)):
                g.trace(kind)
                g.printObj(d)
        return added, deleted, changed
    #@+node:ekr.20180211170333.6: *4* loc.create_compare_node
    def create_compare_node(self, c1, c2, d, kind):
        '''Create nodes describing the changes.'''
        if not d:
            return
        parent = self.file_node.insertAsLastChild()
        parent.setHeadString(kind)
        fn1, fn2 = c1.fileName(), c2.fileName()
        sfn1, sfn2 = c1.shortFileName(), c2.shortFileName()
        for key in d:
            if kind.lower() == 'changed':
                v1, v2 = d.get(key)
                # Organizer node: contains diff
                organizer = parent.insertAsLastChild()
                organizer.h = v2.h
                body = list(difflib.unified_diff(
                    g.splitLines(v1.b),
                    g.splitLines(v2.b),
                    self.path1,
                    self.path2,
                ))
                if ''.join(body).strip():
                    body.insert(0, '@language patch\n')
                    body.append('@language %s\n' % (c2.target_language))
                else:
                    body = ['Only headline has changed']
                organizer.b = ''.join(body)
                # Node 2: Old node
                p2 = organizer.insertAsLastChild()
                # p2.h = 'Old:' + v1.h
                p2.h = fn1 if sfn1 == sfn2 else sfn1
                p2.h = p2.h + ':' + v1.h
                p2.b = v1.b
                # Node 3: New node
                assert v1.fileIndex == v2.fileIndex
                p_in_c = self.find_gnx(self.c, v1.fileIndex)
                if p_in_c: # Make a clone, if possible.
                    p3 = p_in_c.clone()
                    p3.moveToLastChildOf(organizer)
                else:
                    p3 = organizer.insertAsLastChild()
                    # p3.h = 'New:' + v2.h
                    p3.h = fn2 if sfn1 == sfn2 else sfn2
                    p3.h = p3.h + ':' + v2.h
                    p3.b = v2.b
            else:
                v = d.get(key)
                p = parent.insertAsLastChild()
                p.h = v.h
                p.b = v.b
    #@+node:ekr.20180211170333.7: *4* loc.create_file_node
    def create_file_node(self, diff_list, fn1, fn2):
        '''Create an organizer node for the file.'''
        p = self.root.insertAsLastChild()
        p.h = '%s, %s' % (g.shortFileName(fn1).strip(), g.shortFileName(fn2).strip())
        p.b = ''.join(diff_list)
        return p
    #@+node:ekr.20180211170333.8: *4* loc.create_root
    def create_root(self, aList):
        '''Create the top-level organizer node describing all the diffs.'''
        c = self.c
        g.trace('*****', g.callers())
        p = c.lastTopLevel().insertAfter()
        p.h = 'outline diff'
        p.b = '\n'.join(aList) + '\n'
        return p
    #@+node:ekr.20180211170333.9: *4* loc.find_gnx
    def find_gnx(self, c, gnx):
        '''Return a position in c having the given gnx.'''
        for p in c.all_unique_positions():
            if p.v.fileIndex == gnx:
                return p
        return None
    #@+node:ekr.20180211170333.10: *4* loc.finish
    def finish(self):
        '''Finish execution of this command.'''
        c = self.c
        if self.show_files:
            if hasattr(g.app.gui, 'frameFactory'):
                tff = g.app.gui.frameFactory
                tff.setTabForCommander(c)
        c.contractAllHeadlines(redrawFlag=False)
        self.root.expand()
        c.selectPosition(self.root)
        c.redraw()
    #@+node:ekr.20180211170333.11: *4* loc.get_file
    def get_file(self, path):
        '''Return the contents of the file whose path is given.'''
        with open(path, 'rb') as f:
            s = f.read()
        return g.toUnicode(s).replace('\r','')
    #@+node:ekr.20180211170333.13: *4* loc.make_diff_outlines
    def make_diff_outlines(self, c1, c2):
        '''Create an outline-oriented diff from the outlines c1 and c2.'''
        added, deleted, changed = self.compute_dicts(c1, c2)
        table = (
            (added, 'Added'),
            (deleted, 'Deleted'),
            (changed, 'Changed'))
        for d, kind in table:
            self.create_compare_node(c1, c2, d, kind)
    #@+node:ekr.20180211170333.14: *4* loc.open_outline_only
    def open_outline_only(self, fn):
        '''Create a hidden temp outline for fn.'''
        # Use previously-opened outlines if possible.
        for c2 in self.newly_opened_commanders:
            if c2.fileName() == fn:
                return c2
        # Don't use any other open commanders.
        for c2 in self.open_commanders:
            if c2.fileName() == fn:
                g.trace('Can not use an open commander:', c2.shortFileName())
                return None
        # Like readOutlineOnly.
        f = open(fn, 'rb')
        gui = None if self.show_files else g.app.nullGui
        c2 = g.app.newCommander(fn, gui=gui)
        c2.fileCommands.readOutlineOnly(f, fn)
            # Closes the file
        self.newly_opened_commanders.append(c2)
        return c2
    #@-others
#@-others
#@@language python
#@@tabwidth -4
#@@pagewidth 70
#@-leo
