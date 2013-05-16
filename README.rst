EnvAssert
===================

Test your servers environments by using fabric.

Requirements
----------------

- python 2.6 or later
- fabric

How to Use
------------------

0. install

   ::

     % pip install envassert

1. write fabfile.py.

   ::

      from fabric.api import env, task
      from envassert import file, process, package, user, group, port, cron, detect

      env.use_ssh_config = True

      @task
      def check():
          env.platform_family = detect.detect()

          assert file.exists("/etc/hosts")
          assert file.is_file("/etc/hosts")
          assert file.is_dir("/tmp/")
          assert file.dir_exists("/tmp/")
          assert file.has_line("/etc/passwd", "sshd")
          assert file.owner_is("/bin/sh", "root")
          assert file.group_is("/bin/sh", "root")
          assert file.mode_is("/bin/sh", "777")

          if env.platform_family == "freebsd":
              assert file.is_link("/compat")
          else:
              assert file.is_link("/usr/tmp")

          assert package.installed("wget.x86_64")

          assert user.exists("sshd")
          assert user.is_belonging_group("shirou", "users")
          assert group.is_exists("wheel")

          assert port.is_listening(22)
          assert process.is_up("http") is False
          assert service.is_enabled("httpd")

          assert cron.has_entry('shirou', 'python')

2. run fab

   ::

     % fab -H somehost check
     [somehost] Executing task 'check'

     Done.
     Disconnecting from root@192.168.22.98... done.

   You can use any other fabric arguments like hosts or parallel.

Detecting OS
-----------------------

The `detect.detect()` function can detect target OS and
distribution. Setting this variable to `env.platform_family`,
functions can dispatch according to that value.

This function is a minimal port of ohai.

Currently, these platform can be detected. (but not tested yet)

- rhel (redhat, centos, oracle, scientific, enterpriseenterprise, amazon)
- debian (debian, ubuntu, linuxmint, raspbian)
- fedora
- suse
- gentoo
- arch
- freebsd
- netbsd
- openbsd
- darwin

However, every functions are not implemented for these all
platform. Pull Requests are welcome.


The giants on whose shoulders this works stands
----------------------------------------------------

- serverspec : http://serverspec.org/
- cuisine : https://github.com/sebastien/cuisine
- ohai (for detecting platforms) : http://docs.opscode.com/chef/ohai.html

License
------------------

MIT License

FYI

- cuisine: BSD
- serverspec: MIT
- ohai: Apache 2




