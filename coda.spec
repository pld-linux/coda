Summary:	Coda distributed filesystem
Name:		coda
Version:	5.3.10
Release:	1
Copyright:	CMU
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source0:	%{name}-%{version}.tgz
Patch0:     	%{name}-ugly-common.patch
Requires:	bc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Source package for the Coda filesystem. Three packages are provided by
this rpm: the client and server and the backup components. Separately
you must install a kernel module, or have a Coda enabled kernel, and
you should get the Coda documentation package.
BEWARE: CVS VERSION

%description -l pl
Pakiet ¼ród³owy systemu plików Coda. Rpm zawiera trzy pakiety:
klienta, serwer oraz komponenty do backupu. Nale¿y oddzielnie
zainstalowaæ modu³ do j±dra (lub mieæ j±dro z obs³ug± Cody), nale¿y
rownie¿ zaopatrzyæ siê w pakiet z dokumentacj± Cody.
UWAGA: WERSJA CVS

%package client
Summary:	Coda client
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery

%description client
This package contains the main client program, the cachemanager Venus.
Also included are the binaries for the cfs, utilities for logging, ACL
manipulation etc, the hoarding tools for use with laptops and repair
tools for fixing conflicts. Finally there is the cmon and codacon
console utilities to monitor Coda's activities. You need a Coda
kernel-module for your kernel version, or Coda in your kernel, to have
a complete coda client. Make sure to select the correct C library
version.
BEWARE: CVS VERSION

%package server
Summary:	Coda server
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery

%description server
This package contains the fileserver codasrv for the coda filesystem,
as well as the volume utilities. For highest performance you will need
a modified kernel with inode system calls.
BEWARE: CVS VERSION

%package backup
Summary:	Coda backup coordinator
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
%description backup
This package contains the backup software for the coda filesystem, as
well as the volume utilities.
BEWARE: CVS VERSION


%prep
%setup -q
%patch0 -p1

%build
touch ChangeLog
autoheader
aclocal
autoconf
#%configure
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
./configure %{_target_platform} \
	--prefix=%{_prefix}
%{__make} OPTFLAGS="$RPM_OPT_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_prefix}/coda/venus.cache $RPM_BUILD_ROOT/dev \
	$RPM_BUILD_ROOT%{_prefix}/coda%{_sysconfdir} \
	$RPM_BUILD_ROOT/coda $RPM_BUILD_ROOT/etc/rc.d/init.d\
	$RPM_BUILD_ROOT%{_libdir}/coda

%{__make} client-install
%{__make} server-install

touch $RPM_BUILD_ROOT%{_prefix}/coda/venus.cache/INIT
mknod $RPM_BUILD_ROOT/dev/cfs0 c 67 0
touch $RPM_BUILD_ROOT/coda/NOT_REALLY_CODA

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

cd %{_libdir}/coda
if [ ! -x %{_bindir}/tixindex ]; then
	chmod a+x %{_bindir}/tixindex 
fi
tixindex *tcl
#if [ ! -f %{_bindir}/tixwish ]; then
#	ln -s %{_bindir}/tixwish* /usr/bin/tixwish
#	if [ x$? != x0 ]; then
#		echo "**WARNING:tixwish is not correctly installed"
#	fi
#fi
/sbin/chkconfig --add venus.init

%postun
/sbin/chkconfig --del venus.init

%post server
/sbin/chkconfig --add update.init
/sbin/chkconfig --add auth2.init
/sbin/chkconfig --add codasrv.init

%postun server
/sbin/chkconfig --del update.init
/sbin/chkconfig --del auth2.init
/sbin/chkconfig --del codasrv.init

%files client
%defattr(644,root,root,755)
/dev/cfs0
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
%attr(755,root,root) %{_bindir}/advice_srv
%attr(755,root,root) %{_bindir}/filcon
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
%attr(755,root,root) %{_bindir}/logbandwidth
%attr(755,root,root) %{_bindir}/logcmls
%attr(755,root,root) %{_bindir}/logreintegration
%attr(755,root,root) %{_sbindir}/volmunge
%{_libdir}/coda/Advice.tcl
%{_libdir}/coda/CodaConsole
%{_libdir}/coda/Consider.tcl
%{_libdir}/coda/ConsiderAdding.tcl
%{_libdir}/coda/ConsiderRemoving.tcl
%{_libdir}/coda/ControlPanel.tcl
%{_libdir}/coda/Date.tcl
%{_libdir}/coda/DiscoMiss.tcl
%{_libdir}/coda/Events.tcl
%{_libdir}/coda/Globals.tcl
%{_libdir}/coda/Helper.tcl
%{_libdir}/coda/HoardWalk.tcl
%{_libdir}/coda/HoardWalkAdvice.tcl
%{_libdir}/coda/Indicators.tcl
%{_libdir}/coda/Initialization.tcl
%{_libdir}/coda/Lock.tcl
%{_libdir}/coda/Log.tcl
%{_libdir}/coda/Network.tcl
%{_libdir}/coda/OutsideWorld.tcl
%{_libdir}/coda/ReadMiss.tcl
%{_libdir}/coda/Reconnection.tcl
%{_libdir}/coda/Reintegration.tcl
%{_libdir}/coda/Repair.tcl
%{_libdir}/coda/Space.tcl
%{_libdir}/coda/Task.tcl
%{_libdir}/coda/Timing.tcl
%{_libdir}/coda/Tokens.tcl
%{_libdir}/coda/WeakMiss.tcl
%{_libdir}/coda/tixCodaMeter.tcl

%files server	
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/rvmutl
%attr(755,root,root) %{_sbindir}/rdsinit
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
%attr(755,root,root) %{_sbindir}/vice-setup-ports
%attr(755,root,root) %{_sbindir}/vice-killvolumes
%attr(755,root,root) %{_sbindir}/pcfgen
%attr(755,root,root) %{_sbindir}/pwd2pdb
%attr(755,root,root) %{_sbindir}/mvdb
%attr(755,root,root) %{_sbindir}/auth2
%attr(755,root,root) %{_sbindir}/initpw
%attr(755,root,root) %{_sbindir}/volutil
%attr(755,root,root) %{_sbindir}/rpc2portmap
%attr(755,root,root) %{_sbindir}/makeftree
%attr(755,root,root) %{_sbindir}/inoder
%attr(755,root,root) %{_sbindir}/parserecdump
%attr(755,root,root) %{_sbindir}/codasrv
%attr(755,root,root) %{_sbindir}/printvrdb
%attr(755,root,root) %{_sbindir}/updatesrv
%attr(755,root,root) %{_sbindir}/updateclnt
%attr(755,root,root) %{_sbindir}/updatefetch
%attr(755,root,root) %{_bindir}/filcon
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
%attr(755,root,root) %{_bindir}/filcon
