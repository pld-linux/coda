# TODO:
#   - FHS (at least /usr/coda, /var/coda - assuming that /coda is special)
#   - separate some programs to coda-common package
#
Summary:	Coda distributed filesystem
Summary(pl.UTF-8):	Rozproszony system plików Coda
Name:		coda
Version:	6.9.5
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.coda.cs.cmu.edu/pub/coda/src/%{name}-%{version}.tar.gz
# Source0-md5:	23e3cbed0eea41aa9a9dea45df31938b
Source1:	%{name}.venus.init
Source2:	%{name}.auth2.init
Source3:	%{name}.codasrv.init
Source4:	%{name}.update.init
Patch0:		%{name}-ugly-common.patch
Patch1:		%{name}-FHS.patch
Patch3:		%{name}-gcc-334-2.patch
URL:		http://www.coda.cs.cmu.edu/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	db-devel
BuildRequires:	e2fsprogs-devel >= 1.34
BuildRequires:	flex
BuildRequires:	libstdc++-devel
BuildRequires:	lwp-devel >= 2.1
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	rpc2-devel >= 2.0
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	rvm-devel
BuildRequires:	rvm-tools
Requires:	bc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Source package for the Coda filesystem. Three packages are provided by
this rpm: the client and server and the backup components. Separately
you must install a kernel module, or have a Coda enabled kernel, and
you should get the Coda documentation package.

%description -l pl.UTF-8
Pakiet źródłowy systemu plików Coda. Rpm zawiera trzy pakiety:
klienta, serwer oraz komponenty do backupu. Należy oddzielnie
zainstalować moduł do jądra (lub mieć jądro z obsługą Cody), należy
również zaopatrzyć się w pakiet z dokumentacją Cody.

%package common
Summary:	Coda filesystem common programs
Summary(pl.UTF-8):	Wspólne programy dla klienta i serwera systemu plików Coda
Group:		Networking/Daemons

%description common
This package contains programs used by server and client.

%description common -l pl.UTF-8
Ten pakiet zawiera programy używane przez klienta i serwer systemu
plików Coda.

%package client
Summary:	Coda client
Summary(pl.UTF-8):	Klient Cody
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common = %{version}-%{release}
Requires:	rc-scripts

%description client
This package contains the main client program, the cachemanager Venus.
Also included are the binaries for the cfs, utilities for logging, ACL
manipulation etc, the hoarding tools for use with laptops and repair
tools for fixing conflicts. Finally there is the cmon and codacon
console utilities to monitor Coda's activities. You need a Coda
kernel-module for your kernel version, or Coda in your kernel, to have
a complete coda client. Make sure to select the correct C library
version.

%description client -l pl.UTF-8
Ten pakiet zawiera głównego klienta, zarządcę cache Venus. Dołączone
są także binaria cfs, narzędzia do logowania, zarządzania ACL-ami
itp., narzędzia do używania z laptopami i narzędzia do naprawiania
konfliktów. Są także narzędzia cmon i codacon do monitorowania
aktywności Cody. Pakiet wymaga Cody w kernelu lub module kernela.

%package server
Summary:	Coda server
Summary(pl.UTF-8):	Serwer Cody
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common = %{version}-%{release}
Requires:	rc-scripts
Requires:	rvm-tools

%description server
This package contains the fileserver codasrv for the coda filesystem,
as well as the volume utilities. For highest performance you will need
a modified kernel with inode system calls.

%description server -l pl.UTF-8
Ten pakiet zawiera codasrv - serwer systemu plików Coda, oraz
narzędzia do wolumenów. Aby osiągnąć lepszą wydajność, potrzebny jest
zmodyfikowany kernel z wywołaniami dotyczącymi inodów.

%package backup
Summary:	Coda backup coordinator
Summary(pl.UTF-8):	Program do zarządzania backupem Cody
Group:		Networking

%description backup
This package contains the backup software for the coda filesystem, as
well as the volume utilities.

%description backup -l pl.UTF-8
Ten pakiet zawiera oprogramowanie do backupu systemu plików Coda oraz
narzędzia do wolumenów.

%prep
%setup -q
%patch -P0 -p1
#%%patch1 -p1
%patch -P3 -p1

%build
touch ChangeLog
#%{__autoheader}
#%{__aclocal}
cp -f /usr/share/automake/config.sub configs
%{__autoconf}
%configure \
	--enable-crypto
