Name:           ec2sys-autotune
Version:        1.0.0
Release:        1%{?dist}
Summary:        AWS EC2 instance autotuning

Group:          Applications/Engineering
License:        GPLv2
URL:            https://github.com/awslabs/autotune
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
Requires(pre):  systemd
Requires:       kernel-tools irqbalance procps-ng
Requires:       util-linux ec2-utils grep coreutils
BuildRequires:  python2 python2-devel

%description
An AWS EC2 agent that tunes guest instances automatically based on their instance type

%prep
%setup -q -n %{name}-%{version}

%build
%py2_build

%install
%py2_install

%files
%defattr(-,root,root)
%doc README.md
%license LICENSE
%{_unitdir}/autotune.service
%{_bindir}/ec2sys_autotune_start
%{_bindir}/ec2sys_autotune_stop
%{_bindir}/autotune
%config(noreplace) %{_sysconfdir}/ec2sys-autotune.cfg
%config(noreplace) %{_sysconfdir}/%{name}.d/user.ini
%dir "%{_var}/lib/%{name}"
%{python2_sitelib}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post autotune.service

%preun
%systemd_preun autotune.service

%postun
%systemd_postun_with_restart autotune.service

%changelog
* Mon Feb 4 2019 Vallish Vaidyeshwara <vallish@amazon.com> - 1.0.0
- Initial build
