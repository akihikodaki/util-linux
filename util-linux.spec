# Upstream maintainer aeb@cwi.nl

%define make_options HAVE_PIVOT_ROOT=yes HAVE_PAM=yes HAVE_SHADOW=no HAVE_PASSWD=yes ALLOW_VCS_USE=no ADD_RAW=yes HAVE_SLANG=yes HAVE_SELINUX=yes SLANGFLAGS=-I/usr/include/slang INSTALLSUID='$(INSTALL) -m $(SUIDMODE)' USE_TTY_GROUP=no
%define make_cflags -DUSE_TTY_GROUP -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 

%define with_kbdrate 0
%define floppyver 0.12
%define cramfsver 1.1
%define no_hwclock_archs s390 s390x
%define cytune_archs %{ix86} alpha armv4l

Summary: A collection of basic system utilities.
Name: util-linux
Version: 2.12a
Release: 10
License: distributable
Group: System Environment/Base

BuildRequires: sed
BuildRequires: pam-devel
BuildRequires: ncurses-devel
BuildRequires: libtermcap-devel
BuildRequires: zlib-devel
BuildRequires: slang-devel
BuildRequires: texinfo
BuildRequires: gettext
BuildRequires: libselinux-devel

Source0: ftp://ftp.win.tue.nl/pub/linux-local/utils/util-linux/util-linux-%{version}.tar.gz
Source1: util-linux-selinux.pamd
Source4: util-linux-2.7-login.pamd
Source2: util-linux-2.7-chfn.pamd
Source3: util-linux-2.7-chsh.pamd
Source8: nologin.c
Source9: nologin.8
Source10: kbdrate.tar.gz
Source11: http://download.sourceforge.net/floppyutil/floppy-%{floppyver}.tar.gz
Source12: http://download.sourceforge.net/cramfs/cramfs-%{cramfsver}.tar.gz

##### Red Hat Linux-specific patches
# 1. Add the option of not installing chkdupexe (WANT_CHKDUPEXE=no)
# 2. Change 
Patch: util-linux-2.12a-moretc.patch

# Reduce MAX_PARTS to 16 (upstream reasonably won't take it)
Patch70: util-linux-2.12a-partlimit.patch

# Note on how to set up raw device mappings using RHL /etc/sysconfig/rawdevices
Patch109: util-linux-2.11f-rawman.patch

######## Patches that should be upstream eventually
Patch100: util-linux-2.12a-managed.patch

Patch106: util-linux-2.11w-swaponsymlink-57300.patch
Patch107: util-linux-2.11y-procpartitions-37436.patch
Patch113: util-linux-2.11r-ctty3.patch
Patch117: util-linux-2.11y-moremisc.patch

Patch120: util-linux-2.11y-skipraid2.patch
Patch125: util-linux-2.11y-umask-82552.patch
Patch126: util-linux-2.11y-multibyte.patch
Patch128: util-linux-2.12a-ipcs-84243-86285.patch

Patch131: util-linux-2.11y-sysmap-85407.patch
Patch138: util-linux-2.11y-chsh-103004.patch
Patch139: util-linux-2.11y-fdisksegv-103954.patch
Patch140: util-linux-2.11y-alldevs-101772.patch
Patch142: util-linux-2.11y-mountman-90588.patch

Patch143: cramfs-1.1-blocksize_and_quiet.patch
Patch144: cramfs-1.1-pagesize.patch

Patch145: util-linux-2.12.pam.patch
Patch147: util-linux-2.12a-126572-fdiskman.patch
Patch148: util-linux-2.12a-127097-labelcrash.patch
Patch149: util-linux-2.12a-125531-swaplabel.patch
Patch150: floppy-0.12-locale.patch

Patch151: util-linux-2.12a-mountbylabel-dm.patch
Patch152: util-linux-2.12a-mountnolabel.patch
Patch153: util-linux-2.12a-16415-rdevman.patch
Patch154: util-linux-2.11y-102566-loginman.patch
Patch155: util-linux-2.12a-104321-rescuept.patch
Patch156: util-linux-2.12a-fdiskmessage-107824.patch

# Patch to enabled remote service for login/pam (#91174)
Patch157: util-linux-2.12a-pamstart.patch

Patch158: util-linux-2.12a-moreswaplabel.patch

# patches required for NFSv4 support
Patch1000: util-linux-2.12-nfsv4.patch

# When adding patches, please make sure that it is easy to find out what bug # the 
# patch fixes.
########### END upstreamable

Obsoletes: fdisk tunelp
%ifarch alpha sparc sparc64 sparcv9 s390
Obsoletes: clock
%endif
%ifarch alpha
Conflicts: initscripts <= 4.58, timeconfig <= 3.0.1
%endif
BuildRoot: %{_tmppath}/%{name}-root
Requires: pam >= 0.66-4, /etc/pam.d/system-auth
%if %{with_kbdrate}
Requires: usermode
%endif
Conflicts: kernel < 2.2.12-7, 
Prereq: /sbin/install-info
Obsoletes: mount losetup
Provides: mount = %{version}
Provides: losetup = %{version}

%description
The util-linux package contains a large variety of low-level system
utilities that are necessary for a Linux system to function. Among
others, Util-linux contains the fdisk configuration tool and the login
program.

%if 0
%package -n mount
Group: System Environment/Base
Summary: Programs for mounting and unmounting filesystems.
ExclusiveOS: Linux

%description -n mount
The mount package contains the mount, umount, swapon, and swapoff
programs. Accessible files on your system are arranged in one big tree
or hierarchy. These files can be spread out over several devices. The
mount command attaches a filesystem on some device to your system's
file tree. The umount command detaches a filesystem from the
tree. Swapon and swapoff, respectively, specify and disable devices
and files for paging and swapping.

%package -n losetup
Summary: Programs for setting up and configuring loopback devices.
Group: System Environment/Base

%description -n losetup
Linux supports a special block device called the loop device, which
maps a normal file onto a virtual block device. This allows for the
file to be used as a "virtual file system" inside another file.
Losetup is used to associate loop devices with regular files or block
devices, to detach loop devices and to query the status of a loop
device.
%endif

%prep

%setup -q -a 10 -a 11 -a 12

%patch0 -p1

%patch70 -p1

# nologin
cp %{SOURCE8} %{SOURCE9} .

%patch100 -p1

sed -e 's:^MAN_DIR=.*:MAN_DIR=%{_mandir}:' -e 's:^INFO_DIR=.*:INFO_DIR=%{_infodir}:' MCONFIG > MCONFIG.new
mv MCONFIG.new MCONFIG

%patch106 -p1
%patch107 -p1
%patch109 -p1

%patch113 -p1
%patch117 -p1
%patch120 -p1

%patch125 -p1
%patch126 -p1
%patch128 -p1

%patch131 -p1
%patch138 -p1
%patch139 -p1
%patch140 -p1
%patch142 -p1

# cramfs
%patch143 -p0
%patch144 -p1

%patch145 -p1
%patch147 -p1
%patch148 -p1
%patch149 -p1
%patch150 -p0

%patch151 -p1
%patch152 -p1
%patch153 -p1
%patch154 -p1
%patch155 -p1
%patch156 -p1 -b .fdiskmessage
%patch157 -p1 -b .pamstart
%patch158 -p1

%patch1000 -p1 -b .nfsv4

