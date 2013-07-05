====================================
Python interface to coveralls.io API
====================================

.. image:: https://api.travis-ci.org/z4r/python-coveralls.png?branch=master
    :target: http://travis-ci.org/z4r/python-coveralls
.. image:: https://coveralls.io/repos/z4r/python-coveralls/badge.png?branch=master
    :target: https://coveralls.io/r/z4r/python-coveralls
.. image:: https://pypip.in/v/python-coveralls/badge.png
   :target: https://crate.io/packages/python-coveralls/
.. image:: https://pypip.in/d/python-coveralls/badge.png
   :target: https://crate.io/packages/python-coveralls/

This package provides a module to interface with the https://coveralls.io API.

INSTALLING THE PKG
==================
Using pip::

    $ pip install python-coveralls

...Or simply add it to your requirements.


CONFIGURATION
=============
If you're not using Travis, Coveralls for Python uses a ``.coveralls.yml`` file at the root level of your repository to configure options.
The only required option is ``repo_token`` (found on your repository's page on Coveralls) to specify which project on Coveralls your project maps to.
Another important option is is ``service_name`` which allows you to specify where Coveralls should look to find additional information about your builds. This can be any string, but using travis-ci or travis-pro will allow Coveralls to fetch branch data, comment on pull requests, and more.
A ``.coveralls.yml`` file configured for Travis Pro::

    repo_token: abcdef1234569abdcef
    service_name: travis-pro

if you don't want the ``repo_token`` under source control, set it in your ``coveralls`` command::

    COVERALLS_REPO_TOKEN=abcdef1234569abdcef coveralls

TRAVIS.YML
==========
Create a ``.coverage`` file and you can use ``coverage``, ``py-cov``, or ``nose``.
Then you can add in the _after_success_ step::

    coveralls

It should look like something like::

    language: python
    python:
      - "2.6"
      - "2.7"
    install:
      - pip install -e . --use-mirrors
    before_script:
      - pip install -r test_requirements.txt --use-mirrors
      - git clone https://github.com/z4r/python-coveralls-example.git
      - cd python-coveralls-example
      - git checkout -qf 17b8119796516195527dcb4f454a2ebd41d60244
      - py.test example/tests.py --cov=example
      - cd -
    script:
      - py.test coveralls/tests.py --doctest-modules --pep8 coveralls -v --cov coveralls --cov-report term-missing
    after_success:
      - coveralls

