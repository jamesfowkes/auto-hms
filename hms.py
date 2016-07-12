import datetime

from robobrowser import RoboBrowser

from project import Project

HMS_ROOT = "https://lspace.nottinghack.org.uk/hms"

class HMS:
    
    def __init__(self):
        self.br = RoboBrowser(parser="html.parser") 
        self.last_url = None

    def ensure_url(self, url):
        if self.last_url != url:
            self.br.open(url)
            self.last_url = url

    def try_login(self, user, pwd):

        self.ensure_url(HMS_ROOT + "/members/login")

        form = self.br.get_form(id="UserLoginForm")

        form["data[User][usernameOrEmail]"].value = user
        form["data[User][password]"].value = pwd

        self.br.submit_form(form)

    def is_logged_in(self, user):
        login_div = self.br.select("div.login")
        return user in login_div[0].text

    def get_projects(self):
        self.ensure_url(HMS_ROOT + "/memberProjects/listProjects")
        return Project.from_rows(self.br.select("tr"))

    def find_project(self, name):

        projects = self.get_projects()

        for project in projects:
            if project.name == name:
                return project

    def print_project_label(self, cells):

        found_project = self.find_project(name)
        if found_project and found_project.can_print_label():
            self.br.open(HMS_ROOT + project.links["printDNHLabel"])

    def open_add_project(self):
        self.ensure_url(HMS_ROOT + "/memberProjects/add")

    def create_project(self, name, description):

        self.open_add_project()

        form = self.br.get_form(id="MemberProjectAddForm")

        form["data[MemberProject][project_name]"].value = name
        form["data[MemberProject][description]"].value = description

        self.br.submit_form(form)

    def print_label(self, href):
        if href.startswith('/hms'):
            href = href[4:]

        self.ensure_url(HMS_ROOT + href)
        
    def open_tools_booking_form(self, booking_info, tool):
        booking_url = booking_info.get_encoded_booking_url(tool)
        self.ensure_url(booking_url)

    def on_laser_booking_form(self):
        return "Add laser Booking" in self.br.select("h2")[0].text

    def try_booking(self, booking_info):
        form = self.br.get_form(id="ToolAddbookingForm")
        form["data[Tool][start_hours]"].value = "{:%H}".format(booking_info.start)
        form["data[Tool][start_mins]"].value = "{:%M}".format(booking_info.start)
        form["data[Tool][end_hours]"].valueb= "{:%H}".format(booking_info.end)
        form["data[Tool][end_mins]"].value = "{:%M}".format(booking_info.end)

        self.br.submit_form(form)

    def booking_successful(self):
        flash = self.br.select("#flashMessage")
        return "Booking Added" in flash[0].text, flash[0].text