%build
unset LINGUAS || :

%configure

make OPT="$RPM_OPT_FLAGS %{make_cflags}" \
	LDFLAGS="" \
	%{make_options} \
	%{?_smp_mflags}
make LDFLAGS="" CFLAGS="$RPM_OPT_FLAGS" -C partx %{?_smp_mflags}
cd rescuept
cc -D_FILE_OFFSET_BITS=64 $RPM_OPT_FLAGS -o rescuept rescuept.c
cd ..

%if %{with_kbdrate}
pushd kbdrate
    cc $RPM_OPT_FLAGS -o kbdrate kbdrate.c
popd
%endif

pushd floppy-%{floppyver}
# We have to disable floppygtk somehow...
%configure --with-gtk-prefix=/asfd/jkl
make %{?_smp_mflags}
popd

make -C cramfs-%{cramfsver} %{?_smp_mflags}

gcc $RPM_OPT_FLAGS -o nologin nologin.c

pushd sys-utils
    makeinfo --number-sections ipc.texi
popd

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/{bin,sbin}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_infodir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man{1,6,8,5}
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/{pam.d,security/console.apps}

make \
	OPT="$RPM_OPT_FLAGS %{make_cflags}" \
	LDFLAGS="" \
	%{make_options} \
        INSTALLDIR="install -d -m 755" \
        INSTALLSUID="install -m 755" \
        INSTALLBIN="install -m 755" \
        INSTALLMAN="install -m 644" \
	install DESTDIR=${RPM_BUILD_ROOT}
pushd floppy-%{floppyver}
%makeinstall
popd

pushd cramfs-%{cramfsver}
install -s -m 755 mkcramfs ${RPM_BUILD_ROOT}/sbin/mkfs.cramfs
ln -s ../../sbin/mkfs.cramfs ${RPM_BUILD_ROOT}/usr/bin/mkcramfs
install -s -m 755 cramfsck ${RPM_BUILD_ROOT}/sbin/fsck.cramfs
popd

install -m 755 mount/pivot_root ${RPM_BUILD_ROOT}/sbin
install -m 644 mount/pivot_root.8 ${RPM_BUILD_ROOT}%{_mandir}/man8
install -m 755 rescuept/rescuept ${RPM_BUILD_ROOT}/sbin
mv rescuept/README rescuept/README.rescuept
install -m 755 nologin ${RPM_BUILD_ROOT}/sbin
install -m 644 nologin.8 ${RPM_BUILD_ROOT}%{_mandir}/man8
%if %{with_kbdrate}
install -m 755 kbdrate/kbdrate ${RPM_BUILD_ROOT}/sbin
install -m 644 kbdrate/kbdrate.8 ${RPM_BUILD_ROOT}%{_mandir}/man8
ln -s consolehelper ${RPM_BUILD_ROOT}/usr/bin/kbdrate
%endif
echo '.so man8/raw.8' > $RPM_BUILD_ROOT%{_mandir}/man8/rawdevices.8

install -m 755 partx/{addpart,delpart,partx} $RPM_BUILD_ROOT/sbin

# Correct mail spool path.
sed -e 's,/usr/spool/mail,/var/spool/mail,g' ${RPM_BUILD_ROOT}%{_mandir}/man1/login.1 > ${RPM_BUILD_ROOT}%{_mandir}/man1/login.1.new 
mv ${RPM_BUILD_ROOT}%{_mandir}/man1/login.1.new ${RPM_BUILD_ROOT}%{_mandir}/man1/login.1

