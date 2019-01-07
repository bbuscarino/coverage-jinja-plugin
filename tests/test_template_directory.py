
import unittest
import unittest.mock as mock

from jinja_coverage import JinjaPlugin

class TemplateDirectoryTestCase(unittest.TestCase):

    def test_plugin_receives_template_directory_option_as_pathlike(self):
        options = {"template_directory": "tests/templates"}
        plugin = JinjaPlugin(options=options)

    def test_plugin_returns_file_tracer_for_any_file_in_template_directory(self):
        plugin = JinjaPlugin(options={"template_directory": "tests/templates"})
        assert plugin.file_tracer("tests/templates/hello.html") is not None
        assert plugin.file_tracer("tests/templates/nested_dir/hello.html") is not None

    def test_plugin_returns_file_reporter_for_any_file_in_template_directory(self):
        plugin = JinjaPlugin(options={"template_directory": "tests/templates"})
        assert plugin.file_reporter("tests/templates/hello.html") is not None
        assert plugin.file_reporter("tests/templates/nested_dir/hello.html") is not None

    def test_plugin_returns_none_if_file_not_in_template_directory(self):
        plugin = JinjaPlugin(options={"template_directory": "tests/templates"})
        assert plugin.file_tracer("tests/test_template_directory.py") is None
        assert plugin.file_reporter("tests/test_template_directory.py") is None
