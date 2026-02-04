import pytest


@pytest.mark.parametrize(
    "name",
    [
        ("python3-pip"),
    ],
)
def test_dependencies_are_installed(host, name):
    package = host.package(name)
    assert package.is_installed


@pytest.mark.parametrize(
    "name",
    [
        ("elasticsearch-curator"),
    ],
)
def test_curator_pip_package_is_installed(host, name):
    packages = host.pip.get_packages(pip_path="pip3")
    assert name in packages


def test_curator_command_is_available(host):
    cmd = host.run("curator --version")
    assert cmd.rc == 0


@pytest.mark.parametrize(
    "path,user,group,mode",
    [
        ("/etc/curator", "root", "root", 0o755),
    ],
)
def test_curator_config_directory_exists(host, path, user, group, mode):
    directory = host.file(path)
    assert directory.exists
    assert directory.is_directory
    assert directory.user == user
    assert directory.group == group
    assert directory.mode == mode


@pytest.mark.parametrize(
    "path,user,group,mode",
    [
        ("/etc/curator/curator.yml", "root", "root", 0o640),
        ("/etc/curator/actionfile.yml", "root", "root", 0o644),
    ],
)
def test_curator_config_files_exist(host, path, user, group, mode):
    config = host.file(path)
    assert config.exists
    assert config.is_file
    assert config.user == user
    assert config.group == group
    assert config.mode == mode


def test_curator_config_contains_hosts(host):
    config = host.file("/etc/curator/curator.yml")
    assert config.contains("elasticsearch-test:9200")


def test_curator_actionfile_is_valid_yaml(host):
    config = host.file("/etc/curator/actionfile.yml")
    assert config.contains("actions:")
    assert config.contains("delete_indices")


@pytest.mark.parametrize(
    "unit",
    [
        ("curator.service"),
        ("curator.timer"),
    ],
)
def test_systemd_units_exist(host, unit):
    systemd_file = host.file(f"/etc/systemd/system/{unit}")
    assert systemd_file.exists
    assert systemd_file.is_file
    assert systemd_file.user == "root"
    assert systemd_file.group == "root"
    assert systemd_file.mode == 0o644


def test_curator_service_is_enabled(host):
    service = host.service("curator.service")
    assert service.is_enabled


def test_curator_timer_is_enabled(host):
    timer = host.service("curator.timer")
    assert timer.is_enabled
    assert timer.is_running
