# Upstream maintainer util-linux@math.uio.no

%define with_kbdrate 0

Summary: A collection of basic system utilities.
Name: util-linux
Version: 2.11r
Release: 9
License: distributable
Group: System Environment/Base

BuildRequires: sed
BuildRequires: pam-devel
BuildRequires: ncurses-devel
BuildRequires: libtermcap-devel
BuildRequires: zlib-devel

Source0: ftp://ftp.kernel.org/pub/linux/utils/util-linux/util-linux-%{version}.tar.gz
Source1: util-linux-2.7-login.pamd
Source2: util-linux-2.7-chfn.pamd
Source3: util-linux-2.7-chsh.pamd
Source6: mkcramfs.c
Source7: cramfs.h
Source8: nologin.c
Source9: nologin.8
Source10: kbdrate.tar.gz

Patch0: util-linux-2.11a-rhconfig.patch
Patch1: util-linux-2.11r-nochkdupexe.patch
Patch2: util-linux-2.11a-gecossize.patch

Patch4: util-linux-2.11n-mount.patch

Patch21: util-linux-2.9v-nonroot.patch

Patch27: util-linux-2.11r-moretc.patch

Patch35: util-linux-2.10m-loginpath.patch
Patch60: util-linux-2.10s-s390x.patch
Patch61: util-linux-2.11b-s390x.patch

Patch70: util-linux-2.11r-miscfixes.patch

Patch100: mkcramfs.patch
Patch101: mkcramfs-quiet.patch

########
# Mount patches
Patch201: mount-2.10m-nolock-docs.patch
Patch202: mount-2.10o-nfsman.patch
Patch204: mount-2.10r-2gb.patch
Patch206: mount-2.10r-kudzu.patch
Patch207: mount-2.11r-swapon.patch
Patch209: mount-2.11b-swapoff.patch
Patch210: util-linux-2.11b-largefile.patch
Patch211: mount-2.11e-user_label_umount.patch
Patch212: mount-2.11r-netdev.patch
Patch220: util-linux-2.11n-makej.patch

########### START UNSUBMITTED
Patch103: util-linux-2.11r-ownerumount.patch
Patch106: util-linux-2.11g-swaponsymlink-57300.patch
Patch107: util-linux-2.11r-procpartitions-37436.patch
Patch108: util-linux-2.11n-autosmb-32132.patch
Patch109: util-linux-2.11f-rawman.patch
Patch111: util-linux-2.11n-mkfsman.patch
Patch113: util-linux-2.11r-ctty3.patch
Patch114: util-linux-2.11n-dumboctal.patch
Patch115: util-linux-2.11n-fstabperm-61868.patch
Patch116: util-linux-2.11n-loginutmp-66950.patch
Patch117: util-linux-2.11r-moremisc.patch
Patch300: util-linux-2.11n-ia64mkswap.patch
Patch301: util-linux-2.11r-swapondetect.patch
Patch302: util-linux-2.11r-largeswap.patch

Patch118: util-linux-2.11r-gptsize-69603.patch
Patch119: fdisk-add-primary.patch

Patch120: util-linux-2.11r-skipraid2.patch
########### END UNSUBMITTED

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

%description
The util-linux package contains a large variety of low-level system
utilities that are necessary for a Linux system to function. Among
others, Util-linux contains the fdisk configuration tool and the login
program.

%package -n mount
Group: System Environment/Base
Summary: Programs for mounting and unmounting filesystems.
ExclusiveOS: Linux
Prereq: mktemp /bin/awk /usr/bin/cmp textutils fileutils

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

%prep

%setup -q -a 10

%patch0 -p1 -b .rhconfig

# We don't want the 'chkdupexe' program installed
%patch1 -p1 -b .nochkdupexe

%patch2 -p1 -b .gecos

# mount comes from its own rpm (again)
%patch4 -p1 -b .mount
%patch21 -p1 -b .nonroot

# Link 'more' against libtermcap instead of ncurses because ncurses
# is under /usr and won't be accessable if / is mounted but /usr is not
%patch27 -p1 -b .moretc

%patch35 -p1 -b .loginpath

%ifarch s390 s390x
%patch60 -p1 -b .s390x2
%patch61 -p1 -b .s390x
%endif

