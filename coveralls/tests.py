from unittest import TestCase
from httpretty import HTTPretty, httprettified
from coveralls import coveralls, gitrepo, post, wear
import os


class Arguments(object):
    coveralls_url = 'https://coveralls.io/api/v1/jobs'
    repo_token = 'abcdef1234569abdcef'
    service_job_id = '4699301'
    service_name = 'travi-ci',
    base_dir = os.path.abspath('python-coveralls-example')
    data_file = os.path.join(base_dir, '.coverage')
    config_file = os.path.join(base_dir, '.coveragerc')


GIT_EXP = {
    'head': {
        'committer_email': '24erre@gmail.com',
        'author_email': '24erre@gmail.com',
        'author_name': u'z4r',
        'message': u'1st commit with a test message',
        'committer_name': u'z4r',
        'id': '17b8119796516195527dcb4f454a2ebd41d60244'
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
        'source': "def exsum(a, b):\n    # A comment of a exsum\n    return a + b\n\n\ndef exdiff(a, b):\n    return a - b\n\n\nif __name__ == '__main__':\n    print exsum(3,4)\n    print exdiff(2,2)",
        'name': 'example/exmath.py',
        'coverage': [1, None, 1, None, None, 1, 0, None, None, None, None, None]
    }
]


class CoverallsTestCase(TestCase):
    @httprettified
    def test_wear(self):
        HTTPretty.register_uri(
            'POST',
            'https://coveralls.io/api/v1/jobs',
            body='{"message":"Job #5.1 - 100.0% Covered","url":"https://coveralls.io/jobs/5722"}'
        )
        response = wear(Arguments)
        self.assertEqual(response.json(), {u'url': u'https://coveralls.io/jobs/5722', u'message': u'Job #5.1 - 100.0% Covered'})

    def test_gitrepo(self):
        git = gitrepo(Arguments.base_dir)
        self.assertEqual(git, GIT_EXP)

    def test_coveralls(self):
        coverage = coveralls(data_file=Arguments.data_file, config_file=Arguments.config_file)
        coverage.load()
        self.assertEqual(coverage.coveralls(Arguments.base_dir), SOURCE_FILES)

    @httprettified
    def test_api(self):
        HTTPretty.register_uri(
            'POST',
            'https://coveralls.io/api/v1/jobs',
            body='{"message":"Job #5.1 - 100.0% Covered","url":"https://coveralls.io/jobs/5722"}'
        )
        response = post(
            url=Arguments.coveralls_url,
            repo_token=Arguments.repo_token,
            service_job_id=Arguments.service_job_id,
            service_name=Arguments.service_name,
            git=GIT_EXP,
            source_files=SOURCE_FILES
        )
        self.assertEqual(response.json(), {u'url': u'https://coveralls.io/jobs/5722', u'message': u'Job #5.1 - 100.0% Covered'})