%{__make} \
	OPTFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_localstatedir}/%{name}/venus.cache \
	$RPM_BUILD_ROOT%{_prefix}/coda%{_sysconfdir} \
	$RPM_BUILD_ROOT/coda $RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT/garbage

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	exec_prefix=$RPM_BUILD_ROOT%{_prefix} \
	libdir=$RPM_BUILD_ROOT%{_libdir} \
	libexecdir=$RPM_BUILD_ROOT%{_libexecdir} \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	sbindir=$RPM_BUILD_ROOT%{_sbindir} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	sysconfdir=$RPM_BUILD_ROOT%{_sysconfdir}/%{name} \
	initsuffix=$RPM_BUILD_ROOT/garbage

touch $RPM_BUILD_ROOT%{_localstatedir}/%{name}/venus.cache/INIT
#mknod $RPM_BUILD_ROOT/dev/cfs0 c 67 0
touch $RPM_BUILD_ROOT/coda/NOT_REALLY_CODA

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/venus
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/auth2
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/codasrv
install %{SOURCE4} $RPM_BUILD_ROOT/etc/rc.d/init.d/update

%{__perl} -pi -e "s!usr/coda!var/lib/coda!" $RPM_BUILD_ROOT%{_sysconfdir}/coda/*

install -d $RPM_BUILD_ROOT/var/lib/coda/vice/{auth2,db,misc,spool,srv,vol}

%clean
rm -rf $RPM_BUILD_ROOT

%pre client
grep "^coda" /proc/mounts > /dev/null 2>&1
if [ $? = 0 ]; then
	echo "*** Coda is mounted: cannot install ***"
	exit 1
else
	exit 0
fi

%post client
if [ -e %{_sysconfdir}/coda/vstab ]; then
	touch /var/lib/coda/venus.cache/INIT
else
	%{_sbindir}/venus-setup testserver.coda.cs.cmu.edu 40000
fi
/sbin/chkconfig --add venus
%service venus restart

%preun client
grep "^coda" /proc/mounts > /dev/null 2>&1
if [ $? = 0 ]; then
	echo "*** Coda is mounted: cannot uninstall ***"
	exit 1
else
	exit 0
fi
if [ "$1" = "0" ]; then
	%service venus stop
	/sbin/chkconfig --del venus
fi

%post server
/sbin/chkconfig --add auth2
%service auth2 restart

/sbin/chkconfig --add update
%service update restart

/sbin/chkconfig --add codasrv
%service codasrv restart

%preun server
if [ "$1" = "0" ]; then
	%service update stop
	/sbin/chkconfig --del update

	%service auth2 stop
	/sbin/chkconfig --del auth2

	%service codasrv stop
	/sbin/chkconfig --del codasrv
fi

%files common
%defattr(644,root,root,755)
%dir %{_sysconfdir}/coda
%attr(755,root,root) %{_sbindir}/codaconfedit
#%attr(755,root,root) %{_sbindir}/coda-setup-ports
%attr(755,root,root) %{_bindir}/rpc2ping

%files client
%defattr(644,root,root,755)
%dir %{_prefix}/coda
%dir %{_prefix}/coda%{_sysconfdir}
%dir %{_localstatedir}/%{name}/venus.cache
%verify() %{_localstatedir}/%{name}/venus.cache/INIT
%attr(754,root,root) /etc/rc.d/init.d/venus
%dir /coda
%verify() /coda/NOT_REALLY_CODA
%{_sysconfdir}/coda/venus.conf.ex
#%{_sysconfdir}/coda/sidekick.intr.ex
%config %{_sysconfdir}/coda/realms
%attr(755,root,root) %{_sbindir}/codastart
#%attr(755,root,root) %{_sbindir}/pwdtopdbtool.py
%attr(755,root,root) %{_sbindir}/venus-setup
%attr(755,root,root) %{_sbindir}/vutil
%attr(755,root,root) %{_sbindir}/venus
%attr(755,root,root) %{_bindir}/au
%attr(755,root,root) %{_bindir}/clog
%attr(755,root,root) %{_bindir}/coda_replay
%attr(755,root,root) %{_bindir}/cpasswd
%attr(755,root,root) %{_bindir}/ctokens
%attr(755,root,root) %{_bindir}/cunlog
%attr(755,root,root) %{_bindir}/repair
%attr(755,root,root) %{_bindir}/cmon
%attr(755,root,root) %{_bindir}/codacon
%attr(755,root,root) %{_bindir}/cfs
%attr(755,root,root) %{_bindir}/getvolinfo
%attr(755,root,root) %{_bindir}/hoard
%attr(755,root,root) %{_bindir}/mkcodabf
#%attr(755,root,root) %{_bindir}/vcodacon
%attr(755,root,root) %{_bindir}/spy
%attr(755,root,root) %{_bindir}/parser
%attr(755,root,root) %{_bindir}/rvmsizer
%attr(755,root,root) %{_bindir}/smon2
%attr(755,root,root) %{_bindir}/filerepair
%attr(755,root,root) %{_bindir}/removeinc
%attr(755,root,root) %{_bindir}/xfrepair
%attr(755,root,root) %{_bindir}/xaskuser
%attr(755,root,root) %{_bindir}/gcodacon
%{_mandir}/man1/au.1*
%{_mandir}/man1/cfs.1*
%{_mandir}/man1/clog.1*
%{_mandir}/man1/coda_replay.1*
%{_mandir}/man1/cmon.1*
%{_mandir}/man1/cpasswd.1*
%{_mandir}/man1/ctokens.1*
%{_mandir}/man1/cunlog.1*
%{_mandir}/man1/hoard.1*
%{_mandir}/man1/mkcodabf.1*
%{_mandir}/man1/spy.1*
%{_mandir}/man1/repair.1*
%attr(755,root,root) %{_sbindir}/volmunge
%attr(755,root,root) %{_sbindir}/tokentool
#%attr(755,root,root) %{_sbindir}/sidekick
#%attr(755,root,root) %{_sbindir}/coda-client-logrotate
%attr(755,root,root) %{_bindir}/mklka

%files server
%defattr(644,root,root,755)
%{_sysconfdir}/coda/server.conf.ex
%attr(755,root,root) %{_sbindir}/asrlauncher
%attr(755,root,root) %{_sbindir}/codadump2tar
%attr(755,root,root) %{_sbindir}/startserver
%attr(755,root,root) %{_sbindir}/partial-reinit.sh
%attr(755,root,root) %{_sbindir}/createvol_rep
%attr(755,root,root) %{_sbindir}/pdbtool
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
#%attr(755,root,root) %{_sbindir}/rpc2portmap
%attr(755,root,root) %{_sbindir}/inoder
%attr(755,root,root) %{_sbindir}/parserecdump
%attr(755,root,root) %{_sbindir}/codasrv
%attr(755,root,root) %{_sbindir}/printvrdb
%attr(755,root,root) %{_sbindir}/updatesrv
%attr(755,root,root) %{_sbindir}/updateclnt
%attr(755,root,root) %{_sbindir}/updatefetch
%attr(755,root,root) %{_sbindir}/coda-server-logrotate
%attr(755,root,root) %{_sbindir}/norton
%attr(755,root,root) %{_sbindir}/norton-reinit
%attr(755,root,root) %{_bindir}/reinit
%{_mandir}/man5/backuplogs.5*
%{_mandir}/man5/dumpfile.5*
%{_mandir}/man5/dumplist.5*
%{_mandir}/man5/maxgroupid.5*
%{_mandir}/man5/passwd.coda.5*
%{_mandir}/man5/servers.5*
%{_mandir}/man5/vicetab.5*
%{_mandir}/man5/volumelist.5*
%{_mandir}/man5/vrdb.5*
%{_mandir}/man8/auth2.8*
%{_mandir}/man8/initpw.8*
%{_mandir}/man8/backup.8*
%{_mandir}/man8/bldvldb.sh.8*
%{_mandir}/man8/codasrv.8*
%{_mandir}/man8/createvol_rep.8*
%{_mandir}/man8/merge.8*
%{_mandir}/man8/norton.8*
%{_mandir}/man8/pdbtool.8*
%{_mandir}/man8/purgevol_rep.8*
%{_mandir}/man8/readdump.8*
%{_mandir}/man8/startserver.8*
%{_mandir}/man8/updateclnt.8*
%{_mandir}/man8/updatesrv.8*
%{_mandir}/man8/venus-setup.8*
%{_mandir}/man8/venus.8*
%{_mandir}/man8/vice-setup.8*
%{_mandir}/man8/volmunge.8*
%{_mandir}/man8/volutil.8*
%{_mandir}/man8/vutil.8*
%attr(754,root,root) /etc/rc.d/init.d/codasrv
%attr(754,root,root) /etc/rc.d/init.d/auth2
%attr(754,root,root) /etc/rc.d/init.d/update
%dir /var/lib/coda/vice
%dir /var/lib/coda/vice/auth2
%dir /var/lib/coda/vice/db
%dir /var/lib/coda/vice/misc
%dir /var/lib/coda/vice/spool
%dir /var/lib/coda/vice/srv

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
