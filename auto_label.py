""" auto_label.py

Usage:
    auto_label.py <project_name>

Options:
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

def logged_in_to_lspace(br, user):
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

if __name__ == "__main__":

    args = docopt.docopt(__doc__)

    logging.basicConfig(level=logging.INFO)

    username = os.getenv("LSPACE_USERNAME")
    pwd = os.getenv("LSPACE_PASSWORD")

    br = get_browser(HMS_ROOT + "/members/login")

    logging.info("Attempting login as {}...".format(username))
    
    try_login(br, username, pwd)


    if not logged_in_to_lspace(br, username):
       sys.exit("Could not login to lspace")

    try_print_label(br, args["<project_name>"])

