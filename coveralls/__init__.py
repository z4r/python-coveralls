__author__ = 'Andrea De Marco <24erre@gmail.com>'
__version__ = '1.0.1'
__classifiers__ = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Software Development :: Libraries',
]
__copyright__ = "2013, %s " % __author__
__license__ = """
   Copyright %s.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either expressed or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
""" % __copyright__

__docformat__ = 'restructuredtext en'

__doc__ = """
:abstract: Python interface to coveralls.io API
:version: %s
:author: %s
:contact: http://z4r.github.com/
:date: 2012-02-08
:copyright: %s
""" % (__version__, __author__, __license__)


def parse_args():
    import os
    import yaml
    import argparse
    parser = argparse.ArgumentParser(prog='coveralls')
    parser.add_argument('--coveralls_url', '-u', help='coveralls.io api url', default='https://coveralls.io/api/v1/jobs')
    parser.add_argument('--base_dir', '-b', help='project root directory', default='.')
    parser.add_argument('--data_file', '-d', help='coverage file name', default='.coverage')
    parser.add_argument('--config_file', '-c', help='coverage config file name', default='.coveragerc')
    parser.add_argument('--coveralls_yaml', '-y', help='coveralls yaml file name', default='.coveralls.yml')
    args = parser.parse_args()
    args.base_dir = os.path.abspath(args.base_dir)
    args.data_file = os.path.join(args.base_dir, args.data_file)
    args.config_file = os.path.join(args.base_dir, args.config_file)
    args.coveralls_yaml = os.path.join(args.base_dir, args.coveralls_yaml)
    yml = {}
    try:
        with open(args.coveralls_yaml, 'r') as fp:
            yml = yaml.load(fp)
    except:
        pass
    yml = yml or {}
    args.repo_token = yml.get('repo_token', '')
    args.service_name = yml.get('service_name', 'travis-ci')
    args.service_job_id = os.environ.get('TRAVIS_JOB_ID', '')
    return args


def wear(args=None):
    from coveralls.control import coveralls
    from coveralls.repository import gitrepo
    from coveralls.api import post
    args = args or parse_args()
    coverage = coveralls(data_file=args.data_file, config_file=args.config_file)
    coverage.load()
    response = post(
        url=args.coveralls_url,
        repo_token=args.repo_token,
        service_job_id=args.service_job_id,
        service_name=args.service_name,
        git=gitrepo(args.base_dir),
        source_files=coverage.coveralls(args.base_dir),
    )
    print response.text
    return response
