from coverage.control import coverage
from coveralls.report import CoverallsReporter


class coveralls(coverage):
    def coveralls(self, base_dir):
        return CoverallsReporter(self, self.config).report(base_dir)
