Summary: A collection of basic system utilities.
Name: util-linux
Version: 2.10s
Release: 13.7
Copyright: distributable
Group: System Environment/Base
Source0: ftp://ftp.kernel.org/pub/linux/utils/util-linux/util-linux-%{version}.tar.gz
Source1: util-linux-2.7-login.pamd
Source2: util-linux-2.7-chfn.pamd
Source3: util-linux-2.7-chsh.pamd
Source4: util-linux-2.9w-kbdrate.pamd
Source5: util-linux-2.9w-kbdrate.apps
Source6: mkcramfs.c
Source7: cramfs.h

Patch0: util-linux-2.10o-rhconfig.patch
Patch1: util-linux-2.10e-nochkdupexe.patch
Patch2: util-linux-2.10m-gecos.patch
# XXX apply next patch to enable mount-2.8 from util-linux (not applied)
Patch4: util-linux-2.9i-mount.patch
Patch6: util-linux-2.9i-fdiskwarning.patch
Patch8: util-linux-2.9i-nomount.patch
Patch11: util-linux-2.10p-btmp.patch
Patch21: util-linux-2.9v-nonroot.patch
Patch23: util-linux-2.9w-kbdrate.patch
Patch27: util-linux-2.10f-moretc.patch
Patch28: util-linux-2.10k-sparcraid.patch
Patch31: util-linux-2.10k-overflow.patch
Patch32: util-linux-2.10k-glibc.patch
Patch35: util-linux-2.10m-loginpath.patch
Patch36: util-linux-2.10m-dict.patch
Patch37: util-linux-2.10m-fdisk-efi-dell.patch
Patch50: util-linux-2.10m-s390.patch
Patch51: util-linux-2.10p-extended.patch
Patch52: util-linux-2.10p-moremandate.patch
Patch53: util-linux-2.10p-fdisk-l.patch
Patch54: util-linux-2.10s-vipwrace.patch
Patch55: util-linux-2.10s-killman.patch
Patch56: util-linux-2.10s-vipwshadow.patch
Patch57: util-linux-2.10s-logingrp.patch
Patch58: util-linux-2.10s-ipc-info.patch
Patch59: util-linux-2.10s-swapon.patch

Obsoletes: fdisk tunelp
%ifarch alpha sparc sparc64 sparcv9 s390
Obsoletes: clock
%endif
%ifarch alpha
Conflicts: initscripts <= 4.58, timeconfig <= 3.0.1
%endif
BuildRoot: %{_tmppath}/%{name}-root
Requires: pam >= 0.66-4, /etc/pam.d/system-auth
Conflicts: kernel < 2.2.12-7, 
Prereq: /sbin/install-info

%description
The util-linux package contains a large variety of low-level system
utilities that are necessary for a Linux system to function.  Among
many features, Util-linux contains the fdisk configuration tool and
the login program.

%prep

%setup -q

%patch0 -p1 -b .rhconfig
%patch1 -p1 -b .nochkdupexe
%patch2 -p1 -b .gecos

# mount comes from its own rpm (again)
#%patch4 -p1 -b .mount

%patch6 -p1 -b .fdiskwarning
%patch8 -p1 -b .nomount
%patch11 -p1 -b .btmp
%patch21 -p1 -b .nonroot
%patch23 -p1 -b .kbdrate

%patch27 -p1 -b .moretc
%patch28 -p1 -b .sparcraid

%patch31 -p1 -b .overflow

%patch32 -p1 -b .nonx86

%patch35 -p1 -b .loginpath
%patch36 -p1 -b .dict
%patch37 -p1 -b .bug17610

%patch50 -p1 -b .s390

%patch51 -p1 -b .extendedfix
%patch52 -p1 -b .moreman
%patch53 -p1 -b .fdisk-l
%patch54 -p1 -b .vipwrace
%patch55 -p1 -b .killman
%patch56 -p1 -b .vipwshadow
#%patch57 -p1 -b .logingrp
%patch58 -p1 -b .dirinfo
%patch59 -p1 -b .swapon

%build
unset LINGUAS || :

%configure
make "OPT=$RPM_OPT_FLAGS -g" 
cd rescuept
gcc $RPM_OPT_FLAGS -o rescuept rescuept.c
cd ..

cp %{SOURCE7} .
gcc $RPM_OPT_FLAGS -o mkcramfs %{SOURCE6} -I. -lz

pushd sys-utils
    makeinfo --number-sections ipc.texi
popd

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/{bin,sbin}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_infodir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man{1,6,8}
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}

make install DESTDIR=${RPM_BUILD_ROOT}

install -m 755 rescuept/rescuept ${RPM_BUILD_ROOT}/sbin
install -m 755 mkcramfs ${RPM_BUILD_ROOT}/usr/bin

