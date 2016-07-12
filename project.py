import datetime

from collections import namedtuple

class Project(namedtuple("Project", ["name", "desc", "start", "complete", "state", "links"])):

    __slots__ = ()

    def can_print_label(self):
        return any(["printDNHLabel" in link for link in self.links])

    @staticmethod
    def build_link_dict(cell):
        hrefs = [link["href"] for link in cell.select("a")]
        links = {}
        for href in hrefs:
            if "view" in href:
                links["view"] = href
            elif "resume" in href:
                links["resume"] = href
            elif "markComplete" in href:
                links["markComplete"] = href
            elif "printDNHLabel" in href:
                links["printDNHLabel"] = href
            
        return links

    @classmethod    
    def from_rows(cls, rows):
        projects = [cls.from_row(row) for row in rows]
        projects = [p for p in projects if p]
        return projects

    @classmethod
    def from_row(cls, row):
        cells = row.select("td")

        if len(cells):
            name = cells[0].text.strip()
            desc = cells[1].text.strip()
            start = datetime.datetime.strptime(cells[2].text.strip(), "%Y-%m-%d")
            try:
                complete = datetime.datetime.strptime(cells[3].text.strip(), "%Y-%m-%d")
            except ValueError:
                complete = None

            state = cells[4].text.strip()

            links = cls.build_link_dict(cells[5])
            return cls(name, desc, start, complete, state, links)

        return None

    def describe(self):
        if self.complete:
            return "{} ({}), started {:%Y-%m-%d}, completed {:%Y-%m-%d}".format(self.name, self.desc, self.start, self.complete)
        else:
            return "{} ({}), started {:%Y-%m-%d}".format(self.name, self.desc, self.start)
        