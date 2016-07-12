""" auto_project.py

Usage:
    auto_project.py --create <project_name> <description> [-v]
    auto_project.py --print <project_name> [-v]
    auto_project.py --list [--detail | -d] [-v]

Options:
    --verbose, -v   Verbose output (turn on logging messages)
    --list, -l      List all projects
    --create, -c    Create the specified project  (description must be specified)
    --print, -p     Print a label for the specified project
    --detail, -d   Print project description and dates as well as name
    <project_name>  Name of the project to print label for
    <description>   Description of a new project

"""

import os
import sys
import docopt
import datetime
import logging

from hms import HMS

def print_projects(projects, print_detail):
    for project in projects:
        if print_detail:
            print(project.describe())
        else:
            print(project.name)

if __name__ == "__main__":

    args = docopt.docopt(__doc__)

    if args["--create"] and args["<description>"] is None:
        sys.exit("Description must be provided if creating project")

    if args["--verbose"]:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.ERROR)

    username = os.getenv("HMS_USERNAME")
    pwd = os.getenv("HMS_PASSWORD")

    if not username:
        sys.exit("HMS_USERNAME environment variable not set!")

    if not pwd:
        sys.exit("HMS_PASSWORD environment variable not set!")
    
    logging.info("Attempting login as {}...".format(username))

    hms = HMS()

    hms.try_login(username, pwd)

    if not hms.is_logged_in(username):
       sys.exit("Could not login to hms")

    if args["--create"]:
        hms.create_project(args["<project_name>"], args["<description>"])

    elif args["--print"]:
        hms.print_project_label(br, args["<project_name>"])
    
    elif args["--list"]:
        print_detail = args["--detail"]

        projects = hms.get_projects()
        
        print_projects(projects, print_detail)
