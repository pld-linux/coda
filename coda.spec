Summary:	Coda distributed filesystem
Summary(pl):	Rozproszony system plików Coda
Name:		coda
Version:	5.3.10
Release:	1
Copyright:	CMU
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	%{name}-%{version}.tgz
Patch0:		%{name}-ugly-common.patch
Requires:	bc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Source package for the Coda filesystem. Three packages are provided by
this rpm: the client and server and the backup components. Separately
you must install a kernel module, or have a Coda enabled kernel, and
you should get the Coda documentation package. BEWARE: CVS VERSION

%description -l pl
Pakiet ¼ród³owy systemu plików Coda. Rpm zawiera trzy pakiety:
klienta, serwer oraz komponenty do backupu. Nale¿y oddzielnie
zainstalowaæ modu³ do j±dra (lub mieæ j±dro z obs³ug± Cody), nale¿y
rownie¿ zaopatrzyæ siê w pakiet z dokumentacj± Cody. UWAGA: WERSJA CVS

%package client
Summary:	Coda client
Summary(pl):	Klient Cody
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Prereq:		/sbin/chkconfig

%description client
This package contains the main client program, the cachemanager Venus.
Also included are the binaries for the cfs, utilities for logging, ACL
manipulation etc, the hoarding tools for use with laptops and repair
tools for fixing conflicts. Finally there is the cmon and codacon
console utilities to monitor Coda's activities. You need a Coda
kernel-module for your kernel version, or Coda in your kernel, to have
a complete coda client. Make sure to select the correct C library
version. BEWARE: CVS VERSION

%package server
Summary:	Coda server
Summary(pl):	Serwer Cody
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Prereq:		/sbin/chkconfig

%description server
This package contains the fileserver codasrv for the coda filesystem,
as well as the volume utilities. For highest performance you will need
a modified kernel with inode system calls. BEWARE: CVS VERSION

%package backup
Summary:	Coda backup coordinator
Summary(pl):	Program do zarz±dzania backupem Cody
Prereq:		/sbin/chkconfig

%description backup
This package contains the backup software for the coda filesystem, as
well as the volume utilities. BEWARE: CVS VERSION

%prep
%setup -q
%patch0 -p1

%build
touch ChangeLog
autoheader
aclocal
autoconf
#%%configure
CFLAGS="%{rpmcflags}" CXXFLAGS="%{rpmcflags}" LDFLAGS="%{rpmldflags}" \
./configure %{_target_platform} \
	--prefix=%{_prefix}
%{__make} OPTFLAGS="%{rpmcflags}"


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_prefix}/coda/venus.cache \
	$RPM_BUILD_ROOT%{_prefix}/coda%{_sysconfdir} \
	$RPM_BUILD_ROOT/coda $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} prefix=$RPM_BUILD_ROOT%{_prefix} client-install
%{__make} prefix=$RPM_BUILD_ROOT%{_prefix} server-install

touch $RPM_BUILD_ROOT%{_prefix}/coda/venus.cache/INIT
#mknod $RPM_BUILD_ROOT/dev/cfs0 c 67 0
touch $RPM_BUILD_ROOT/coda/NOT_REALLY_CODA

%clean
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
rm -rf $RPM_BUILD_ROOT

%pre client
grep "^coda" /proc/mounts > /dev/null 2>&1
if [ $? = 0 ]; then
	echo "*** Coda is mounted: cannot install ***"
	exit 1
else
	exit 0
fi

%preun client
grep "^coda" /proc/mounts > /dev/null 2>&1
if [ $? = 0 ]; then
	echo "*** Coda is mounted: cannot uninstall ***"
	exit 1
else
	exit 0
fi
	
%post client
if [ -e /usr/coda/etc/vstab ]; then 
	touch /usr/coda/venus.cache/INIT
else
	%{_sbindir}/venus-setup testserver.coda.cs.cmu.edu 40000
fi
NAME=venus.init; %chkconfig_add

%preun client
NAME=venus.init; %chkconfig_del

%post server
NAME=update.init; %chkconfig_add
NAME=auth2.init; DESC=auth2.init; %chkconfig_add
NAME=codasrv.init; DESC=codasrv.init; %chkconfig_add

