%define _rpmfilename %%{ARCH}/%%{NAME}-%%{VERSION}_%%{ARCH}.rpm

Name:           traefik
Version:        1.4.1
Release:        1%{dist}
Summary:        Træfɪk, a modern reverse proxy
ExclusiveArch:  x86_64

Group:          System Environment/Daemons
License:        MIT
URL:            https://traefik.io/
Source0:        https://github.com/containous/traefik/releases/download/v%{version}/traefik_linux-amd64
Source1:        traefik.service
Source2:        https://raw.githubusercontent.com/containous/traefik/master/traefik.sample.toml

BuildRequires:  systemd-units

Requires(pre):  shadow-utils
Requires:       systemd glibc

%description
Træfɪk is a modern HTTP reverse proxy and load balancer made to deploy 
microservices with ease. It supports several backends (Docker, Swarm, 
Mesos/Marathon, Consul, Etcd, Zookeeper, BoltDB, Rest API, file...) to manage 
its configuration automatically and dynamically.

%prep

%build

%install
install -D %{SOURCE0} %{buildroot}/%{_bindir}/traefik
install -D %{SOURCE1} %{buildroot}/%{_unitdir}/%{name}.service
install -D %{SOURCE2} %{buildroot}/%{_sysconfdir}/%{name}/traefik.toml

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
    -c "%{name} user" %{name}
exit 0

%post
/sbin/setcap 'cap_net_bind_service=+ep' /bin/traefik
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
getent passwd %{name} >/dev/null && userdel %{name}
getent group %{name} >/dev/null && groupdel %{name}
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(755, root, root) %{_bindir}/traefik
%attr(644, root, root) %{_unitdir}/%{name}.service
%config(noreplace) %attr(640, root, %{name}) %{_sysconfdir}/%{name}/traefik.toml


%changelog
* Mon May 15 2017 AZME Mickael  > 1.0.0
- Intial version: v1.0.0
- Change traefik version and rename rpm filename
- Add dependency with local filesystem
