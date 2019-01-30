#!/usr/bin/env python
import sys
import os
from optparse import OptionParser

try:
    from xml.etree.ElementTree import XML
except ImportError:
    from elementtree.ElementTree import XML
try:
    from urllib import pathname2url, url2pathname
except ImportError:
    from urllib.request import pathname2url, url2pathname

import codecs
import cgi
import time
import shutil
import urllib


class Mm2Notes:
    def __init__(self):
        self.as_html = True
        self.title_text = ''
        self.full_html = True
        self.order_by_time = False

    def set_order_by_time(self, order_by_time):
        self.order_by_time = order_by_time

    def open(self, infilename):
        """ Open the .mm file and create a notes as a list of lines """
        fd = open(infilename)
        infile = fd.read()
        et_in = self.xmlparse(infile)
        # jsons = self.convert(et_in)
        return et_in

    def xmlparse(self, text):
        """ import the XML text into self.et_in  """
        return XML(text)

    def is_dir(self, node):
        """ import the XML text into self.et_in  """
        if 'LINK' in node.attrib:
            link = node.attrib['LINK']
            linkfile = link[6:]
            linkfile = os.path.abspath(linkfile)
            return os.path.isdir(linkfile)
        else:
            return 1 == len(node.attrib['TEXT'].split('.'))

    def deeper(self, dir):
        if not os.path.exists(dir):
            os.mkdir(dir)
            print('create dir {}'.format(os.path.join(os.getcwd(),dir)))
        os.chdir(dir)
        # print(os.getcwd())

    def floatup(self):
        os.chdir('..')
        # print(os.getcwd())

    def copyfile(self, link):
        linkfile = link[6:]
        linkfile = os.path.abspath(linkfile)
        curdir = os.path.abspath(os.getcwd())
        print('copy from {} to {}'.format(linkfile, curdir))
        shutil.copy(linkfile, curdir)

    def mkdirs(self, in_node):
        nodes = in_node.findall('node')
        if len(nodes) == 0:
            # ????
            self.floatup()
            return 0
        else:
            # ?????
            for node in nodes:
                if self.is_dir(node):
                    # ???????????
                    subdir = node.attrib['TEXT']
                    self.deeper(subdir)
                    self.mkdirs(node)
                elif 'LINK' in node.attrib:
                    # ????????????????
                    link = node.attrib['LINK']
                    self.copyfile(link)

        self.floatup()
        return 1


def parse_command_line():
    usage = """%prog <mmfile> -o [<htmloutput>]
Create a FreeMind (.mm) document (see http://freemind.sourceforge.net/wiki/index.php/Main_Page)
the main node will be the title page and the lower nodes will be pages.
"""
    parser = OptionParser(usage)
    parser.add_option('-o', '--output', dest="outpath")
    parser.add_option('-m', '--minutes', dest="order_by_time",
                      action='store_true',
                      help="Order the minutes by time and show the time")
    (options, args) = parser.parse_args()
    if len(args) == 0:
        parser.print_usage()
        sys.exit(-1)

    infile = args[0]
    if not infile.endswith('.mm'):
        print("Input file must end with '.mm'")
        parser.print_usage()
        sys.exit(-1)

    mm2notes = Mm2Notes()
    elements = mm2notes.open(infile)
    if options.outpath:
        # Writing out the HTML in correct UTF-8 format is a little tricky.
        rootdir = options.outpath
        print("Outputting to '%s'" % (rootdir))
        if os.path.exists(rootdir):
            # rootdir=rootdir+'1'
            shutil.rmtree(rootdir)

        os.makedirs(rootdir)
        os.chdir(rootdir)

    mm2notes.mkdirs(elements)
    # mm2notes.set_order_by_time(options.order_by_time)

    # mm2notes.write(outfile, lines)


if __name__ == "__main__":
    parse_command_line()