%postun server
NAME=update.init; %chkconfig_del
NAME=auth2.init; %chkconfig_del
NAME=codasrv.init; %chkconfig_del

%files client
%defattr(644,root,root,755)
%dir %{_prefix}/coda
%dir %{_prefix}/coda%{_sysconfdir}
%dir %{_prefix}/coda/venus.cache
%verify() %{_prefix}/coda/venus.cache/INIT
/etc/rc.d/init.d/venus.init
%dir /coda
%verify() /coda/NOT_REALLY_CODA
%attr(755,root,root) %{_sbindir}/venus-setup
%attr(755,root,root) %{_sbindir}/vutil
%attr(755,root,root) %{_sbindir}/venus
%attr(755,root,root) %{_sbindir}/au
%attr(755,root,root) %{_bindir}/clog
%attr(755,root,root) %{_bindir}/cpasswd
%attr(755,root,root) %{_bindir}/ctokens
%attr(755,root,root) %{_bindir}/cunlog
%attr(755,root,root) %{_bindir}/repair
%attr(755,root,root) %{_bindir}/cmon
%attr(755,root,root) %{_bindir}/codacon
%attr(755,root,root) %{_bindir}/cfs
%attr(755,root,root) %{_bindir}/hoard
%attr(755,root,root) %{_bindir}/spy
%attr(755,root,root) %{_bindir}/replay
%attr(755,root,root) %{_bindir}/parser
%attr(755,root,root) %{_bindir}/filerepair
%attr(755,root,root) %{_bindir}/removeinc
%attr(755,root,root) %{_bindir}/xfrepair
%attr(755,root,root) %{_bindir}/xaskuser
%attr(755,root,root) %{_sbindir}/volmunge

%files server	
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/startserver
%attr(755,root,root) %{_sbindir}/partial-reinit.sh
%attr(755,root,root) %{_sbindir}/createvol_rep
%attr(755,root,root) %{_sbindir}/purgevol
%attr(755,root,root) %{_sbindir}/purgevol_rep
%attr(755,root,root) %{_sbindir}/bldvldb.sh
%attr(755,root,root) %{_sbindir}/vice-setup
%attr(755,root,root) %{_sbindir}/vice-setup-rvm
%attr(755,root,root) %{_sbindir}/vice-setup-srvdir
%attr(755,root,root) %{_sbindir}/vice-setup-user
%attr(755,root,root) %{_sbindir}/vice-setup-scm
%attr(755,root,root) %{_sbindir}/vice-killvolumes
%attr(755,root,root) %{_sbindir}/auth2
%attr(755,root,root) %{_sbindir}/initpw
%attr(755,root,root) %{_sbindir}/volutil
%attr(755,root,root) %{_sbindir}/rpc2portmap
%attr(755,root,root) %{_sbindir}/inoder
%attr(755,root,root) %{_sbindir}/parserecdump
%attr(755,root,root) %{_sbindir}/codasrv
%attr(755,root,root) %{_sbindir}/printvrdb
%attr(755,root,root) %{_sbindir}/updatesrv
%attr(755,root,root) %{_sbindir}/updateclnt
%attr(755,root,root) %{_sbindir}/updatefetch
%attr(755,root,root) %{_bindir}/norton
%attr(755,root,root) %{_bindir}/norton-reinit
%attr(755,root,root) %{_bindir}/reinit
/etc/rc.d/init.d/codasrv.init
/etc/rc.d/init.d/auth2.init
/etc/rc.d/init.d/update.init

%files backup	
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/backup.sh
%attr(755,root,root) %{_sbindir}/tape.pl
%attr(755,root,root) %{_sbindir}/auth2
%attr(755,root,root) %{_sbindir}/volutil
%attr(755,root,root) %{_sbindir}/backup
%attr(755,root,root) %{_sbindir}/readdump
%attr(755,root,root) %{_sbindir}/merge
%attr(755,root,root) %{_sbindir}/updatesrv
%attr(755,root,root) %{_sbindir}/updateclnt
%attr(755,root,root) %{_sbindir}/updatefetch
