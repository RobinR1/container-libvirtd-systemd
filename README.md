# Systemd service file to run libvirtd container via systemd and podman

* `/etc/sysconfig/container-libvirtd` contains generic settings
* `/etc/libvirtd-secrets/ROOT_PASSWORD` is a file for setting the root password of the container.
  It should not be readable by anyone but root user. This location can be altered via `SECRETS_DIR`
  in the `/etc/sysconfig/container-libvirtd` file.