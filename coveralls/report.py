from coverage.report import Reporter


class CoverallsReporter(Reporter):
    def report(self, base_dir):
        self.find_code_units(None)
        ret = []
        for cu in self.code_units:
            with open(cu.filename) as fp:
                source = fp.readlines()
            analysis = self.coverage._analyze(cu)
            coverage_list = [None for _ in source]
            for lineno, line in enumerate(source):
                if lineno + 1 in analysis.statements:
                    coverage_list[lineno] = int(lineno + 1 not in analysis.missing)
            ret.append({
                'name': cu.filename.replace(base_dir, '').lstrip('/'),
                'source': ''.join(source).rstrip(),
                'coverage': coverage_list,
            })
        return ret
