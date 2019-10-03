# contains the "scoped" fixtures
# no need to import this module in the test files as they automatically gain access to it
# see https://docs.pytest.org/en/latest/fixture.html

import pytest
import os
from .utiltest import run_script


# scope should be module
@pytest.fixture(scope='module')
def start_solr():
    from subprocess import call
    # call(['~/solr-7.6.0/bin/solr', 'start', '-e', 'cloud', '-noprompt'])


@pytest.fixture(scope='module')
def stop_solr():
    from subprocess import call
    # call(['~/solr-7.6.0/bin/solr', 'stop', 'all'])


@pytest.fixture(scope='session')
def upload_golden_copy_test_config():
    solr_home = os.environ["SOLR_HOME"]
    print("################## Running session fixture, SOLR_HOME=%s ##################" % solr_home)
    args = [
        "-z localhost:2181,localhost:2182,localhost:2183/my_solr_conf",
        "-cmd upconfig",
        "-confname GoldenCopyConfig",
        "-confdir /home/pjmd/python_workspace/PychramProjects/scrapy_nhs/nhs/resources/solr/configsets/GoldenCopyConfig/conf"
    ]
    run_script("".join([solr_home, "/server/scripts/cloud-scripts/zkcli.sh"]), args)