if [ "%{_infodir}" != "%{_prefix}/info" -a -d ${RPM_BUILD_ROOT}%{_prefix}/info ]; then
   ( cd ${RPM_BUILD_ROOT}%{_prefix}/info; tar cf - ./* ) |
   ( cd ${RPM_BUILD_ROOT}%{_infodir}; tar xf - )
   ( cd ${RPM_BUILD_ROOT}%{_prefix}; rm -rf ./info )
fi

%ifarch sparc sparc64 sparcv9
rm -rf ${RPM_BUILD_ROOT}%{_bindir}/sunhostid
cat << E-O-F > ${RPM_BUILD_ROOT}%{_bindir}/sunhostid
#!/bin/sh
# this should be %{_bindir}/sunhostid or somesuch.
# Copyright 1999 Peter Jones, <pjones@redhat.com> .  
# GPL and all that good stuff apply.
(
idprom=\`cat /proc/openprom/idprom\`
echo \$idprom|dd bs=1 skip=2 count=2
echo \$idprom|dd bs=1 skip=27 count=6
echo
) 2>/dev/null
E-O-F
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/sunhostid
%endif

gzip -9nf ${RPM_BUILD_ROOT}%{_infodir}/ipc.info

%if %{with_kbdrate}
install -m644 kbdrate/kbdrate.apps $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/kbdrate
install -m644 kbdrate/kbdrate.pam $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/kbdrate
%endif
{ 
  pushd ${RPM_BUILD_ROOT}%{_sysconfdir}/pam.d
  install -m 644 %{SOURCE1} ./login
  install -m 644 ${RPM_SOURCE_DIR}/util-linux-2.7-chsh.pamd ./chsh
  install -m 644 ${RPM_SOURCE_DIR}/util-linux-2.7-chsh.pamd ./chfn
  popd
}

ln -sf ../../sbin/hwclock ${RPM_BUILD_ROOT}/usr/sbin/hwclock
ln -sf ../../sbin/clock ${RPM_BUILD_ROOT}/usr/sbin/clock
ln -sf hwclock ${RPM_BUILD_ROOT}/sbin/clock

# We do not want dependencies on csh
chmod 644 ${RPM_BUILD_ROOT}%{_datadir}/misc/getopt/*
rm -f fdisk/README.cfdisk

# Final cleanup
%ifnarch %cytune_archs
rm -f $RPM_BUILD_ROOT%{_bindir}/cytune $RPM_BUILD_ROOT%{_mandir}/man8/cytune.8*
%endif
%ifarch %no_hwclock_archs
rm -f $RPM_BUILD_ROOT/sbin/{hwclock,clock} $RPM_BUILD_ROOT%{_mandir}/man8/hwclock.8*
%endif
%ifarch s390 s390x
rm -f $RPM_BUILD_ROOT/usr/{bin,sbin}/{fdformat,tunelp,floppy,setfdprm} $RPM_BUILD_ROOT%{_mandir}/man8/{fdformat,tunelp,floppy,setfdprm}.8*
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/fdprm
%endif

for I in /sbin/cfdisk /sbin/fsck.minix /sbin/mkfs.{bfs,minix} /sbin/sln /usr/bin/chkdupexe \
	%{_bindir}/line %{_bindir}/pg %{_bindir}/raw; do
	rm -f $RPM_BUILD_ROOT$I
done

for I in man1/chkdupexe.1 man1/line.1 man1/pg.1 man8/cfdisk.8 man8/fsck.minix.8 man8/mkfs.minix.8 man8/mkfs.bfs.8 \
	man8/raw.8 man8/rawdevices.8; do
	rm -rf $RPM_BUILD_ROOT%{_mandir}/${I}*
done

ln -sf ../../bin/kill $RPM_BUILD_ROOT%{_bindir}/kill

%find_lang %{name}

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info %{_infodir}/ipc.info* %{_infodir}/dir

%postun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/ipc.info* %{_infodir}/dir
fi

%files -f %{name}.lang
%defattr(-,root,root)
%doc */README.* HISTORY MAINTAINER

/bin/arch
/bin/dmesg
%attr(755,root,root)	/bin/login
/bin/more
/bin/kill

%ifnarch s390 s390x
%config %{_sysconfdir}/fdprm
%endif
%config %{_sysconfdir}/pam.d/chfn
%config %{_sysconfdir}/pam.d/chsh
%config %{_sysconfdir}/pam.d/login

/sbin/agetty
%{_mandir}/man8/agetty.8*
/sbin/blockdev
/sbin/pivot_root
/sbin/ctrlaltdel
/sbin/elvtune
/sbin/addpart
/sbin/delpart
/sbin/partx

/sbin/sfdisk
%{_mandir}/man8/sfdisk.8*
%doc fdisk/sfdisk.examples

/sbin/fdisk
%{_mandir}/man8/fdisk.8*
%ifnarch %no_hwclock_archs
/sbin/clock
/sbin/hwclock
/usr/sbin/hwclock
%{_mandir}/man8/hwclock.8*
%endif
/sbin/mkfs
/sbin/mkswap
/sbin/rescuept
/sbin/nologin
%{_mandir}/man8/nologin.8*

# Begin kbdrate stuff
%if %{with_kbdrate}
/sbin/kbdrate
/usr/bin/kbdrate
%{_mandir}/man8/kbdrate.8*
%{_sysconfdir}/pam.d/kbdrate
%{_sysconfdir}/security/console.apps/kbdrate
%endif

%{_bindir}/cal
%attr(4711,root,root)	%{_bindir}/chfn
%attr(4711,root,root)	%{_bindir}/chsh
%{_bindir}/col
%{_bindir}/colcrt
%{_bindir}/colrm
%{_bindir}/column
%ifarch %cytune_archs
%{_bindir}/cytune
%{_mandir}/man8/cytune.8*
%endif
%{_bindir}/ddate
%ifnarch s390 s390x
%{_bindir}/fdformat
%endif
%{_bindir}/getopt
%{_bindir}/hexdump
%{_bindir}/ipcrm
%{_bindir}/ipcs
%{_bindir}/isosize
%{_bindir}/kill
%{_bindir}/logger
%{_bindir}/look
%{_bindir}/mcookie
%{_bindir}/mkcramfs
/sbin/fsck.cramfs
/sbin/mkfs.cramfs
%ifnarch s390 s390x
%{_bindir}/floppy
%{_mandir}/man8/floppy.8*
%endif
%{_bindir}/namei
%attr(4711,root,root)	%{_bindir}/newgrp
%{_bindir}/rename
%{_bindir}/renice
%{_bindir}/rev
%{_bindir}/script
%ifnarch s390 s390x
%{_bindir}/setfdprm
%endif
%{_bindir}/setsid
%{_bindir}/setterm
%ifarch sparc sparc64 sparcv9
%{_bindir}/sunhostid
%endif
%{_bindir}/tailf
%{_bindir}/ul
%{_bindir}/whereis
%attr(2755,root,tty)	%{_bindir}/write

%ifarch %{ix86}
%{_sbindir}/rdev
%{_sbindir}/ramsize
%{_sbindir}/rootflags
%{_sbindir}/vidmode
%{_mandir}/man8/rdev.8*
%{_mandir}/man8/ramsize.8*
%{_mandir}/man8/rootflags.8*
%{_mandir}/man8/vidmode.8*
%endif
%{_sbindir}/readprofile
%ifnarch s390 s390x
%{_sbindir}/tunelp
%endif
%{_sbindir}/vipw
%{_sbindir}/vigr

%{_infodir}/ipc.info*

%{_mandir}/man1/arch.1*
%{_mandir}/man1/cal.1*
%{_mandir}/man1/chfn.1*
%{_mandir}/man1/chsh.1*
%{_mandir}/man1/col.1*
%{_mandir}/man1/colcrt.1*
%{_mandir}/man1/colrm.1*
%{_mandir}/man1/column.1*
%{_mandir}/man1/ddate.1*
%{_mandir}/man1/getopt.1*
%{_mandir}/man1/hexdump.1*
%{_mandir}/man1/kill.1*
%{_mandir}/man1/logger.1*
%{_mandir}/man1/login.1*
%{_mandir}/man1/look.1*
%{_mandir}/man1/mcookie.1*
%{_mandir}/man1/more.1*
%{_mandir}/man1/namei.1*
%{_mandir}/man1/newgrp.1*
%{_mandir}/man1/readprofile.1*
%{_mandir}/man1/rename.1*
%{_mandir}/man1/rev.1*
%{_mandir}/man1/script.1*
%{_mandir}/man1/setterm.1*
%{_mandir}/man1/tailf.1*
%{_mandir}/man1/ul.1*
%{_mandir}/man1/whereis.1*
%{_mandir}/man1/write.1*

%{_mandir}/man8/blockdev.8*
%{_mandir}/man8/ctrlaltdel.8*
%{_mandir}/man8/dmesg.8*
%{_mandir}/man8/elvtune.8*
%ifnarch s390 s390x
%{_mandir}/man8/fdformat.8*
%endif
%{_mandir}/man8/ipcrm.8*
%{_mandir}/man8/ipcs.8*
%{_mandir}/man8/isosize.8*
%{_mandir}/man8/mkfs.8*
%{_mandir}/man8/mkswap.8*
%{_mandir}/man8/pivot_root.8*
%{_mandir}/man8/renice.8*
%ifnarch s390 s390x
%{_mandir}/man8/setfdprm.8*
%endif
%{_mandir}/man8/setsid.8*
# XXX this man page should be moved to glibc.
%{_mandir}/man8/sln.8*
%ifnarch s390 s390x
%{_mandir}/man8/tunelp.8*
%endif
%{_mandir}/man8/vigr.8*
%{_mandir}/man8/vipw.8*

%{_datadir}/misc/getopt

#files -n mount
#defattr(-,root,root)
%attr(4755,root,root)   /bin/mount
%attr(4755,root,root)   /bin/umount
/sbin/swapon
/sbin/swapoff
%{_mandir}/man5/fstab.5*
%{_mandir}/man5/nfs.5*
%{_mandir}/man8/mount.8*
%{_mandir}/man8/swapoff.8*
%{_mandir}/man8/swapon.8*
%{_mandir}/man8/umount.8*

#files -n losetup
#defattr(-,root,root)
%{_mandir}/man8/losetup.8*
/sbin/losetup

%changelog
* Wed Sep 29 2004 Elliot Lee <sopwith@redhat.com> 2.12a-10
- Make swaplabel support work with swapon -a -e

* Tue Sep 28 2004 Steve Dickson <SteveD@RedHat.com>
- Updated the NFS and NFS4 code to the latest CITI patch set
  (in which they incorporate a number of our local patches).

* Wed Sep 15 2004 Nalin Dahybhai <nalin@redhat.com> 2.12a-8
- Fix #132196 - turn on SELinux support at build-time.

* Wed Sep 15 2004 Phil Knirsch <pknirsch@redhat.com> 2.12a-7
- Fix #91174 with pamstart.patch

* Tue Aug 31 2004 Elliot Lee <sopwith@redhat.com> 2.12a-6
- Fix #16415, #70616 with rdevman.patch
- Fix #102566 with loginman.patch
- Fix #104321 with rescuept.patch (just use plain lseek - we're in _FILE_OFFSET_BITS=64 land now)
- Fix #130016 - remove raw.
- Re-add agetty (replacing it with mgetty is too much pain, and mgetty is much larger)

* Thu Aug 26 2004 Steve Dickson <SteveD@RedHat.com>
- Made the NFS security checks more explicit to avoid confusion
  (an upstream fix)
- Also removed a compilation warning

* Wed Aug 11 2004 Alasdair Kergon <agk@redhat.com>
- Remove unused mount libdevmapper inclusion.

* Wed Aug 11 2004 Alasdair Kergon <agk@redhat.com>
- Add device-mapper mount-by-label support
- Fix segfault in mount-by-label when a device without a label is present.

* Wed Aug 11 2004 Steve Dickson <SteveD@RedHat.com>
- Updated nfs man page to show that intr are on by
  default for nfs4

* Thu Aug 05 2004 Jindrich Novy <jnovy@redhat.com>
- modified warning causing heart attack for >16 partitions, #107824

* Fri Jul 09 2004 Elliot Lee <sopwith@redhat.com> 2.12a-3
- Fix #126623, #126572
- Patch cleanup
- Remove agetty (use mgetty, agetty is broken)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jun 03 2004 Elliot Lee <sopwith@redhat.com> 2.12a-1
- Update to 2.12a
- Fix #122448

* Thu May 13 2004 Dan Walsh <dwalsh@RedHat.com> 2.12-19
- Change pam_selinux to run last

* Tue May 04 2004 Elliot Lee <sopwith@redhat.com> 2.12-18
- Fix #122448 (autofs issues)

* Fri Apr 23 2004 Elliot Lee <sopwith@redhat.com> 2.12-17
- Fix #119157 by editing the patch
- Add patch145 to fix #119986

* Fri Apr 16 2004 Elliot Lee <sopwith@redhat.com> 2.12-16
- Fix #118803

* Tue Mar 23 2004 Jeremy Katz <katzj@redhat.com> 2.12-15
- mkcramfs: use PAGE_SIZE for default blocksize (#118681)

* Sat Mar 20 2004 <SteveD@RedHat.com>
- Updated the nfs-mount.patch to correctly 
  handle the mounthost option and to ignore 
  servers that do not set auth flavors

* Tue Mar 16 2004 Dan Walsh <dwalsh@RedHat.com> 2.12-13
- Fix selinux ordering or pam for login

* Tue Mar 16 2004 <SteveD@RedHat.com>
- Make RPC error messages displayed with -v argument
- Added two checks to the nfs4 path what will print warnings
  when rpc.idmapd and rpc.gssd are not running
- Ping NFS v4 servers before diving into kernel
- Make v4 mount interruptible which also make the intr option on by default 

* Sun Mar 13 2004  <SteveD@RedHat.com>
- Reworked how the rpc.idmapd and rpc.gssd checks were
  done due to review comments from upstream.
- Added rpc_strerror() so the '-v' flag will show RPC errors.

* Sat Mar 13 2004  <SteveD@RedHat.com>
- Added two checks to the nfs4 path what will print warnings
  when rpc.idmapd and rpc.gssd are not running.

* Thu Mar 11 2004 <SteveD@RedHat.com>
- Reworked and updated the nfsv4 patches.

* Wed Mar 10 2004 Dan Walsh <dwalsh@RedHat.com>
- Bump version

* Wed Mar 10 2004 Steve Dickson <SteveD@RedHat.com>
- Tried to make nfs error message a bit more meaninful
- Cleaned up some warnings

* Sun Mar  7 2004 Steve Dickson <SteveD@RedHat.com> 
- Added pesudo flavors for nfsv4 mounts.
- Added BuildRequires: libselinux-devel and Requires: libselinux
  when WITH_SELINUX is set. 

* Fri Feb 27 2004 Dan Walsh <dwalsh@redhat.com> 2.12-5
- check for 2.6.3 kernel in mount options

* Mon Feb 23 2004 Elliot Lee <sopwith@redhat.com> 2.12-4
- Remove /bin/kill for #116100

* Fri Feb 20 2004 Dan Walsh <dwalsh@redhat.com> 2.12-3
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 12 2004 Elliot Lee <sopwith@redhat.com> 2.12-1
- Final 2.12 has been out for ages - might as well use it.

* Wed Jan 28 2004 Steve Dickson <SteveD@RedHat.com> 2.12pre-4
- Added mount patches that have NFS version 4 support

* Mon Jan 26 2004 Elliot Lee <sopwith@redhat.com> 2.12pre-3
- Provides: mount losetup

* Mon Jan 26 2004 Dan Walsh <dwalsh@redhat.com> 2.12pre-2
- Add multiple to /etc/pam.d/login for SELinux

* Thu Jan 15 2004 Elliot Lee <sopwith@redhat.com> 2.12pre-1
- 2.12pre-1
- Merge mount/losetup packages into the main package (#112324)
- Lose separate 

* Mon Nov 3 2003 Dan Walsh <dwalsh@redhat.com> 2.11y-35.sel
- remove selinux code from login and use pam_selinux

* Thu Oct 30 2003 Dan Walsh <dwalsh@redhat.com> 2.11y-34.sel
- turn on selinux

* Fri Oct 24 2003 Elliot Lee <sopwith@redhat.com> 2.11y-34
- Add BuildRequires: texinfo (from a bug# I don't remember)
- Fix #90588 with mountman patch142.

* Mon Oct 6 2003 Dan Walsh <dwalsh@redhat.com> 2.11y-33
- turn off selinux

* Thu Sep 25 2003 Dan Walsh <dwalsh@redhat.com> 2.11y-32.sel
- turn on selinux
- remove context selection

* Fri Sep 19 2003 Elliot Lee <sopwith@redhat.com> 2.11y-31
- Add patch140 (alldevs) to fix #101772. Printing the total size of
  all devices was deemed a lower priority than having all devices
  (e.g. /dev/ida/c0d9) displayed.

* Fri Sep 12 2003 Dan Walsh <dwalsh@redhat.com> 2.11y-31
- turn off selinux

* Fri Sep 12 2003 Dan Walsh <dwalsh@redhat.com> 2.11y-30.sel
- turn on selinux

* Fri Sep 5 2003 Elliot Lee <sopwith@redhat.com> 2.11y-28
- Fix #103004, #103954

* Fri Sep 5 2003 Dan Walsh <dwalsh@redhat.com> 2.11y-27
- turn off selinux

* Thu Sep 4 2003 Dan Walsh <dwalsh@redhat.com> 2.11y-26.sel
- build with selinux

* Mon Aug 11 2003 Elliot Lee <sopwith@redhat.com> 2.11y-25
- Use urandom instead for mkcramfs

* Tue Jul 29 2003 Dan Walsh <dwalsh@redhat.com> 2.11y-24
- add SELINUX 2.5 support

* Wed Jul 23 2003 Elliot Lee <sopwith@redhat.com> 2.11y-22
- #100433 patch

* Mon Jun 14 2003 Elliot Lee <sopwith@redhat.com> 2.11y-20
- #97381 patch

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Apr 21 2003 Elliot Lee <sopwith@redhat.com> 2.11y-17
- Change patch128 to improve ipcs -l

* Fri Apr 11 2003 Elliot Lee <sopwith@redhat.com> 2.11y-16
- Fix #85407

* Fri Apr 11 2003 Elliot Lee <sopwith@redhat.com> 2.11y-15
- Change patch128 to util-linux-2.11f-ipcs-84243-86285.patch to get all
ipcs fixes

* Thu Apr 10 2003 Matt Wilson <msw@redhat.com> 2.11y-14
- fix last login date display on AMD64 (#88574)

* Mon Apr  7 2003 Jeremy Katz <katzj@redhat.com> 2.11y-13
- include sfdisk on ppc

* Fri Mar 28 2003 Jeremy Katz <katzj@redhat.com> 2.11y-12
- add patch from msw to change mkcramfs blocksize with a command line option

* Tue Mar 25 2003 Phil Knirsch <pknirsch@redhat.com> 2.11y-11
- Fix segfault on s390x due to wrong usage of BLKGETSIZE.

* Thu Mar 13 2003 Elliot Lee <sopwith@redhat.com> 2.11y-10
- Really apply the ipcs patch. Doh.

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 19 2003 Elliot Lee <sopwith@redhat.com> 2.11y-8
- ipcs-84243.patch to fix #84243

* Thu Feb 13 2003 Yukihiro Nakai <ynakai@redhat.com> 2.11y-7
- Update moremisc patch to fix swprintf()'s minimum field (bug #83361).

* Mon Feb 03 2003 Elliot Lee <sopwith@redhat.com> 2.11y-6
- Fix mcookie segfault on many 64-bit architectures (bug #83345).

* Mon Feb 03 2003 Tim Waugh <twaugh@redhat.com> 2.11y-5
- Fix underlined multibyte characters (bug #83376).

* Sun Feb 02 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- rebuild to have again a s390 rpm
- disable some more apps for mainframe

* Wed Jan 29 2003 Elliot Lee <sopwith@redhat.com> 2.11y-4
- util-linux-2.11y-umask-82552.patch

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan 13 2003 Elliot Lee <sopwith@redhat.com> 2.11y-2
- Fix #81069, #75421

* Mon Jan 13 2003 Elliot Lee <sopwith@redhat.com> 2.11y-1
- Update to 2.11y
- Fix #80953
- Update patch0, patch107, patch117, patch120 for 2.11y
- Remove patch60, patch61, patch207, patch211, patch212, patch119, patch121
- Remove patch122, patch200

* Wed Oct 30 2002 Elliot Lee <sopwith@redhat.com> 2.11w-2
- Remove some crack/unnecessary patches while submitting stuff upstream.
- Build with -D_FILE_OFFSET_BITS=64

* Tue Oct 29 2002 Elliot Lee <sopwith@redhat.com> 2.11w-1
- Update to 2.11w, resolve patch conflicts

* Tue Oct 08 2002 Phil Knirsch <pknirsch@redhat.com> 2.11r-10hammer.3
- Extended util-linux-2.11b-s390x patch to work again.

* Thu Oct 03 2002 Elliot Lee <sopwith@redhat.com> 2.11r-10hammer.2
- Add patch122 for hwclock on x86_64

* Thu Sep 12 2002 Than Ngo <than@redhat.com> 2.11r-10hammer.1
- Fixed pam config files

* Wed Sep 11 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.11r-10hammer
- Port to hammer

* Fri Aug 30 2002 Elliot Lee <sopwith@redhat.com> 2.11r-10
- Patch120 (hwclock) to fix #72140
- Include isosize util

* Wed Aug 7 2002  Elliot Lee <sopwith@redhat.com> 2.11r-9
- Patch120 (skipraid2) to fix #70353, because the original patch was 
totally useless.

* Fri Aug 2 2002  Elliot Lee <sopwith@redhat.com> 2.11r-8
- Patch119 (fdisk-add-primary) from #67898

* Wed Jul 24 2002 Elliot Lee <sopwith@redhat.com> 2.11r-7
- Really add the gptsize patch, instead of what I think the patch says.
(+1)

* Tue Jul 23 2002 Elliot Lee <sopwith@redhat.com> 2.11r-6
- Add the sp[n].size part of the patch from #69603

* Mon Jul 22 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- adjust mainframe patches

* Tue Jul  2 2002 Bill Nottingham <notting@redhat.com> 2.11r-4
- only require usermode if we're shipping kbdrate here

* Fri Jun 28 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.11r-3
- Port the large swap patch to new util-linux... the off_t changes 
  now in main aren't sufficient

* Thu Jun 27 2002 Elliot Lee <sopwith@redhat.com> 2.11r-2
- Remove swapondetect (patch301) until it avoids possible false positives.

* Thu Jun 27 2002 Elliot Lee <sopwith@redhat.com> 2.11r-1
- Update to 2.11r, wheeee
- Remove unused patches

* Thu Jun 27 2002 Elliot Lee <sopwith@redhat.com> 2.11n-19
- Make a note here that this package was the source of the single change 
contained in util-linux-2.11f-18 (in 7.2/Alpha), and also contains the 
rawman patch from util-linux-2.11f-17.1 (in 2.1AS).
- Package has no runtime deps on slang, so remove the BuildRequires: 
slang-devel.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jun 20 2002 Elliot Lee <sopwith@redhat.com> 2.11n-17
- Fix teg's swapondetect patch to not print out the usage message when 
'swapon -a -e' is run. (#66690) (edit existing patch)
- Apply hjl's utmp handling patch (#66950) (patch116)
- Fix fdisk man page notes on IDE disk partition limit (#64013) (patch117)
- Fix mount.8 man page notes on vfat shortname option (#65628) (patch117)
- Fix possible cal overflow with widechars (#67090) (patch117)

* Tue Jun 11 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.11n-16
- support large swap partitions
- add '-d' option to autodetect available swap partitions

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May 15 2002 Elliot Lee <sopwith@redhat.com> 2.11n-14
- Remove kbdrate (again).

* Mon Apr 29 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- adjust mainframe patches to apply to current rpm
- do not include fdisk until it is fixed to work on mainframe

* Mon Apr 01 2002 Elliot Lee <sopwith@redhat.com> 2.11n-12
- Don't strip binaries - rpm does it for us.

* Sun Mar 31 2002 Elliot Lee <sopwith@redhat.com> 2.11n-11
- Apply patch115 from ejb@ql.org for bug #61868

* Wed Mar 27 2002 Elliot Lee <sopwith@redhat.com> 2.11n-10
- Finish fixing #60675 (ipcrm man page), updated the patch.
- Fix #61203 (patch114 - dumboctal.patch).

* Tue Mar 12 2002 Elliot Lee <sopwith@redhat.com> 2.11n-9
- Update ctty3 patch to ignore SIGHUP while dropping controlling terminal

* Fri Mar 08 2002 Elliot Lee <sopwith@redhat.com> 2.11n-8
- Update ctty3 patch to drop controlling terminal before forking.

* Fri Mar 08 2002 Elliot Lee <sopwith@redhat.com> 2.11n-7
  Fix various bugs:
- Add patch110 (skipraid) to properly skip devices that are part of a RAID array.
- Add patch111 (mkfsman) to update the mkfs man page's "SEE ALSO" section.
- remove README.cfdisk
- Include partx
- Fix 54741 and related bugs for good(hah!) with patch113 (ctty3)

* Wed Mar 06 2002 Elliot Lee <sopwith@redhat.com> 2.11n-6
- Put kbdrate in, add usermode dep.

* Tue Feb 26 2002 Elliot Lee <sopwith@redhat.com> 2.11n-5
- Fix #60363 (tweak raw.8 man page, make rawdevices.8 symlink).

* Tue Jan 28 2002 Bill Nottingham <notting@redhat.com> 2.11n-4
- remove kbdrate (fixes kbd conflict)

* Fri Dec 28 2001 Elliot Lee <sopwith@redhat.com> 2.11n-3
- Add util-linux-2.11n-ownerumount.patch (#56593)
- Add patch102 (util-linux-2.11n-colrm.patch) to fix #51887
- Fix #53452 nits.
- Fix #56953 (remove tunelp on s390)
- Fix #56459, and in addition switch to using sed instead of perl.
- Fix #58471
- Fix #57300
- Fix #37436
- Fix #32132

* Wed Dec 26 2001 Elliot Lee <sopwith@redhat.com> 2.11n-1
- Update to 2.11n
- Merge mount/losetup back in.

* Tue Dec 04 2001 Elliot Lee <sopwith@redhat.com> 2.11f-17
- Add patch38 (util-linux-2.11f-ctty2.patch) to ignore SIGINT/SIGTERM/SIGQUIT in the parent, so that ^\ won't break things.

* Fri Nov 09 2001 Elliot Lee <sopwith@redhat.com> 2.11f-16
- Merge patches 36, 75, 76, and 77 into patch #37, to attempt resolve all the remaining issues with #54741.

* Wed Oct 24 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add nologin man-page for s390/s390x

* Wed Oct 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.11f-14
- Don't build kbdrate on s390/s390x
- Don't make the pivot_root.8 man page executable(!)

* Tue Oct 23 2001 Elliot Lee <sopwith@redhat.com> 2.11f-13
- Patch/idea #76 from HJL, fixes bug #54741 (race condition in login 
acquisition of controlling terminal).

* Thu Oct 11 2001 Bill Nottingham <notting@redhat.com>
- fix permissions problem with vipw & shadow files, again (doh!)

* Tue Oct 09 2001 Erik Troan <ewt@redhat.com>
- added patch from Olaf Kirch to fix possible pwent structure overwriting

* Fri Sep 28 2001 Elliot Lee <sopwith@redhat.com> 2.11f-10
- fdisk patch from arjan

* Sun Aug 26 2001 Elliot Lee <sopwith@redhat.com> 2.11f-9
- Don't include cfdisk, since it appears to be an even bigger pile of junk than fdisk? :)

* Wed Aug  1 2001 Tim Powers <timp@redhat.com>
- don't require usermode

* Mon Jul 30 2001 Elliot Lee <sopwith@redhat.com> 2.11f-7
- Incorporate kbdrate back in.

* Mon Jul 30 2001 Bill Nottingham <notting@redhat.com>
- revert the patch that calls setsid() in login that we had reverted
  locally but got integrated upstream (#46223)

* Tue Jul 24 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- correct s390x patch

* Mon Jul 23 2001 Elliot Lee <sopwith@redhat.com>
- Add my megapatch (various bugs)
- Include pivot_root (#44828)

* Thu Jul 12 2001 Bill Nottingham <notting@redhat.com>
- make shadow files 0400, not 0600

* Wed Jul 11 2001 Bill Nottingham <notting@redhat.com>
- fix permissions problem with vipw & shadow files

* Mon Jun 18 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.11f, remove any merged patches
- add s390x patches for somewhat larger swap

* Thu Jun 14 2001 Erik Troan <ewt@redhat.com>
- added --verbose patch to mkcramfs; it's much quieter by default now

* Tue May 22 2001 Erik Troan <ewt@redhat.com>
- removed warning about starting partitions on cylinder 0 -- swap version2
  makes it unnecessary

* Wed May  9 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.11b-2
- Fix up s390x support

* Mon May  7 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.11b-1
- Fix up login for real (a console session should be the controlling tty)
  by reverting to 2.10s code (#36839, #36840, #39237)
- Add man page for agetty (#39287)
- 2.11b, while at it

* Fri Apr 27 2001 Preston Brown <pbrown@redhat.com> 2.11a-4
- /sbin/nologin from OpenBSD added.

* Fri Apr 20 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.11a-3
- Fix up login - exiting immediately even if the password is correct
  is not exactly a nice feature.
- Make definite plans to kill people who update login without checking
  if the new version works ;)

* Tue Apr 17 2001 Erik Troan <ewt@redhat.com>
- upgraded to 2.11a (kbdrate moved to kbd, among other things)
- turned off ALLOW_VCS_USE
- modified mkcramfs to not use a large number of file descriptors
- include mkfs.bfs

* Sun Apr  8 2001 Matt Wilson <msw@redhat.com>
- changed Requires: kernel >= 2.2.12-7 to Conflicts: kernel < 2.2.12-7
  (fixes a initscripts -> util-linux -> kernel -> initscripts prereq loop)

* Tue Mar 20 2001 Matt Wilson <msw@redhat.com>
- patched mkcramfs to use the PAGE_SIZE from asm/page.h instead of hard
  coding 4096 (fixes mkcramfs on alpha...)

* Mon Mar 19 2001 Matt Wilson <msw@redhat.com>
- added mkcramfs (from linux/scripts/mkcramfs)

* Mon Feb 26 2001 Tim Powers <timp@redhat.com>
- fixed bug #29131, where ipc.info didn't have an info dir entry,
  added the dir entry to ipc.texi (Patch58)

* Fri Feb 23 2001 Preston Brown <pbrown@redhat.com>
- use lang finder script
- install info files

* Thu Feb 08 2001 Erik Troan <ewt@redhat.com>
- reverted login patch; seems to cause problems
- added agetty

* Wed Feb 07 2001 Erik Troan <ewt@redhat.com>
- updated kill man page
- added patch to fix vipw race
- updated vipw to edit /etc/shadow and /etc/gshadow, if appropriate
- added patch to disassociate login from tty, session, and pgrp

* Tue Feb 06 2001 Erik Troan <ewt@redhat.com>
- fixed problem w/ empty extended partitions
- added patch to fix the date in the more man page
- set OPT to pass optimization flags to make rather then RPM_OPT_FLAG
- fixed fdisk -l /Proc/partitions parsing
- updated to 2.10s

* Tue Jan 23 2001 Preston Brown <pbrown@redhat.com>
- danish translations added

* Mon Jan 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix segfault in login in btmp patch (#24025)

* Mon Dec 11 2000 Oliver Paukstadt <oliver.paukstadt@millenux.com>
- ported to s390

* Wed Nov 01 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.10p
- update patch37 to newer fdisk version

* Mon Oct  9 2000 Jeff Johnson <jbj@redhat.com>
- update to 2.10o
-  fdformat: fixed to work with kernel 2.4.0test6 (Marek Wojtowicz)
-  login: not installed suid
-  getopt: by default install aux files in /usr/share/misc
- update to 2.10n:
-  added blockdev.8
-  change to elvtune (andrea)
-  fixed overrun in agetty (vii@penguinpowered.com)
-  shutdown: prefer umounting by mount point (rgooch)
-  fdisk: added plan9
-  fdisk: remove empty links in chain of extended partitions
-  hwclock: handle both /dev/rtc and /dev/efirtc (Bill Nottingham)
-  script: added -f (flush) option (Ivan Schreter)
-  script: added -q (quiet) option (Per Andreas Buer)
-  getopt: updated to version 1.1.0 (Frodo Looijaard)
-  Czech messages (Jiri Pavlovsky)
- login.1 man page had not /var/spool/mail path (#16998).
- sln.8 man page (but not executable) included (#10601).
- teach fdisk 0xde(Dell), 0xee(EFI GPT), 0xef(EFI FAT) partitions (#17610).

* Wed Aug 30 2000 Matt Wilson <msw@redhat.com>
- rebuild to cope with glibc locale binary incompatibility, again

* Mon Aug 14 2000 Jeff Johnson <jbj@redhat.com>
- setfdprm should open with O_WRONLY, not 3.

* Fri Aug 11 2000 Jeff Johnson <jbj@redhat.com>
- fdformat should open with O_WRONLY, not 3.

* Fri Jul 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- make 'look' look in /usr/share/dict

* Fri Jul 21 2000 Bill Nottingham <notting@redhat.com>
- put /usr/local/sbin:/usr/local/bin in root's path

* Wed Jul 19 2000 Jakub Jelinek <jakub@redhat.com>
- rebuild to cope with glibc locale binary incompatibility

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Bill Nottingham <notting@redhat.com>
- enable hwclock to use /dev/efirtc on ia64 (gettext is fun. :( )

* Mon Jul  3 2000 Bill Nottingham <notting@redhat.com>
- move cfdisk to /usr/sbin, it depends on /usr stuff
- add rescuept

* Fri Jun 23 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- point more at the correct path to vi (for "v"), Bug #10882

* Sun Jun  4 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging changes.

* Thu Jun  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- modify PAM setup to use system-auth

* Mon May  1 2000 Bill Nottingham <notting@redhat.com>
- eek, where did login go? (specfile tweaks)

* Mon Apr 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.10k
- fix compilation with current glibc

* Tue Mar 21 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.10h

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Sat Mar  4 2000 Matt Wilson <msw@redhat.com>
- use snprintf - not sprintf - when doing
  sprintf ("%s\n", _("Some string")) to avoid overflows and
  segfaults.

* Mon Feb 21 2000 Jeff Johnson <jbj@redhat.com>
- raw control file was /dev/raw, now /dev/rawctl.
- raw access files were /dev/raw*, now /dev/raw/raw*.

* Thu Feb 17 2000 Erik Troan <ewt@redhat.com>
- -v argument to mkswap wasn't working

* Thu Feb 10 2000 Jakub Jelinek <jakub@redhat.com>
- Recognize 0xfd on Sun disklabels as RAID

* Tue Feb  8 2000 Bill Nottingham <notting@redhat.com>
- more lives in /bin, and was linked against /usr/lib/libnurses. Bad.

* Thu Feb 03 2000 Jakub Jelinek <jakub@redhat.com>
- update to 2.10f
- fix issues in the new realpath code, avoid leaking memory

* Tue Feb 01 2000 Cristian Gafton <gafton@redhat.com>
- rebuild to fix dependencies
- add NFSv3 patches

* Fri Jan 28 2000 Bill Nottingham <notting@redhat.com>
- don't require csh

* Mon Jan 24 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.10e
- add rename

* Thu Jan 20 2000 Jeff Johnson <jbj@redhat.com>
- strip newlines in logger input.

* Mon Jan 10 2000 Jeff Johnson <jbj@redhat.com>
- rebuild with correct ncurses libs.

* Tue Dec  7 1999 Matt Wilson <msw@redhat.com>
- updated to util-linux 2.10c
- deprecated IMAP login mail notification patch17
- deprecated raw patch22
- depricated readprofile patch24

* Tue Dec  7 1999 Bill Nottingham <notting@redhat.com>
- add patch for readprofile

* Thu Nov 18 1999 Michael K. Johnson <johnsonm@redhat.com>
- tunelp should come from util-linux

* Tue Nov  9 1999 Jakub Jelinek <jakub@redhat.com>
- kbdrate cannot use /dev/port on sparc.

* Wed Nov  3 1999 Jakub Jelinek <jakub@redhat.com>
- fix kbdrate on sparc.

* Wed Oct 27 1999 Bill Nottingham <notting@redhat.com>
- ship hwclock on alpha.

* Tue Oct  5 1999 Bill Nottingham <notting@redhat.com>
- don't ship symlinks to rdev if we don't ship rdev.

* Tue Sep 07 1999 Cristian Gafton <gafton@redhat.com>
- add rawIO support from sct

* Mon Aug 30 1999 Preston Brown <pbrown@redhat.com>
- don't display "new mail" message when the only piece of mail is from IMAP

* Fri Aug 27 1999 Michael K. Johnson <johnsonm@redhat.com>
- kbdrate is now a console program

* Thu Aug 26 1999 Jeff Johnson <jbj@redhat.com>
- hostid is now in sh-utils. On sparc, install hostid as sunhostid (#4581).
- update to 2.9w:
-  Updated mount.8 (Yann Droneaud)
-  Improved makefiles
-  Fixed flaw in fdisk

* Tue Aug 10 1999 Jeff Johnson <jbj@redhat.com>
- tsort is now in textutils.

* Wed Aug  4 1999 Bill Nottingham <notting@redhat.com>
- turn off setuid bit on login. Again. :(

* Tue Aug  3 1999 Peter Jones, <pjones@redhat.com>
- hostid script for sparc (#3803).

* Tue Aug 03 1999 Christian 'Dr. Disk' Hechelmann <drdisk@tc-gruppe.de>
- added locale message catalogs to %file
- added patch for non-root build
- vigr.8 and /usr/lib/getopt  man-page was missing from file list
- /etc/fdprm really is a config file

* Fri Jul 23 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.9v:
-   cfdisk no longer believes the kernel's HDGETGEO
    (and may be able to partition a 2 TB disk)

* Fri Jul 16 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.9u:
-   Czech more.help and messages (Jiøí Pavlovský)
-   Japanese messages (Daisuke Yamashita)
-   fdisk fix (Klaus G. Wagner)
-   mount fix (Hirokazu Takahashi)
-   agetty: enable hardware flow control (Thorsten Kranzkowski)
-   minor cfdisk improvements
-   fdisk no longer accepts a default device
-   Makefile fix

* Tue Jul  6 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.9t:
-   national language support for hwclock
-   Japanese messages (both by Daisuke Yamashita)
-   German messages and some misc i18n fixes (Elrond)
-   Czech messages (Jiøí Pavlovský)
-   wall fixed for /dev/pts/xx ttys
-   make last and wall use getutent() (Sascha Schumann)
    [Maybe this is bad: last reading all of wtmp may be too slow.
     Revert in case people complain.]
-   documented UUID= and LABEL= in fstab.5
-   added some partition types
-   swapon: warn only if verbose

* Fri Jun 25 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.9s.

* Sat May 29 1999 Jeff Johnson <jbj@redhat.com>
- fix mkswap sets incorrect bits on sparc64 (#3140).

* Thu Apr 15 1999 Jeff Johnson <jbj@redhat.com>
- on sparc64 random ioctls on clock interface cause kernel messages.

* Thu Apr 15 1999 Jeff Johnson <jbj@redhat.com>
- improved raid patch (H.J. Lu).

* Wed Apr 14 1999 Michael K. Johnson <johnsonm@redhat.com>
- added patch for smartraid controllers

* Sat Apr 10 1999 Cristian Gafton <gafton@redhat.com>
- fix logging problems caused by setproctitle and PAM interaction
  (#2045)

* Wed Mar 31 1999 Jeff Johnson <jbj@redhat.com>
- include docs and examples for sfdisk (#1164)

* Mon Mar 29 1999 Matt Wilson <msw@redhat.com>
- rtc is not working properly on alpha, we can't use hwclock yet.

* Fri Mar 26 1999 Cristian Gafton <gafton@redhat.com>
- add patch to make mkswap more 64 bit friendly... Patch from
  eranian@hpl.hp.com (ahem!)

* Thu Mar 25 1999 Jeff Johnson <jbj@redhat.com>
- include sfdisk (#1164)
- fix write (#1784)
- use positive logic in spec file (%ifarch rather than %ifnarch).
- (re)-use 1st matching utmp slot if search by mypid not found.
- update to 2.9o
- lastb wants bad logins in wtmp clone /var/run/btmp (#884)

* Thu Mar 25 1999 Jakub Jelinek <jj@ultra.linux.cz>
- if hwclock is to be compiled on sparc,
  it must actually work. Also, it should obsolete
  clock, otherwise it clashes.
- limit the swap size in mkswap for 2.2.1+ kernels
  by the actual maximum size kernel can handle.
- fix kbdrate on sparc, patch by J. S. Connell
  <ankh@canuck.gen.nz>

* Wed Mar 24 1999 Matt Wilson <msw@redhat.com>
- added pam_console back into pam.d/login

* Tue Mar 23 1999 Matt Wilson <msw@redhat.com>
- updated to 2.9i
- added hwclock for sparcs and alpha

* Mon Mar 22 1999 Erik Troan <ewt@redhat.com>
- added vigr to file list

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 12)

* Thu Mar 18 1999 Cristian Gafton <gafton@redhat.com>
- remove most of the ifnarch arm stuff

* Mon Mar 15 1999 Michael Johnson <johnsonm@redhat.com>
- added pam_console.so to /etc/pam.d/login

* Thu Feb  4 1999 Michael K. Johnson <johnsonm@redhat.com>
- .perms patch to login to make it retain root in parent process
  for pam_close_session to work correctly

* Tue Jan 12 1999 Jeff Johnson <jbj@redhat.com>
- strip fdisk in buildroot correctly (#718)

* Mon Jan 11 1999 Cristian Gafton <gafton@redhat.com>
- have fdisk compiled on sparc and arm

* Mon Jan 11 1999 Erik Troan <ewt@redhat.com>
- added beos partition type to fdisk

* Wed Dec 30 1998 Cristian Gafton <gafton@redhat.com>
- incorporate fdisk on all arches

* Sat Dec  5 1998 Jeff Johnson <jbj@redhat.com>
- restore PAM functionality at end of login (Bug #201)

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- patch top build on the arm without PAM and related utilities, for now.
- build hwclock only on intel

* Wed Nov 18 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to version 2.9

* Thu Oct 29 1998 Bill Nottingham <notting@redhat.com>
- build for Raw Hide (slang-1.2.2)
- patch kbdrate wackiness so it builds with egcs

* Tue Oct 13 1998 Erik Troan <ewt@redhat.com>
- patched more to use termcap

* Mon Oct 12 1998 Erik Troan <ewt@redhat.com>
- added warning about alpha/bsd label starting cylinder

* Mon Sep 21 1998 Erik Troan <ewt@redhat.com>
- use sigsetjmp/siglongjmp in more rather then sig'less versions

* Fri Sep 11 1998 Jeff Johnson <jbj@redhat.com>
- explicit attrs for setuid/setgid programs

* Thu Aug 27 1998 Cristian Gafton <gafton@redhat.com>
- sln is now included in glibc

* Sun Aug 23 1998 Jeff Johnson <jbj@redhat.com>
- add cbm1581 floppy definitions (problem #787)

* Mon Jun 29 1998 Jeff Johnson <jbj@redhat.com>
- remove /etc/nologin at end of shutdown/halt.

* Fri Jun 19 1998 Jeff Johnson <jbj@redhat.com>
- add mount/losetup.

* Thu Jun 18 1998 Jeff Johnson <jbj@redhat.com>
- update to 2.8 with 2.8b clean up. hostid now defunct?

* Mon Jun 01 1998 David S. Miller <davem@dm.cobaltmicro.com>
- "more" now works properly on sparc

* Sat May 02 1998 Jeff Johnson <jbj@redhat.com>
- Fix "fdisk -l" fault on mounted cdrom. (prob #513)

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat Apr 11 1998 Cristian Gafton <gafton@redhat.com>
- manhattan rebuild

* Mon Dec 29 1997 Erik Troan <ewt@redhat.com>
- more didn't suspend properly on glibc
- use proper tc*() calls rather then ioctl's

* Sun Dec 21 1997 Cristian Gafton <gafton@redhat.com>
- fixed a security problem in chfn and chsh accepting too 
  long gecos fields

* Fri Dec 19 1997 Mike Wangsmo <wanger@redhat.com>
- removed "." from default path

* Tue Dec 02 1997 Cristian Gafton <gafton@redhat.com>
- added (again) the vipw patch

* Wed Oct 22 1997 Michael Fulbright <msf@redhat.com>
- minor cleanups for glibc 2.1

* Fri Oct 17 1997 Michael Fulbright <msf@redhat.com>
- added vfat32 filesystem type to list recognized by fdisk

* Fri Oct 10 1997 Erik Troan <ewt@redhat.com>
- don't build clock on the alpha 
- don't install chkdupexe

* Thu Oct 02 1997 Michael K. Johnson <johnsonm@redhat.com>
- Update to new pam standard.
- BuildRoot.

* Thu Sep 25 1997 Cristian Gafton <gafton@redhat.com>
- added rootok and setproctitle patches
- updated pam config files for chfn and chsh

* Tue Sep 02 1997 Erik Troan <ewt@redhat.com>
- updated MCONFIG to automatically determine the architecture
- added glibc header hacks to fdisk code
- rdev is only available on the intel

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
- update to util-linux 2.7, fixed login problems

* Wed Jun 25 1997 Erik Troan <ewt@redhat.com>
- Merged Red Hat changes into main util-linux source, updated package to
  development util-linux (nearly 2.7).

* Tue Apr 22 1997 Michael K. Johnson <johnsonm@redhat.com>
- LOG_AUTH --> LOG_AUTHPRIV in login and shutdown

* Mon Mar 03 1997 Michael K. Johnson <johnsonm@redhat.com>
- Moved to new pam and from pam.conf to pam.d

* Tue Feb 25 1997 Michael K. Johnson <johnsonm@redhat.com>
- pam.patch differentiated between different kinds of bad logins.
  In particular, "user does not exist" and "bad password" were treated
  differently.  This was a minor security hole.
