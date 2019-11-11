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

def read_sizes(category):
    """
    From DATA_DIR, create a list of tuples of the timestamp and the
    category size, specified without a namespace.
    """
    sizes = [] # (timestamp string, size)
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            with open(DATA_DIR + os.sep + filename, "r") as file_object:
                data_from_file = json.load(file_object)
                if category in data_from_file:
                    sizes.append((filename[:-5], data_from_file[category]))
    return sizes

def main():
    page_template = None
    try:
        with open("/data/project/apersonbot/public_html/cat-track/template.txt") as template_file:
            page_template = Template(template_file.read())
    except IOError as error:
        print("<h1>CatTrack Error!</h1><p class='error'>I couldn't read the web template.<br /><small>Details: " + str(error) + "</small>")
        sys.exit(0)

    other_options = "<p>You can <a href='index.html'>make a new search</a> or <a href='list.py'>view a list of available pages</a>.</p>"

    form = cgi.FieldStorage()
    category = form.getvalue("category")
    if not category:
        print(page_template.substitute(name="Error",
                                       heading="CatTrack Error!",
                                       content="<p class='error'>You didn't specify a category to look at!</p>" + other_options))
        sys.exit(0)

    category = category.replace("Category:", "")
    old_category = category

    content = ""

    sizes = read_sizes(category)

    if not sizes:
        
        # Maybe there's an "All" version of this category?
        category = "All " + old_category.replace("Articles", "articles")
        sizes = read_sizes(category)
        if sizes:
            content += (("<p>There isn't any data for \"{}\", but I found data" +
                    " for \"{}\", which is probably what you were looking fo" +
                    "r.").format(old_category, category))
        else:
            content += "<p class='error'>There isn't any data for that category!</p><p>It might not exist or have {{<a href='https://en.wikipedia.org/wiki/Template:CatTrack'>CatTrack</a>}} on it.</p>"

    # Sort by date, ascending
    sizes = sorted(sizes, key=lambda x: datetime.datetime.strptime(x[0], "%d %B %Y"))

    if sizes:
        content += "<p>Here's the size of " + wikilink("Category:" + category) + " over the time period data was collected.</p>"

        # Graph
        content += "<script type='text/javascript'>var graph_data = [%s];</script>\n" % ",".join(
            "{'time': '%s', 'count': %d}" % datapoint for datapoint in sizes)
        content += """    <p>Show:&nbsp;
          <label for='year'><input type='radio' name='length' id='year' value='year' checked />Last year</label>
          <label for='all'><input type='radio' name='length' id='all' value='all' />All time</label>
        </p>"""
        content += "<div id='graph'></div>"
        content += "<script type='text/javascript' src='graph.js'></script>"

        # List of counts
        content += "<ul>"
        for timestamp, size in sizes:
            content += "<li>{}: {:,}</li>".format(timestamp, size)
        content += "</ul>"

    content += other_options

    print(page_template.substitute(name=category,
                                   heading="CatTrack Results for \"" + old_category + "\"",
                                   content=content))

def wikilink(page_name):
    return "<a href='https://en.wikipedia.org/wiki/{0}' title='{0} on English Wikipedia'>{0}</a>".format(page_name)

main()
