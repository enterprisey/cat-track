#!/usr/bin/env python

import cgitb; cgitb.enable()

import cgi
import datetime
import json
import os
from string import Template
import sys
import urllib

#from wikitools import wiki
#from wikitools import api

DATA_DIR = "/data/project/apersonbot/bot/cat-track/data"

def main():
    page_template = None
    try:
        with open("/data/project/apersonbot/public_html/cat-track/template.txt") as template_file:
            page_template = Template(template_file.read())
    except IOError as error:
        print("<h1>CatTrack Error!</h1><p>I couldn't read the web template.<br /><small>Details: " + str(error) + "</small>")
        sys.exit(0)

    content = ""

    content += "<p>This is a list of the categories that have data available from {{<a href='https://en.wikipedia.org/wiki/Template:CatTrack'>CatTrack</a>}}.</p>"

    content += "<ul>\n"

    filename = next(x for x in os.listdir(DATA_DIR) if x.endswith(".json"))
    with open(DATA_DIR + os.sep + filename, "r") as file_object:
        data_from_file = json.load(file_object)
        for each_category in sorted(data_from_file.keys()):
            content += "  <li>{} (<a href='https://tools.wmflabs.org/apersonbot/cat-track/view.py?category={}'>CatTrack</a>)</li>\n".format(wikilink("Category:" + each_category), each_category.replace(" ", "+"))

    content += "</ul>\n"

    print(page_template.substitute(name="List",
                                   heading="List of all CatTrack categories",
                                   content=content))

def wikilink(page_name):
    return "<a href='https://en.wikipedia.org/wiki/{0}' title='{0} on English Wikipedia'>{0}</a>".format(page_name)

main()
