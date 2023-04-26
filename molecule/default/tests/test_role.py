import pytest

import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize(
    "name",
    [
        ("elasticsearch-curator"),
    ],
)
def test_curator_is_installed(host, name):
    packages = host.pip.get_packages(pip_path="pip3")
    assert name in packages


@pytest.mark.parametrize(
    "username,groupname,path",
    [
        ("root", "root", "/etc/curator/curator.yml"),
    ],
)
def test_curator_config_file(host, username, groupname, path):
    curator_config = host.file(path)
    assert curator_config.exists
    assert curator_config.is_file
    assert curator_config.user == username
    assert curator_config.group == groupname


@pytest.mark.parametrize(
    "username,groupname,path",
    [
        ("root", "adm", "/var/log/curator"),
    ],
)
def test_curator_log_directory(host, username, groupname, path):
    curator_config = host.file(path)
    assert curator_config.exists
    assert curator_config.is_directory
    assert curator_config.user == username
    assert curator_config.group == groupname


@pytest.mark.parametrize(
    "username,groupname,path",
    [
        ("root", "root", "/etc/curator/actionfile.yml"),
    ],
)
def test_curator_action_file(host, username, groupname, path):
    curator_action = host.file(path)
    assert curator_action.exists
    assert curator_action.is_file
    assert curator_action.user == username
    assert curator_action.group == groupname
