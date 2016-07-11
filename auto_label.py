""" auto_label.py

Usage:
    auto_label.py [--create|--print] <project_name> [<description>]

Options:
    --create        Create the specified project
    --print         Print a label for the specified project (description must be specified)
    <project_name>  Name of the project to print label for

"""

import os
import sys
import docopt
import datetime
import logging
import urllib.parse

from robobrowser import RoboBrowser

HMS_ROOT = "https://lspace.nottinghack.org.uk/hms"

def get_browser(url):
    br = RoboBrowser()
    br.open(url)

    return br

def try_login(br, user, pwd):
    form = br.get_form(id="UserLoginForm")

    form["data[User][usernameOrEmail]"].value = user
    form["data[User][password]"].value = pwd

    br.submit_form(form)

def logged_into_hms(br, user):
    login_div = br.select("div.login")
    
    return user in login_div[0].text

def print_from_cells(br, cells):
    last_cell = cells[-1]
    links = last_cell.select("a")

    for link in links:
        if "printDNHLabel" in link["href"]:

            br.open(HMS_ROOT + link["href"][4:])
    
def try_print_label(br, name):

    br.open(HMS_ROOT + "/memberProjects/listProjects")

    rows = br.select("tr")

    for row in rows:
        cells = row.select("td")
        for cell in cells:
            if cell.text == name:
                print_from_cells(br, cells)

def try_create_project(br, name, description):

    br.open(HMS_ROOT + "/memberProjects/add")

    form = br.get_form(id="MemberProjectAddForm")

    form["data[MemberProject][project_name]"].value = name
    form["data[MemberProject][description]"].value = description

    br.submit_form(form)

if __name__ == "__main__":

    args = docopt.docopt(__doc__)

    if args["--create"] and args["<description>"] is None:
        sys.exit("Description must be provided if creating project")

    logging.basicConfig(level=logging.INFO)

    username = os.getenv("HMS_USERNAME")
    pwd = os.getenv("HMS_PASSWORD")

    if not username:
        sys.exit("HMS_USERNAME environment variable not set!")

    if not pwd:
        sys.exit("HMS_PASSWORD environment variable not set!")

    br = get_browser(HMS_ROOT + "/members/login")

    logging.info("Attempting login as {}...".format(username))
    
    try_login(br, username, pwd)

    if not logged_into_hms(br, username):
       sys.exit("Could not login to hms")

    if args["--create"]:
        try_create_project(br, args["<project_name>"], args["<description>"])
    elif args["--print"]:
        try_print_label(br, args["<project_name>"])

