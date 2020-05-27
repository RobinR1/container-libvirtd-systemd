%define libvirtd
%define libvirtd.service

%if %{undefined service_del_postun_without_restart}
%define service_del_postun_without_restart() \
DISABLE_RESTART_ON_UPDATE=1 \
%service_del_postun %{?*}
%endif

Name:           container-libvirtd
Version:        0.1
Release:        0
Summary:        Systemd service file and config file for RobinR1's libvirtd container
License:        MIT
URL:            https://github.com/RobinR1/containers-libvirtd
Source:         containers-libvirtd-%{version}.tar.xz
Source1:        container-libvirtd.rpmlintrc
Requires(post): %fillup_prereq
BuildArch:      noarch

%description
This package contains the configuration file and systemd unit
to run RobinR1's libvirtd container via podman managed by systemd.

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_fillupdir}
mkdir -p %{buildroot}/srv/libvirtd
install -m 644 sysconfig.container-libvirtd %{buildroot}%{_fillupdir}/
install -m 644 container-libvirtd.service %{buildroot}%{_unitdir}/
# create symlink for rccontainer-*
ln -s /sbin/service %{buildroot}%{_sbindir}/rccontainer-libvirtd
mkdir -p %{buildroot}%{_sysconfdir}/libvirtd-secrets
touch %{buildroot}%{_sysconfdir}/mariadb-secrets/ROOT_PASSWORD

%pre
%service_add_pre libvirtd.service

%post
%{fillup_only -n container-libvirtd}
%service_add_post libvirtd.service

%preun
%service_del_preun libvirtd.service

%postun
# Avoid useless container restarts on update of this package
%service_del_postun_without_restart libvirtd.service

%files
%license LICENSE
%doc README.md
%{_unitdir}/container-libvirtd.service
%{_fillupdir}/sysconfig.container-libvirtd
%{_sbindir}/rccontainer-libvirtd
%ghost %dir /srv/libvirtd
%dir %attr(0700,root,root) %{_sysconfdir}/libvirtd-secrets
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/libvirtd-secrets/ROOT_PASSWORD

%changelog
