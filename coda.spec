#
# TODO:
#   - more FHS-compilant changes (/coda, /usr/coda)
#   - separate some programs to coda-common package
#
Summary:	Coda distributed filesystem
Summary(pl):	Rozproszony system plików Coda
Name:		coda
Version:	5.3.20
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.coda.cs.cmu.edu/pub/coda/src/%{name}-%{version}.tar.gz
Source1:	%{name}.venus.init
Source2:	%{name}.auth2.init
Source3:	%{name}.codasrv.init
Source4:	%{name}.update.init
Patch0:		%{name}-ugly-common.patch
Patch1:		%{name}-FHS.patch
URL:		http://www.coda.cs.cmu.edu/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	lwp-devel
BuildRequires:	rvm-devel
BuildRequires:	rpc2-devel
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
Requires:	bc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Source package for the Coda filesystem. Three packages are provided by
this rpm: the client and server and the backup components. Separately
you must install a kernel module, or have a Coda enabled kernel, and
you should get the Coda documentation package.

%description -l pl
Pakiet ¼ród³owy systemu plików Coda. Rpm zawiera trzy pakiety:
klienta, serwer oraz komponenty do backupu. Nale¿y oddzielnie
zainstalowaæ modu³ do j±dra (lub mieæ j±dro z obs³ug± Cody), nale¿y
rownie¿ zaopatrzyæ siê w pakiet z dokumentacj± Cody.

%package common
Summary:	Coda filesystem common programs
Summary(pl):	Wspólne programy dla klienta i serwera systemu plików Coda
Group:		Networking/Daemons

%description common
This package contains programs used by server and client.

%description common -l pl
Ten pakiet zawiera programy u¿ywane przez klienta i serwer systemu plików
Coda.

%package client
Summary:	Coda client
Summary(pl):	Klient Cody
Group:		Networking/Daemons
Prereq:		/sbin/chkconfig
Requires:	coda-common

%description client
This package contains the main client program, the cachemanager Venus.
Also included are the binaries for the cfs, utilities for logging, ACL
manipulation etc, the hoarding tools for use with laptops and repair
tools for fixing conflicts. Finally there is the cmon and codacon
console utilities to monitor Coda's activities. You need a Coda
kernel-module for your kernel version, or Coda in your kernel, to have
a complete coda client. Make sure to select the correct C library
version.

%description client -l pl
Ten pakiet zawiera g³ównego klienta, zarz±dcê cache Venus. Do³±czone
s± tak¿e binaria cfs, narzêdzia do logowania, zarz±dzania ACL-ami
itp., narzêdzia do u¿ywania z laptopami i narzêdzia do naprawiania
konfliktów. S± tak¿e narzêdzia cmon i codacon do monitorowania
aktywno¶ci Cody. Pakiet wymaga Cody w kernelu lub module kernela.

%package server
Summary:	Coda server
Summary(pl):	Serwer Cody
Group:		Networking/Daemons
Prereq:		/sbin/chkconfig
Requires:	coda-common

%description server
This package contains the fileserver codasrv for the coda filesystem,
as well as the volume utilities. For highest performance you will need
a modified kernel with inode system calls.

%description server -l pl
Ten pakiet zawiera codasrv - serwer systemu plików Coda, oraz
narzêdzia do wolumenów. Aby osi±gn±æ lepsz± wydajno¶æ, potrzebny jest
zmodyfikowany kernel z wywo³aniami dotycz±cymi inodów.

%package backup
Summary:	Coda backup coordinator
Summary(pl):	Program do zarz±dzania backupem Cody
Group:		Networking

%description backup
This package contains the backup software for the coda filesystem, as
well as the volume utilities.

%description backup -l pl
Ten pakiet zawiera oprogramowanie do backupu systemu plików Coda oraz
narzêdzia do wolumenów.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
touch ChangeLog
#autoheader
%{__aclocal}
#autoconf
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

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/venus
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/auth2
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/codasrv
install %{SOURCE4} $RPM_BUILD_ROOT/etc/rc.d/init.d/update

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
if [ -e /usr/coda/etc/vstab ]; then
	touch /usr/coda/venus.cache/INIT
else
	%{_sbindir}/venus-setup testserver.coda.cs.cmu.edu 40000