# No support for large numbers of cylinders in fdisk{sgi,sun}label.*
# Too many places in those files assume that it is an unsigned short,
# not worth fixing.
%patch70 -p1 -b .miscfixes

# mkcramfs
cp %{SOURCE7} %{SOURCE6} .
%patch100 -p1 -b .mkcramfs
%patch101 -p1 -b .quiet

# nologin
cp %{SOURCE8} %{SOURCE9} .

%patch201 -p1 -b .docbug
%patch202 -p1 -b .nfsman
%patch204 -p1 -b .2gb
%patch206 -p1 -b .kudzu
%patch207 -p1 -b .swapon
%patch209 -p2 -b .swapoff
%patch210 -p1 -b .largefile
%patch211 -p2 -b .userumount
%patch212 -p1 -b .netdev
%patch220 -p1 -b .makej

sed -e 's:^MAN_DIR=.*:MAN_DIR=%{_mandir}:' -e 's:^INFO_DIR=.*:INFO_DIR=%{_infodir}:' MCONFIG > MCONFIG.new
mv MCONFIG.new MCONFIG

%patch103 -p1 -b .ownerumount
%patch106 -p1 -b .swaponsymlink
%patch107 -p1 -b .procpartitions
%patch108 -p1 -b .autosmb
%patch109 -p1 -b .rawman
%patch111 -p1 -b .mkfsman

%patch113 -p1 -b .ctty3
%patch114 -p1 -b .dumboctal
%patch115 -p1 -b .fstabperm
%patch116 -p1 -b .loginutmp
%patch117 -p1 -b .moremisc
%patch118 -p1 -b .gptsize
cd fdisk
%patch119 -p0 -b .addprimary
cd ..
%patch120 -p1 -b .sopwith

# All of this patch is in except a 'max swap size' change, which
# doesn't seem to be needed
#%patch300 -p1 -b .offtmkswap
#%patch301 -p1 -b .detectswap
%patch302 -p1 -b .largeswap

%build
unset LINGUAS || :

%configure

make "OPT=$RPM_OPT_FLAGS -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE" \
	LDFLAGS="" \
	HAVE_PIVOT_ROOT=yes \
	%{?_smp_mflags}
make LDFLAGS="" CFLAGS="$RPM_OPT_FLAGS" -C partx %{?_smp_mflags}
cd rescuept
cc $RPM_OPT_FLAGS -o rescuept rescuept.c
cd ..

%if %{with_kbdrate}
pushd kbdrate
    cc $RPM_OPT_FLAGS -o kbdrate kbdrate.c
popd
%endif

gcc $RPM_OPT_FLAGS -o mkcramfs mkcramfs.c -I. -lz

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
        INSTALLDIR="install -d -m 755" \
        INSTALLSUID="install -m 755" \
        INSTALLBIN="install -m 755" \
        INSTALLMAN="install -m 644" \
	install DESTDIR=${RPM_BUILD_ROOT}

install -m 755 mount/pivot_root ${RPM_BUILD_ROOT}/sbin
install -m 644 mount/pivot_root.8 ${RPM_BUILD_ROOT}%{_mandir}/man8
install -m 755 rescuept/rescuept ${RPM_BUILD_ROOT}/sbin
mv rescuept/README rescuept/README.rescuept
install -m 755 mkcramfs ${RPM_BUILD_ROOT}/usr/bin
install -m 755 nologin ${RPM_BUILD_ROOT}/sbin
install -m 644 nologin.8 ${RPM_BUILD_ROOT}%{_mandir}/man8
%if %{with_kbdrate}
install -m 555 kbdrate/kbdrate ${RPM_BUILD_ROOT}/sbin
install -m 644 kbdrate/kbdrate.8 ${RPM_BUILD_ROOT}%{_mandir}/man8
ln -s consolehelper ${RPM_BUILD_ROOT}/usr/bin/kbdrate
%endif
echo '.so man8/raw.8' > $RPM_BUILD_ROOT%{_mandir}/man8/rawdevices.8

install -m 555 partx/{addpart,delpart,partx} $RPM_BUILD_ROOT/sbin

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
  install -m 644 ${RPM_SOURCE_DIR}/util-linux-2.7-login.pamd ./login
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
%doc */README.*

