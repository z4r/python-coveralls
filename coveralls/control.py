from coverage.control import coverage
from coveralls.report import CoverallsReporter


class coveralls(coverage):
    def coveralls(self, base_dir, ignore_errors=False):
        reporter = CoverallsReporter(self, self.config)
        reporter.find_code_units(None)
        return reporter.report(base_dir, ignore_errors=False)