fi
/sbin/chkconfig --add venus
if [ -f /var/lock/subsys/venus ]; then
	/etc/rc.d/init.d/venus restart >&2
else
	echo "Run \"/etc/rc.d/init.d/venus start\" to start venus." >&2
fi

%preun client
grep "^coda" /proc/mounts > /dev/null 2>&1
if [ $? = 0 ]; then
	echo "*** Coda is mounted: cannot uninstall ***"
	exit 1
else
	exit 0
fi
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/venus ]; then
		/etc/rc.d/init.d/venus stop >&2
	fi
	/sbin/chkconfig --del venus
fi

%post server
/sbin/chkconfig --add auth2
if [ -f /var/lock/subsys/auth2 ]; then
	/etc/rc.d/init.d/auth2 restart >&2
else
	echo "Run \"/etc/rc.d/init.d/auth2 start\" to start auth." >&2
fi
/sbin/chkconfig --add update
if [ -f /var/lock/subsys/update ]; then
	/etc/rc.d/init.d/update restart >&2
else
	echo "Run \"/etc/rc.d/init.d/update start\" to start update." >&2
fi
/sbin/chkconfig --add codasrv
if [ -f /var/lock/subsys/codasrv ]; then
	/etc/rc.d/init.d/codasrv restart >&2
else
	echo "Run \"/etc/rc.d/init.d/codasrv start\" to start codasrv." >&2
fi

%preun server
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/update ]; then
		/etc/rc.d/init.d/update stop >&2
	fi
	/sbin/chkconfig --del update
	if [ -f /var/lock/subsys/auth2 ]; then
		/etc/rc.d/init.d/auth2 stop >&2
	fi
	/sbin/chkconfig --del auth2
	if [ -f /var/lock/subsys/codasrv ]; then
		/etc/rc.d/init.d/codasrv stop >&2
	fi
	/sbin/chkconfig --del codasrv
fi

%files common
%defattr(644,root,root,755)
%dir %{_sysconfdir}/coda
%attr(755,root,root) %{_sbindir}/codaconfedit
%attr(755,root,root) %{_sbindir}/coda-setup-ports
%attr(755,root,root) %{_bindir}/rpc2ping

%files client
%defattr(644,root,root,755)
%dir %{_prefix}/coda
%dir %{_prefix}/coda%{_sysconfdir}
%dir %{_prefix}/coda/venus.cache
%verify() %{_prefix}/coda/venus.cache/INIT
%attr(754,root,root) /etc/rc.d/init.d/venus
%dir /coda
%verify() /coda/NOT_REALLY_CODA
%{_sysconfdir}/coda/venus.conf.ex
%attr(755,root,root) %{_sbindir}/codastart
%attr(755,root,root) %{_sbindir}/pwdtopdbtool.py
%attr(755,root,root) %{_sbindir}/venus-setup
%attr(755,root,root) %{_sbindir}/vutil
%attr(755,root,root) %{_sbindir}/venus
%attr(755,root,root) %{_sbindir}/au
%attr(755,root,root) %{_bindir}/clog
%attr(755,root,root) %{_bindir}/codaconfedit
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
%attr(755,root,root) %{_bindir}/spy
%attr(755,root,root) %{_bindir}/parser
%attr(755,root,root) %{_bindir}/smon2
%attr(755,root,root) %{_bindir}/filerepair
%attr(755,root,root) %{_bindir}/removeinc
%attr(755,root,root) %{_bindir}/xfrepair
%attr(755,root,root) %{_bindir}/xaskuser
%attr(755,root,root) %{_sbindir}/volmunge

%files server
%defattr(644,root,root,755)
%{_sysconfdir}/coda/server.conf.ex
%attr(755,root,root) %{_sbindir}/startserver
%attr(755,root,root) %{_sbindir}/partial-reinit.sh
%attr(755,root,root) %{_sbindir}/createvol_rep
%attr(755,root,root) %{_sbindir}/pdbtool
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
%attr(754,root,root) /etc/rc.d/init.d/codasrv
%attr(754,root,root) /etc/rc.d/init.d/auth2
%attr(754,root,root) /etc/rc.d/init.d/update

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