/bin/arch
/bin/dmesg
/bin/kill
%attr(755,root,root)	/bin/login
/bin/more

%config %{_sysconfdir}/fdprm
%config %{_sysconfdir}/pam.d/chfn
%config %{_sysconfdir}/pam.d/chsh
%config %{_sysconfdir}/pam.d/login

/sbin/agetty
/sbin/blockdev
/sbin/pivot_root
%ifnarch s390 s390x
/sbin/clock
/sbin/fdisk
%endif
/sbin/ctrlaltdel
/sbin/elvtune
/sbin/addpart
/sbin/delpart
/sbin/partx

%ifarch %{ix86} alpha ia64 s390 s390x
/sbin/fsck.minix
/sbin/mkfs.minix
/sbin/mkfs.bfs
%{_mandir}/man8/fsck.minix.8*
%{_mandir}/man8/mkfs.minix.8*
%{_mandir}/man8/mkfs.bfs.8*
/sbin/sfdisk
%{_mandir}/man8/sfdisk.8*
%doc fdisk/sfdisk.examples
%endif

%ifnarch s390 s390x
/sbin/hwclock
/usr/sbin/hwclock
%endif
/sbin/mkfs
/sbin/mkswap
#/sbin/mkfs.bfs
/sbin/rescuept
#/sbin/sln
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
%ifarch %{ix86} alpha armv4l
%{_bindir}/cytune
%{_mandir}/man8/cytune.8*
%endif
%{_bindir}/ddate
%{_bindir}/fdformat
%{_bindir}/getopt
%{_bindir}/hexdump
%{_bindir}/ipcrm
%{_bindir}/ipcs
%{_bindir}/logger
%{_bindir}/look
%{_bindir}/mcookie
%{_bindir}/mkcramfs
%{_bindir}/namei
%attr(4711,root,root)	%{_bindir}/newgrp
%{_bindir}/raw
%{_bindir}/rename
%{_bindir}/renice
%{_bindir}/rev
%{_bindir}/script
%{_bindir}/setfdprm
%{_bindir}/setsid
%{_bindir}/setterm
%ifarch sparc sparc64 sparcv9
%{_bindir}/sunhostid
%endif
#%{_bindir}/tsort
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
%ifnarch s390
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
#%{_mandir}/man1/hostid.1*
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
#%{_mandir}/man1/tsort.1*
%{_mandir}/man1/ul.1*
%{_mandir}/man1/whereis.1*
%{_mandir}/man1/write.1*

%{_mandir}/man8/agetty.8*
%{_mandir}/man8/blockdev.8*
%{_mandir}/man8/ctrlaltdel.8*
%{_mandir}/man8/dmesg.8*
%{_mandir}/man8/elvtune.8*
%{_mandir}/man8/fdformat.8*
%ifnarch s390 s390x
%{_mandir}/man8/fdisk.8*
%{_mandir}/man8/hwclock.8*
%endif
%{_mandir}/man8/ipcrm.8*
%{_mandir}/man8/ipcs.8*
%{_mandir}/man8/mkfs.8*
#%{_mandir}/man8/mkfs.bfs.8*
%{_mandir}/man8/mkswap.8*
%{_mandir}/man8/pivot_root.8*
%{_mandir}/man8/raw.8*
%{_mandir}/man8/rawdevices.8*
%{_mandir}/man8/renice.8*
%{_mandir}/man8/setfdprm.8*
%{_mandir}/man8/setsid.8*
# XXX this man page should be moved to glibc.
%{_mandir}/man8/sln.8*
%{_mandir}/man8/tunelp.8*
%{_mandir}/man8/vigr.8*
%{_mandir}/man8/vipw.8*

%{_datadir}/misc/getopt
%{_datadir}/misc/more.help

%files -n mount
%defattr(-,root,root)
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

%files -n losetup
%defattr(-,root,root)
%{_mandir}/man8/losetup.8*
/sbin/losetup

%changelog
* Wed Aug 7 2002  Elliot Lee <sopwith@redhat.com> 2.11r-9
- Patch120 (skiproot2) to fix #70353, because the original patch was 
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
