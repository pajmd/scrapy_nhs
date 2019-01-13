# contains the "scoped" fixtures
# no need to import this module in the test files as they automatically gain access to it
# see https://docs.pytest.org/en/latest/fixture.html

import pytest


# scope should be module
@pytest.fixture(scope='module')
def start_solr():
    from subprocess import call
    call(['~/solr-7.6.0/bin/solr', 'start', '-e', 'cloud', '-noprompt'])


@pytest.fixture(scope='module')
def stop_solr():
    from subprocess import call
    call(['~/solr-7.6.0/bin/solr', 'stop', 'all'])
