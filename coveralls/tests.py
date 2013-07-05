# coding=utf-8
import json
from unittest import TestCase
from coverage.codeunit import CodeUnit
from coverage.files import FileLocator
from coveralls.control import coveralls
from coveralls.report import CoverallsReporter
from httpretty import HTTPretty, httprettified
from coveralls import api, repository, control, wear
import os


class Arguments(object):
    coveralls_url = 'https://coveralls.io/api/v1/jobs'
    repo_token = 'abcdef1234569abdcef'
    service_job_id = '4699301'
    service_name = 'travi-ci',
    base_dir = os.path.abspath('python-coveralls-example')
    data_file = os.path.join(base_dir, '.coverage')
    config_file = os.path.join(base_dir, '.coveragerc')
    ignore_errors = False


GIT_EXP = {
    'head': {
        'committer_email': '24erre@gmail.com',
        'author_email': '24erre@gmail.com',
        'author_name': u'Andrea de Marco',
        'message': u'py3',
        'committer_name': u'Andrea de Marco',
        'id': 'c2c372b16ab98e00fddcb56d818ee5be435d37ec'
    },
    'remotes': [
        {
            'url': 'https://github.com/z4r/python-coveralls-example.git',
            'name': 'origin'
        }
    ],
    'branch': 'master'
}

SOURCE_FILES = [
    {
        'source': "__author__ = 'ademarco'",
        'name': 'example/__init__.py',
        'coverage': [1]
    },
    {
        'source': '# coding=utf-8\nEUR = "€"\n\n\ndef amount(tariff, currency=EUR):\n    return \'{0} {1:.2f}\'.format(currency, float(tariff))',
        'name': 'example/exencode.py',
        'coverage': [None, 1, None, None, 1, 1]
    },
    {
        'source': "def exsum(a, b):\n    # A comment of a exsum\n    return a + b\n\n\ndef exdiff(a, b):\n    return a - b\n\n\nif __name__ == '__main__':\n    print(exsum(3,4))\n    print(exdiff(2,2))",
        'name': 'example/exmath.py',
        'coverage': [1, None, 1, None, None, 1, 0, None, None, None, None, None]
    }

]


class CoverallsTestCase(TestCase):
    @httprettified
    def test_wear(self):
        HTTPretty.register_uri(
            HTTPretty.POST,
            'https://coveralls.io/api/v1/jobs',
            body='{"message":"Job #5.1 - 100.0% Covered","url":"https://coveralls.io/jobs/5722"}'
        )
        response = wear(Arguments)
        self.assertEqual(response.json(), {u'url': u'https://coveralls.io/jobs/5722', u'message': u'Job #5.1 - 100.0% Covered'})

    def test_gitrepo(self):
        git = repository.gitrepo(Arguments.base_dir)
        self.assertEqual(git['head'], GIT_EXP['head'])
        self.assertEqual(git['remotes'], GIT_EXP['remotes'])
        self.assertTrue(git['branch'] in (GIT_EXP['branch'], 'HEAD'))

    def test_coveralls(self):
        coverage = control.coveralls(data_file=Arguments.data_file, config_file=Arguments.config_file)
        coverage.load()
        self.assertEqual(coverage.coveralls(Arguments.base_dir), SOURCE_FILES)

    @httprettified
    def test_api(self):
        HTTPretty.register_uri(
            HTTPretty.POST,
            'https://coveralls.io/api/v1/jobs',
            body='{"message":"Job #5.1 - 100.0% Covered","url":"https://coveralls.io/jobs/5722"}'
        )
        response = api.post(
            url=Arguments.coveralls_url,
            repo_token=Arguments.repo_token,
            service_job_id=Arguments.service_job_id,
            service_name=Arguments.service_name,
            git=GIT_EXP,
            source_files=SOURCE_FILES
        )
        self.assertEqual(response.json(), {u'url': u'https://coveralls.io/jobs/5722', u'message': u'Job #5.1 - 100.0% Covered'})

    def test_build_file_eur(self):
        json_file = api.build_file(
            repo_token=Arguments.repo_token,
            service_job_id=Arguments.service_job_id,
            service_name=Arguments.service_name,
            git=GIT_EXP,
            source_files=SOURCE_FILES
        )
        self.assertEqual(
            json.loads(json_file.read())['source_files'][1]['source'],
            u'# coding=utf-8\nEUR = "€"\n\n\ndef amount(tariff, currency=EUR):\n    return \'{0} {1:.2f}\'.format(currency, float(tariff))'
        )


class NotAFileTestCase(TestCase):
    def setUp(self):
        coverage = coveralls(data_file=Arguments.data_file, config_file=Arguments.config_file)
        coverage.load()
        self.reporter = CoverallsReporter(coverage, coverage.config)
        self.reporter.find_code_units(None)
        self.reporter.code_units.append(CodeUnit('NotAFile.py', FileLocator()))

    def test_report_raises(self):
        self.assertRaises(IOError, self.reporter.report, Arguments.base_dir)

    def test_report_continue(self):
        self.assertEqual(self.reporter.report(Arguments.base_dir, ignore_errors=True), SOURCE_FILES)
