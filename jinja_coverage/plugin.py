"""The Jinja2 coverage plugin."""

import os.path
import pathlib

import coverage.plugin
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader


class JinjaPlugin(coverage.plugin.CoveragePlugin):
    def __init__(self, options):
        self.template_directory = pathlib.Path(options.get("template_directory"))
        self.environment = Environment(
            loader=FileSystemLoader(str(self.template_directory)),
            extensions=[]
        )

    def _is_in_template_directory(self, filename):
        file_path = pathlib.Path(filename)
        try:
            file_path.relative_to(self.template_directory)
        except ValueError:
            return False
        else:
            return True

    def file_tracer(self, filename):
        if self._is_in_template_directory(filename):
            return FileTracer(filename)

    def file_reporter(self, filename):
        if self._is_in_template_directory(filename):
            return FileReporter(filename, self.environment)


class FileTracer(coverage.plugin.FileTracer):
    def __init__(self, filename):
        self.metadata = {'filename': filename}

    def source_filename(self):
        return self.metadata["filename"]

    def line_number_range(self, frame):
        lineno = -1
        env = frame.f_locals.get('environment')
        if env:
            template = env.get_template(os.path.basename(frame.f_code.co_filename))
            lineno = template.get_corresponding_lineno(frame.f_lineno)

        if lineno == 0:
            # Zeros should not be tracked, return -1 to skip them.
            lineno = -1
        return lineno, lineno


class FileReporter(coverage.plugin.FileReporter):
    def __init__(self, filename, environment):
        super(FileReporter, self).__init__(filename)
        self._source = None
        self.environment = environment

    def source(self):
        if self._source is None:
            with open(self.filename) as f:
                self._source = f.read()
        return self._source

    def lines(self):
        source_lines = set()
        # this is what Jinja2 does when parsing, however not sure
        # if we do it correctly b/c Jinja doesn't provide correct
        # mappings between compiled Python code and HTML template text
        tokens = self.environment._tokenize(self.source(), self.filename)

        for token in tokens:
            source_lines.add(token.lineno)

        return source_lines
