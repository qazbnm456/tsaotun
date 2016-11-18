"""This module contains the formatter class of `docker ps` class"""

from pystache import TemplateSpec

class Formatter(TemplateSpec):
    """This class represents a formatter for `docker ps` command"""

    formatKey = ["table", "raw"]

    def __init__(self, formatType="table"):
        if formatType in self.formatKey:
            self.template_name = formatType + "_formatter"
        else:
            self.template_name = "table_formatter"