if [ "%{_mandir}" != "%{_prefix}/man" -a -d ${RPM_BUILD_ROOT}%{_prefix}/man ]; then
   ( cd ${RPM_BUILD_ROOT}%{_prefix}/man; tar cf - ./* ) |
   ( cd ${RPM_BUILD_ROOT}%{_mandir}; tar xf - )
   ( cd ${RPM_BUILD_ROOT}%{_prefix}; rm -rf ./man )
fi

# Correct mail spool path.
perl -pi -e 's,/usr/spool/mail,/var/spool/mail,' ${RPM_BUILD_ROOT}%{_mandir}/man1/login.1

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

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/pam.d
{ 
  pushd ${RPM_BUILD_ROOT}%{_sysconfdir}/pam.d
  install -m 644 ${RPM_SOURCE_DIR}/util-linux-2.7-login.pamd ./login
  install -m 644 ${RPM_SOURCE_DIR}/util-linux-2.7-chsh.pamd ./chsh
  install -m 644 ${RPM_SOURCE_DIR}/util-linux-2.7-chsh.pamd ./chfn
  install -m 644 ${RPM_SOURCE_DIR}/util-linux-2.9w-kbdrate.pamd ./kbdrate
  popd
}

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/security/console.apps
{ pushd ${RPM_BUILD_ROOT}%{_sysconfdir}/security/console.apps
  install -m 644 ${RPM_SOURCE_DIR}/util-linux-2.9w-kbdrate.apps ./kbdrate
  popd
}

ln -sf consolehelper ${RPM_BUILD_ROOT}%{_bindir}/kbdrate

ln -sf hwclock ${RPM_BUILD_ROOT}/sbin/clock

# We do not want dependencies on csh
chmod 644 ${RPM_BUILD_ROOT}%{_datadir}/misc/getopt/*

# This has dependencies on stuff in /usr
%ifnarch sparc sparc64 sparcv9
mv ${RPM_BUILD_ROOT}/sbin/cfdisk ${RPM_BUILD_ROOT}/usr/sbin
%endif

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
%config %{_sysconfdir}/pam.d/kbdrate
%config %{_sysconfdir}/pam.d/login
%config %{_sysconfdir}/security/console.apps/kbdrate

/sbin/agetty
/sbin/blockdev
/sbin/clock
/sbin/ctrlaltdel
/sbin/elvtune
/sbin/fdisk

%ifarch %{ix86} alpha ia64
/sbin/fsck.minix
/sbin/mkfs.minix
%{_mandir}/man8/fsck.minix.8*
%{_mandir}/man8/mkfs.minix.8*
/sbin/sfdisk
%{_mandir}/man8/sfdisk.8*
%doc fdisk/sfdisk.examples
%endif

/sbin/hwclock
/sbin/kbdrate
/sbin/mkfs
/sbin/mkswap
#/sbin/mkfs.bfs
/sbin/rescuept
#/sbin/sln

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
%{_bindir}/kbdrate
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

%{_prefix}/games/banner

%ifnarch sparc sparc64 sparcv9
%{_sbindir}/cfdisk
%{_mandir}/man8/cfdisk.8*
%endif
%ifarch %{ix86}
%{_sbindir}/rdev
%{_sbindir}/ramsize
%{_sbindir}/rootflags
%{_sbindir}/swapdev
%{_sbindir}/vidmode
%{_mandir}/man8/rdev.8*
%{_mandir}/man8/ramsize.8*
%{_mandir}/man8/rootflags.8*
%{_mandir}/man8/swapdev.8*
%{_mandir}/man8/vidmode.8*
%endif
%{_sbindir}/readprofile
%{_sbindir}/tunelp
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

%{_mandir}/man6/banner.6*

#%{_mandir}/man8/agtetty.8*
%{_mandir}/man8/blockdev.8*
%{_mandir}/man8/ctrlaltdel.8*
%{_mandir}/man8/dmesg.8*
%{_mandir}/man8/elvtune.8*
%{_mandir}/man8/fdformat.8*
%{_mandir}/man8/fdisk.8*
%{_mandir}/man8/hwclock.8*
%{_mandir}/man8/ipcrm.8*
%{_mandir}/man8/ipcs.8*
%{_mandir}/man8/kbdrate.8*
%{_mandir}/man8/mkfs.8*
#%{_mandir}/man8/mkfs.bfs.8*
%{_mandir}/man8/mkswap.8*
%{_mandir}/man8/raw.8*
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

%changelog
* Wed Jul 11 2001 Bill Nottingham <notting@redhat.com>
- fix vipw to not create world-readable shadow files

* Sun Apr  8 2001 Matt Wilson <msw@redhat.com>
- changed Requires: kernel >= 2.2.12-7 to Conflicts: kernel < 2.2.12-7
  (fixes a initscripts -> util-linux -> kernel -> initscripts prereq loop)

* Thu Mar 22 2001 Erik Troan <ewt@redhat.com>
- added -e option to swapon
- made -a silently skip swap devics that are already enabled

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
