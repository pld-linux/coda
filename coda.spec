Summary:	Coda distributed filesystem
Name:		coda
Version:	5.2.0
Release:	1
Copyright:	CMU
Group:		Networking/Daemons
Source:		ftp://ftp.coda.cs.cmu.edu/pub/coda/src/%{name}-%{version}.tgz
Requires:	bc
BuildRoot:	/tmp/%{name}-%{version}-root

%description
Source package for the Coda filesystem.  Three packages are provided by
this rpm: the client and server and the backup components. Separately
you must install a kernel module, or have a Coda enabled kernel, and 
you should get the Coda documentation package.

%package client
Summary:	Coda client
Group:		Networking/Daemons

%description client
This package contains the main client program, the cachemanager Venus.
Also included are the binaries for the cfs, utilities for logging, ACL
manipulation etc, the hoarding tools for use with laptops and repair
tools for fixing conflicts. Finally there is the cmon and codacon
console utilities to monitor Coda's activities. You need a Coda
kernel-module for your kernel version, or Coda in your kernel, to have
a complete coda client.  Make sure to select the correct C library
version.

%package server
Summary:	Coda server
Group:		Networking/Daemons

%description server
This package contains the fileserver codasrv for the coda filesystem,
as well as the volume utilities.  For highest performance you will
need a modified kernel with inode system calls.

%package backup
Summary: Coda backup coordinator
Group: Networking/Daemons
%description backup
This package contains the backup software for the coda filesystem, as
well as the volume utilities.

	
%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
./configure %{_target_platform} \
	--prefix=/usr
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/usr/coda/venus.cache $RPM_BUILD_ROOT/dev \
	$RPM_BUILD_ROOT/usr/coda/etc \
	$RPM_BUILD_ROOT/coda $RPM_BUILD_ROOT/etc/rc.d/init.d\
	$RPM_BUILD_ROOT%{_libdir}/coda

make client-install
make server-install

touch $RPM_BUILD_ROOT/usr/coda/venus.cache/INIT
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
#		echo "**WARNING: tixwish is not correctly installed"
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
/dev/cfs0
%dir /usr/coda
%dir /usr/coda/etc
%dir /usr/coda/venus.cache
%verify() /usr/coda/venus.cache/INIT
/etc/rc.d/init.d/venus.init
%dir /coda
%verify() /coda/NOT_REALLY_CODA
%{_sbindir}/venus-setup
%{_sbindir}/vutil
%{_sbindir}/venus
%{_sbindir}/au
%{_bindir}/advice_srv
%{_bindir}/filcon
%{_bindir}/clog
%{_bindir}/cpasswd
%{_bindir}/ctokens
%{_bindir}/cunlog
%{_bindir}/repair
%{_bindir}/cmon
%{_bindir}/codacon
%{_bindir}/cfs
%{_bindir}/hoard
%{_bindir}/spy
%{_bindir}/replay
%{_bindir}/parser
%{_bindir}/filerepair
%{_bindir}/removeinc
%{_bindir}/xfrepair
%{_bindir}/xaskuser
%{_bindir}/logbandwidth
%{_bindir}/logcmls
%{_bindir}/logreintegration
%{_sbindir}/volmunge
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
%{_sbindir}/rvmutl
%{_sbindir}/rdsinit
%{_sbindir}/startserver
%{_sbindir}/partial-reinit.sh
%{_sbindir}/createvol_rep
%{_sbindir}/purgevol
%{_sbindir}/purgevol_rep
%{_sbindir}/bldvldb.sh
%{_sbindir}/vice-setup
%{_sbindir}/vice-setup-rvm
%{_sbindir}/vice-setup-srvdir
%{_sbindir}/vice-setup-user
%{_sbindir}/vice-setup-scm
%{_sbindir}/vice-setup-ports
%{_sbindir}/vice-killvolumes
%{_sbindir}/pcfgen
%{_sbindir}/pwd2pdb
%{_sbindir}/mvdb
%{_sbindir}/auth2
%{_sbindir}/initpw
%{_sbindir}/volutil
%{_sbindir}/rpc2portmap
%{_sbindir}/makeftree
%{_sbindir}/inoder
%{_sbindir}/parserecdump
%{_sbindir}/codasrv
%{_sbindir}/printvrdb
%{_sbindir}/updatesrv
%{_sbindir}/updateclnt
%{_sbindir}/updatefetch
%{_bindir}/filcon
%{_bindir}/norton
%{_bindir}/norton-reinit
%{_bindir}/reinit
/etc/rc.d/init.d/codasrv.init
/etc/rc.d/init.d/auth2.init
/etc/rc.d/init.d/update.init

%files backup	
%{_sbindir}/backup.sh
%{_sbindir}/tape.pl
%{_sbindir}/auth2
%{_sbindir}/volutil
%{_sbindir}/backup
%{_sbindir}/readdump
%{_sbindir}/merge
%{_sbindir}/updatesrv
%{_sbindir}/updateclnt
%{_sbindir}/updatefetch
%{_bindir}/filcon

%changelog
* Fri Feb 12 1999 Bernhard Rosenkraenzer <bero@microsoft.sucks.eu.org>
- adapt to BeroLinux

* Sun Jun 21 1998 Peter Braam <braam@cs.cmu.edu>
- get rid of the kernel package. This needs interaction during the build.
- no more separate libc, glibc packages

* Tue Dec 30 1997 Peter Braam <braam@cs.cmu.edu>
- several changes: documentation separate
- use variables: =`uname -r`, 5.0.1=coda version

* Mon Jun 02 1997 Peter Braam <braam@cs.cmu.edu>
- small changes to Elliots improvements.
- some of his ideas are now in the scripts

* Wed May 28 1997 Elliot Lee <sopwith@redhat.com>
- Based upon 4.0.3-1 spec file.
- Changed to BuildRoot
- Do as much as possible at build time instead of in %post
- Added initscript for venus
