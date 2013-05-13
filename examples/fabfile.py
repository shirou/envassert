import os, sys
sys.path.append(os.path.abspath(os.path.join('..', 'src')))

from fabric.api import env, task
from envassert import file, process, package, user, group, port, cron, service, detect

env.use_ssh_config = True

@task
def check():
    env.platform_family = detect.detect()
    # file
    assert file.is_exists("/etc/hosts")
    assert file.is_file("/etc/hosts")
    assert file.is_dir("/tmp/")
    assert file.dir_exists("/tmp/")
    assert file.has_line("/etc/passwd", "sshd")
    assert file.owner_is("/bin/sh", "root")
    if env.platform_family == "freebsd":
        assert file.is_link("/compat")
        assert file.group_is("/bin/sh", "wheel")
        assert file.mode_is("/bin/sh", "555")
    else:
        assert file.is_link("/usr/tmp")
        assert file.group_is("/bin/sh", "root")
        assert file.mode_is("/bin/sh", "777")

    assert package.installed("wget.x86_64")

    assert user.is_exists("sshd")
    assert user.is_belonging_group("worker", "users")

    assert group.is_exists("wheel")

    assert port.is_listening(22)
    assert cron.has_entry('shirou', 'python')

    if env.platform_family == "freebsd":
        assert service.is_enabled("apache22")
        assert process.is_up("httpd")
    else:
        assert service.is_enabled("http")
        assert process.is_up("http") is False
