# -*- Mode: rpm-spec -*-
#
# (c) Mandriva
#

%define kernelversion	3
%define patchlevel	4
%define sublevel	19

# kernel.org -rcX patch (only the number after "rc")
%define krc		0

# kernel.org -gitX patch (only the number after "git")
%define kgit		0

# this is the releaseversion
%define mdvrelease 	1

# This is only to make life easier for people that creates derivated kernels
# a.k.a name it kernel-tmb :)
%define kname 		kernel-linus

%define rpmtag		%distsuffix

%if %krc || %kgit
%define	rpmrel		%mkrel %{?%{krc}:-rc%{krc}}%{?%{kgit}:-git%{kgit}}-%{mdvrelease}
%else
%define rpmrel		%mkrel %{mdvrelease}
%endif


# theese two never change, they are used to fool rpm/urpmi/smart
%define fakever		1
%define fakerel		%mkrel 1

# When we are using a rc/git patch
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}
%define kverrel   	%{kversion}-%{rpmrel}

# used for not making too long names for rpms or search paths
%if %krc || %kgit
%define tar_ver	  	%{kernelversion}.%(expr %{patchlevel} - 1)
%define buildrpmrel	0%{?%{krc}:.rc%{krc}}%{?%{kgit}:.git%{kgit}}.%{mdvrelease}%{rpmtag}
%else
%define tar_ver	  	%{kernelversion}.%{patchlevel}
%define	buildrpmrel	%{mdvrelease}%{rpmtag}
%endif

%define buildrel        %{kversion}-%{buildrpmrel}

%define klinus_notice NOTE: This kernel has no Mandriva patches and no third-party drivers.

# having different top level names for packges means that you have to remove them by hard :(
%define top_dir_name    %{kname}-%{_arch}

%define build_dir       %{_builddir}/%{top_dir_name}
%define src_dir         %{build_dir}/linux-%{tar_ver}

# disable useless debug rpms...
%define _enable_debug_packages  %{nil}
%define debug_package           %{nil}

# build defines
%define build_doc 1
%define build_source 1
%define build_devel 1

%define build_kernel 1

%define distro_branch %(perl -pe '/(\\d+)\\.(\\d)\\.?(\\d)?/; $_="$1.$2"' /etc/mandriva-release)

# End of user definitions
%{?_without_kernel: %global build_kernel 0}
%{?_without_doc: %global build_doc 0}
%{?_without_source: %global build_source 0}
%{?_without_devel: %global build_devel 0}

%{?_with_kernel: %global build_kernel 1}
%{?_with_doc: %global build_doc 1}
%{?_with_source: %global build_source 1}
%{?_with_devel: %global build_devel 1}

%if %(if [ -z "$CC" ] ; then echo 0; else echo 1; fi)
%define kmake %make CC="$CC"
%else
%define kmake %make
%endif
# there are places where parallel make don't work
%define smake make

# Parallelize xargs invocations on smp machines
%define kxargs xargs %([ -z "$RPM_BUILD_NCPUS" ] \\\
	&& RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"; \\\
	[ "$RPM_BUILD_NCPUS" -gt 1 ] && echo "-P $RPM_BUILD_NCPUS")

# Aliases for amd64 builds (better make source links?)
%define target_cpu	%(echo %{_target_cpu} | sed -e "s/amd64/x86_64/")
%define target_arch	%(echo %{_arch} | sed -e "s/amd64/x86_64/")

# src.rpm description
Summary: 	The Linux kernel (the core of the Linux operating system)
Name:           %{kname}
Version:        %{kversion}
Release:        %{rpmrel}
License: 	GPLv2
Group: 		System/Kernel and hardware
ExclusiveArch: 	%{ix86} x86_64
ExclusiveOS: 	Linux
URL: 		https://wiki.mandriva.com/en/Docs/Howto/Mandriva_Kernels#kernel-linus

####################################################################
#
# Sources
#
### This is for full SRC RPM
Source0:        ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.0/linux-%{tar_ver}.tar.xz
Source1:        ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.0/linux-%{tar_ver}.tar.sign

# This is for disabling mrproper and other targets on -devel rpms
Source2:	disable-mrproper-in-devel-rpms.patch

Source4:       README.kernel-sources

# Kernel defconfigs
Source20: 	i386_defconfig
Source21: 	x86_64_defconfig

# rpmlintrc
Source30:	%{name}.rpmlintrc


####################################################################
#
# Patches

#
# Patch0 to Patch100 are for core kernel upgrades.
#

# Pre linus patch: ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing

%if %sublevel
Patch1:         ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.0/patch-%{kversion}.xz
Source10:       ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.0/patch-%{kversion}.sign
%endif
# kernel.org -git
%if %kgit
Patch2:         ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/snapshots/patch-%{kernelversion}.%{patchlevel}-%{sublevel}-git%{kgit}.xz
Source11:       ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/snapshots/patch-%{kernelversion}.%{patchlevel}-%{sublevel}-git%{kgit}.sign
%endif

#END
####################################################################

# Defines for the things that are needed for all the kernels
%define requires1 module-init-tools >= 3.6-12
%define requires2 mkinitrd >= 3.4.43-10
%define requires3 bootloader-utils >= 1.9
%define requires4 sysfsutils
%define requires5 kernel-firmware >= 2.6.27-0.rc2.2mdv

%define kprovides kernel = %{tar_ver}, alsa

Autoreqprov: 	no
BuildRequires: 	gcc module-init-tools >= 0.9.15

%description
Source package to build the Linux kernel.

%{klinus_notice}


#
# kernel: Symmetric MultiProcessing kernel
#
%if %build_kernel
%package -n %{kname}-%{buildrel}
Version:	%{fakever}
Release:	%{fakerel}
%ifarch %{ix86}
Summary:	Linux Kernel for desktop use with i586 & 4GB RAM
%else
Summary:	Linux Kernel for desktop use with %{_arch}
%endif
Group:		System/Kernel and hardware
Provides:	%kprovides
Provides:	should-restart = system
Requires:	%requires1
Requires:	%requires2
Requires:	%requires3
Requires:	%requires4
Requires: 	%requires5

%ifarch %{ix86}
Conflicts:	arch(x86_64)
%endif

%description -n %{kname}-%{buildrel}
%ifarch %{ix86}
This kernel is compiled for desktop use, single or multiple i586
processor(s)/core(s) and less than 4GB RAM, using HZ_1000, voluntary
preempt, CFS cpu scheduler and cfq i/o scheduler.
This kernel relies on in-kernel smp alternatives to switch between
up & smp mode depending on detected hardware. To force the kernel
to boot in single processor mode, use the "nosmp" boot parameter.
%else
This kernel is compiled for desktop use, single or multiple %{_arch}
processor(s)/core(s), using HZ_1000, voluntary preempt, CFS cpu
scheduler and cfq i/o scheduler.
This kernel relies on in-kernel smp alternatives to switch between
up & smp mode depending on detected hardware. To force the kernel
to boot in single processor mode, use the "nosmp" boot parameter.
%endif

For instructions for update, see:
http://www.mandriva.com/en/security/kernelupdate

%{klinus_notice}
%endif # build_kernel


#
# kernel-source: kernel sources
#
%if %build_source
%package -n %{kname}-source-%{buildrel}
Version:	%{fakever}
Release:	%{fakerel}
Provides:	%{kname}-source, kernel-source = %{kverrel}, kernel-devel = %{kverrel}
Provides:	%{kname}-source-%{kernelversion}.%{patchlevel}
Requires:	glibc-devel, ncurses-devel, make, gcc, perl, diffutils
Summary:	The source code for the Linux kernel
Group:		Development/Kernel
Autoreqprov: 	no
%ifarch %{ix86}
Conflicts:	arch(x86_64)
%endif

%description -n %{kname}-source-%{buildrel}
The %{kname}-source package contains the source code files for the
Linux kernel. Theese source files are only needed if you want to build
your own custom kernel that is better tuned to your particular hardware.

If you only want the files needed to build 3rdparty (nVidia, Ati, dkms-*,...)
drivers against, install the *-devel-* rpm that is matching your kernel.

For instructions for update, see:
http://www.mandriva.com/en/security/kernelupdate

%{klinus_notice}
%endif #build_source


#
# kernel-devel: stripped kernel sources
#
%if %build_devel
%package -n %{kname}-devel-%{buildrel}
Version:	%{fakever}
Release:	%{fakerel}
Provides:	kernel-devel = %{kverrel}
Summary:	The %{kname} devel files for 3rdparty modules build
Group:		Development/Kernel
Autoreqprov:	no
Requires:	glibc-devel, ncurses-devel, make, gcc, perl
%ifarch %{ix86}
Conflicts:	arch(x86_64)
%endif

%description -n %{kname}-devel-%{buildrel}
This package contains the kernel-devel files that should be enough to build
3rdparty drivers against for use with the %{kname}-%{buildrel}.

If you want to build your own kernel, you need to install the full
%{kname}-source-%{buildrel} rpm.

%{klinus_notice}
%endif #build_devel


#
# kernel-doc: documentation for the Linux kernel
#
%if %build_doc
%package -n %{kname}-doc
Version:        %{kversion}
Release:        %{rpmrel}
Summary:	Various documentation bits found in the kernel source
Group:		Books/Computer books
Buildarch:	noarch

%description -n %{kname}-doc
This package contains documentation files form the kernel source. Various
bits of information about the Linux kernel and the device drivers shipped
with it are documented in these files. You also might want install this
package if you need a reference to the options that can be passed to Linux
kernel modules at load time.

For instructions for update, see:
http://www.mandriva.com/en/security/kernelupdate

%{klinus_notice}
%endif #build_doc


#
# kernel-latest: virtual rpm
#
%if %build_kernel
%package -n %{kname}-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-%{buildrel}
Obsoletes:	%{kname}-smp-latest
%ifarch %{ix86}
Conflicts:	arch(x86_64)
%endif

%description -n %{kname}-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname} installed...

%{klinus_notice}
%endif #build_kernel


#
# kernel-source-latest: virtual rpm
#
%if %build_source
%package -n %{kname}-source-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-source
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-source-%{buildrel}
%ifarch %{ix86}
Conflicts:	arch(x86_64)
%endif

%description -n %{kname}-source-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-source installed...

%{klinus_notice}
%endif #build_source


#
# kernel-devel-latest: virtual rpm
#
%if %build_devel
%package -n %{kname}-devel-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-devel
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-devel-%{buildrel}
Obsoletes:	%{kname}-smp-devel-latest
Obsoletes:	%{kname}-smp-headers-latest
%ifarch %{ix86}
Conflicts:	arch(x86_64)
%endif

%description -n %{kname}-devel-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-devel installed...

%{klinus_notice}
%endif #build_devel


#
# End packages - here begins build stage
#
%prep
%setup -q -n %top_dir_name -c

pushd %src_dir
%if %sublevel
%patch1 -p1
%endif
%if %kgit
%patch2 -p1
%endif
popd

# PATCH END


#
# Setup Begin
#


# Install defconfigs...
install %{SOURCE20} %{build_dir}/linux-%{tar_ver}/arch/x86/configs/
install %{SOURCE21} %{build_dir}/linux-%{tar_ver}/arch/x86/configs/

# make sure the kernel has the patchlevel we know it has...
LC_ALL=C perl -p -i -e "s/^SUBLEVEL.*/SUBLEVEL = %{sublevel}/" linux-%{tar_ver}/Makefile

# switching back to ld.bfd May be it is not the best solution, but it works.
sed -i '/^LD/s/ld$/ld.bfd/' %{build_dir}/linux-%{tar_ver}/Makefile

%build
# Common target directories
%define _bootdir /boot
%define _modulesdir /lib/modules
%define _firmwaredir /lib/firmware
%define _kerneldir /usr/src/%{kname}-%{buildrel}
%define _develdir /usr/src/%{kname}-devel-%{buildrel}


# Directories definition needed for building
%define temp_root %{build_dir}/temp-root
%define temp_boot %{temp_root}%{_bootdir}
%define temp_modules %{temp_root}%{_modulesdir}
%define temp_firmware %{temp_root}%{_firmwaredir}
%define temp_source %{temp_root}%{_kerneldir}
%define temp_devel %{temp_root}%{_develdir}


# Create a simulacro of buildroot
rm -rf %{temp_root}
install -d %{temp_root}


# make sure we are in the directory
cd %{src_dir}

# make sure EXTRAVERSION says what we want it to say
LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = %{?%{krc}:-rc%{krc}}%{?%{kgit}:-git%{kgit}}-%{buildrpmrel}/" Makefile

# Prepare the kernel
%smake -s mrproper
%ifarch %{ix86} x86_64
	cp arch/x86/configs/%{target_arch}_defconfig .config
%else
	cp arch/%{target_arch}/defconfig .config
%endif
%smake ARCH=%{target_arch} oldconfig

# Build the kernel
%kmake ARCH=%{target_arch} all

# Install kernel
install -d %{temp_boot}
install -m 644 System.map %{temp_boot}/System.map-%{buildrel}
install -m 644 .config %{temp_boot}/config-%{buildrel}
cp -f arch/%{target_arch}/boot/bzImage %{temp_boot}/vmlinuz-%{buildrel}

# Install modules
install -d %{temp_modules}/%{buildrel}
%smake INSTALL_MOD_PATH=%{temp_root} KERNELRELEASE=%{buildrel} modules_install 

# OLD COMMENT: remove /lib/firmware, we use a separate kernel-firmware
# COMMENT: I add it, but clean the firmware dir, because some firmware 
#          not exist in the official firmware packages
for i in `%{_bindir}/urpmq -l kernel-firmware | /bin/sort -u | %__grep '^/lib/firmware' | %__sed "s#^/lib/firmware#%{temp_firmware}#g"` ; do
	[[ -f $i ]] && rm -f $i
done
for i in `%{_bindir}/urpmq -l kernel-firmware-extra | /bin/sort -u | %__grep '^/lib/firmware' | %__sed "s#^/lib/firmware#%{temp_firmware}#g"` ; do
	[[ -f $i ]] && rm -f $i
done
find %{temp_firmware} -type d | xargs rmdir --ignore-fail-on-non-empty

# Save devel tree
%if %build_devel
mkdir -p %{temp_devel}
for i in $(find . -name 'Makefile*'); do cp -R --parents $i %{temp_devel};done
for i in $(find . -name 'Kconfig*' -o -name 'Kbuild*' -o -name config.mk); do cp -R --parents $i %{temp_devel};done
cp -fR include %{temp_devel}
cp -fR scripts %{temp_devel}
%ifarch %{ix86} x86_64
	cp -fR arch/x86/kernel/asm-offsets.{c,s} %{temp_devel}/arch/x86/kernel/
	cp -fR arch/x86/kernel/asm-offsets_{32,64}.c %{temp_devel}/arch/x86/kernel/
	cp -fR arch/x86/include %{temp_devel}/arch/x86/
%else
	cp -fR arch/%{target_arch}/kernel/asm-offsets.{c,s} %{temp_devel}/arch/%{target_arch}/kernel/
	cp -fR arch/%{target_arch}/include %{temp_devel}/arch/%{target_arch}/
%endif

# Needed for generation of kernel/bounds.s
cp -fR kernel/bounds.c %{temp_devel}/kernel/

# Needed for lguest
cp -fR drivers/lguest/lg.h %{temp_devel}/drivers/lguest/

cp -fR .config Module.symvers %{temp_devel}

# Needed for truecrypt build (Danny)
cp -fR drivers/md/dm.h %{temp_devel}/drivers/md/

# Needed for external dvb tree (#41418)
cp -fR drivers/media/dvb/dvb-core/*.h %{temp_devel}/drivers/media/dvb/dvb-core/
cp -fR drivers/media/dvb/frontends/lgdt330x.h %{temp_devel}/drivers/media/dvb/frontends/

# add acpica header files, needed for fglrx build
cp -fR drivers/acpi/acpica/*.h %{temp_devel}/drivers/acpi/acpica/

# Need
%ifarch %{ix86} x86_64
cp -fR arch/x86/syscalls/* %{temp_devel}/arch/x86/syscalls/
cp -fR arch/x86/tools/* %{temp_devel}/arch/x86/tools/
%endif
cp -fR tools/include %{temp_devel}/tools/
cp -fR Documentation/DocBook/media/*.b64 %{temp_devel}/Documentation/DocBook/media/

# Check and clean the -devel tree
pushd %{temp_devel} >/dev/null
    %smake -s prepare scripts clean
    rm -f .config.old
popd >/dev/null

# Disable mrproper and other targets
patch -p1 -d %{temp_devel} -i %{SOURCE2}

# Fix permissions
chmod -R a+rX %{temp_devel}
%endif # build_devel

#make sure we are in the directory
cd %src_dir

# kernel-source is shipped as an unprepared tree
%smake -s mrproper


###
### Install
###
%install
install -m 644 %{SOURCE4}  .

cd %src_dir
# Directories definition needed for installing
%define target_source %{buildroot}/%{_kerneldir}
%define target_boot %{buildroot}%{_bootdir}
%define target_modules %{buildroot}%{_modulesdir}
%define target_devel %{buildroot}%{_develdir}

# We want to be able to test several times the install part
rm -rf %{buildroot}
cp -a %{temp_root} %{buildroot}

# Create directories infastructure
%if %build_source
install -d %{target_source}

tar cf - . | tar xf - -C %{target_source}
chmod -R a+rX %{target_source}

# we remove all the source files that we don't ship

# first architecture files
for i in alpha arm avr32 blackfin cris frv h8300 hexagon ia64 m32r mips \
	microblaze m68k m68knommu mn10300 openrisc parisc powerpc ppc \
	s390 score sh sh64 sparc tile unicore32 v850 c6x xtensa; do
	rm -rf %{target_source}/arch/$i

%if %build_devel
	rm -rf %{target_devel}/arch/$i
%endif
done

# remove arch files based on target arch
%ifnarch %{ix86} x86_64
	rm -rf %{target_source}/arch/x86
%if %build_devel
	rm -rf %{target_devel}/arch/x86
%endif
%endif


# other misc files
rm -f %{target_source}/{.config.old,.config.cmd,.tmp_gas_check,.mailmap,.missing-syscalls.d,arch/.gitignore}

#endif %build_source
%endif


# gzipping modules
find %{target_modules} -name "*.ko" | %kxargs gzip -9


# We used to have a copy of PrepareKernel here
# Now, we make sure that the thing in the linux dir is what we want it to be

for i in %{target_modules}/*; do
  rm -f $i/build $i/source
done

# sniff, if we gzipped all the modules, we change the stamp :(
# we really need the depmod -ae here
pushd %{target_modules}
for i in *; do
	/sbin/depmod -u -ae -b %{buildroot} -r -F %{target_boot}/System.map-$i $i
	echo $?
done

for i in *; do
	pushd $i
	echo "Creating module.description for $i"
	modules=`find . -name "*.ko.gz"`
	echo $modules | %kxargs /sbin/modinfo \
	| perl -lne 'print "$name\t$1" if $name && /^description:\s*(.*)/; $name = $1 if m!^filename:\s*(.*)\.k?o!; $name =~ s!.*/!!' > modules.description
	popd
done
popd


###
### Clean
###

%clean
rm -rf %{buildroot}
# We don't want to remove this, the whole reason of its existence is to be 
# able to do several rpm --short-circuit -bi for testing install 
# phase without repeating compilation phase
#rm -rf %{temp_root} 


###
### Scripts
###

### kernel
%if %build_kernel
%preun -n %{kname}-%{buildrel}
/sbin/installkernel -R %{buildrel}
if [ -L /lib/modules/%{buildrel}/build ]; then
    rm -f /lib/modules/%{buildrel}/build
fi
if [ -L /lib/modules/%{buildrel}/source ]; then
    rm -f /lib/modules/%{buildrel}/source
fi
pushd /boot > /dev/null
if [ -L vmlinuz-linus ]; then
    if [ "$(readlink vmlinuz-linus)" = "vmlinuz-%{buildrel}" ]; then
	rm -f vmlinuz-linus
    fi
fi
if [ -L initrd-linus.img ]; then
    if [ "$(readlink initrd-linus.img)" = "initrd-%{buildrel}.img" ]; then
	rm -f initrd-linus.img
    fi
fi
popd > /dev/null
exit 0

%post -n %{kname}-%{buildrel}
/sbin/installkernel -L %{buildrel}
if [ -d /usr/src/%{kname}-devel-%{buildrel} ]; then
    ln -sf /usr/src/%{kname}-devel-%{buildrel} /lib/modules/%{buildrel}/build
    ln -sf /usr/src/%{kname}-devel-%{buildrel} /lib/modules/%{buildrel}/source
fi
pushd /boot > /dev/null
if [ -L vmlinuz-linus ]; then
    rm -f vmlinuz-linus
fi
ln -sf vmlinuz-%{buildrel} vmlinuz-linus
if [ -L initrd-linus.img ]; then
    rm -f initrd-linus.img
fi
ln -sf initrd-%{buildrel}.img initrd-linus.img
popd > /dev/null

%postun -n %{kname}-%{buildrel}
/sbin/kernel_remove_initrd %{buildrel}
rm -rf /lib/modules/%{buildrel} >/dev/null
%endif # build_kernel


### kernel-devel
%if %build_devel
%post -n %{kname}-devel-%{buildrel}
# place /build and /source symlinks in place.
if [ -d /lib/modules/%{buildrel} ]; then
    ln -sf /usr/src/%{kname}-devel-%{buildrel} /lib/modules/%{buildrel}/build
    ln -sf /usr/src/%{kname}-devel-%{buildrel} /lib/modules/%{buildrel}/source
fi

%preun -n %{kname}-devel-%{buildrel}
# we need to delete <modules>/{build,source} at uninstall
if [ -L /lib/modules/%{buildrel}/build ]; then
    rm -f /lib/modules/%{buildrel}/build
fi
if [ -L /lib/modules/%{buildrel}/source ]; then
    rm -f /lib/modules/%{buildrel}/source
fi
exit 0
%endif #build_devel


### kernel-source
%if %build_source
%post -n %{kname}-source-%{buildrel}
for i in /lib/modules/%{buildrel}*; do
	if [ -d $i ]; then
		if [ ! -L $i/build -a ! -L $i/source ]; then
			rm -f $i/{build,source}
		        ln -sf /usr/src/%{kname}-%{buildrel} $i/build
		        ln -sf /usr/src/%{kname}-%{buildrel} $i/source
		fi
	fi
done

%preun -n %{kname}-source-%{buildrel}
for i in /lib/modules/%{buildrel}/{build,source}; do
	if [ -L $i ]; then
		if [ "$(readlink $i)" = "/usr/src/%{kname}-%{buildrel}" ]; then
			rm -f $i
		fi
	fi
done
exit 0
%endif # build_source


###
### file lists
###

# kernel
%if %build_kernel
%files -n %{kname}-%{buildrel}
%defattr(-,root,root)
%{_bootdir}/config-%{buildrel}
%{_bootdir}/vmlinuz-%{buildrel}
%{_bootdir}/System.map-%{buildrel}
%dir %{_modulesdir}/%{buildrel}/
%{_modulesdir}/%{buildrel}/kernel
%{_modulesdir}/%{buildrel}/modules.*
%{_firmwaredir}
%doc README.kernel-sources
%endif # build_kernel

# kernel-source
%if %build_source
%files -n %{kname}-source-%{buildrel}
%defattr(-,root,root)
%dir %{_kerneldir}
%dir %{_kerneldir}/arch
%dir %{_kerneldir}/include
%{_kerneldir}/.gitignore
%{_kerneldir}/COPYING
%{_kerneldir}/CREDITS
%{_kerneldir}/Documentation
%{_kerneldir}/Kbuild
%{_kerneldir}/Kconfig
%{_kerneldir}/MAINTAINERS
%{_kerneldir}/Makefile
%{_kerneldir}/README
%{_kerneldir}/REPORTING-BUGS
%{_kerneldir}/arch/Kconfig
%ifarch %{ix86} x86_64
%{_kerneldir}/arch/x86
%endif
%{_kerneldir}/arch/um
%{_kerneldir}/block
%{_kerneldir}/crypto
%{_kerneldir}/drivers
%{_kerneldir}/firmware
%{_kerneldir}/fs
%{_kerneldir}/include/Kbuild
%{_kerneldir}/include/acpi
%{_kerneldir}/include/asm-generic
%{_kerneldir}/include/crypto
%{_kerneldir}/include/drm
%{_kerneldir}/include/linux
%{_kerneldir}/include/math-emu
#%{_kerneldir}/include/memory
%{_kerneldir}/include/net
%{_kerneldir}/include/pcmcia
%{_kerneldir}/include/scsi
%{_kerneldir}/include/sound
%{_kerneldir}/include/target
%{_kerneldir}/include/trace
%{_kerneldir}/include/video
%{_kerneldir}/include/media
%{_kerneldir}/include/misc
%{_kerneldir}/include/mtd
%{_kerneldir}/include/rxrpc
%{_kerneldir}/include/keys
%{_kerneldir}/include/rdma
%{_kerneldir}/include/xen
%{_kerneldir}/init
%{_kerneldir}/ipc
%{_kerneldir}/kernel
%{_kerneldir}/lib
%{_kerneldir}/mm
%{_kerneldir}/net
%{_kerneldir}/samples
%{_kerneldir}/scripts
%{_kerneldir}/security
%{_kerneldir}/sound
%{_kerneldir}/tools
%{_kerneldir}/usr
%{_kerneldir}/virt
%doc README.kernel-sources
%endif # build_source

# kernel-devel
%if %build_devel
%files -n %{kname}-devel-%{buildrel}
%defattr(-,root,root)
%dir %{_develdir}
%dir %{_develdir}/arch
%dir %{_develdir}/include
%{_develdir}/.config
%{_develdir}/Documentation
%{_develdir}/Kbuild
%{_develdir}/Kconfig
%{_develdir}/Makefile
%{_develdir}/Module.symvers
%{_develdir}/arch/Kconfig
%ifarch %{ix86} x86_64
%{_develdir}/arch/x86
%endif
%{_develdir}/arch/um
%{_develdir}/block
%{_develdir}/crypto
%{_develdir}/drivers
%{_develdir}/firmware
%{_develdir}/fs
%{_develdir}/include/Kbuild
%{_develdir}/include/acpi
%{_develdir}/include/asm-generic
%{_develdir}/include/config
%{_develdir}/include/crypto
%{_develdir}/include/drm
%{_develdir}/include/generated
%{_develdir}/include/keys
%{_develdir}/include/linux
%{_develdir}/include/math-emu
%{_develdir}/include/misc
#%{_develdir}/include/memory
%{_develdir}/include/mtd
%{_develdir}/include/net
%{_develdir}/include/pcmcia
%{_develdir}/include/rdma
%{_develdir}/include/scsi
%{_develdir}/include/sound
%{_develdir}/include/target
%{_develdir}/include/trace
%{_develdir}/include/video
%{_develdir}/include/media
%{_develdir}/include/rxrpc
%{_develdir}/include/xen
%{_develdir}/init
%{_develdir}/ipc
%{_develdir}/kernel
%{_develdir}/lib
%{_develdir}/mm
%{_develdir}/net
%{_develdir}/samples
%{_develdir}/scripts
%{_develdir}/security
%{_develdir}/sound
%{_develdir}/tools
%{_develdir}/usr
%{_develdir}/virt
%doc README.kernel-sources
%endif # build_devel


%if %build_doc
%files -n %{kname}-doc
%defattr(-,root,root)
%doc linux-%{tar_ver}/Documentation/*
%endif # build_doc

%if %build_kernel
%files -n %{kname}-latest
%defattr(-,root,root)
%endif # build_kernel

%if %build_source
%files -n %{kname}-source-latest
%defattr(-,root,root)
%endif # build_source

%if %build_devel
%files -n %{kname}-devel-latest
%defattr(-,root,root)
%endif # build_devel


%changelog
* Thu Oct 04 2012 Lonyai Gergely <aleph@mandriva.org> 3.4.12-1mdv2012.0
+ Revision: 818364
- 3.4.12

* Tue Sep 18 2012 Lonyai Gergely <aleph@mandriva.org> 3.4.11-1
+ Revision: 817076
- Try resolv the ld problem (Thanks dmikhirev)
- 3.4.11
- 3.4.10
- 3.4.9
- 3.4.8
- Downgrade: 3.4.7
- Add include/memory
- 3.5

* Fri Jul 20 2012 Lonyai Gergely <aleph@mandriva.org> 3.4.6-1
+ Revision: 810348
- 3.4.6
- Add XEN_SELDBALLONING driver

* Tue Jul 17 2012 Lonyai Gergely <aleph@mandriva.org> 3.4.5-1
+ Revision: 810100
- Remove c6x arch
- Add Documentation/DocBook/media/*.b64
- Resolv 'syscall_32 compile problem'
- 3.4.5
- kernel config revision from official kernel config
- Add x32 ABI support
- 3.4.4
- Disable CONFIG_X86_X32
- 3.4

* Mon May 21 2012 Lonyai Gergely <aleph@mandriva.org> 3.2.18-1
+ Revision: 799754
- .3.2.18

* Mon Apr 16 2012 Lonyai Gergely <aleph@mandriva.org> 3.2.15-1
+ Revision: 791397
- 3.2.15

* Wed Apr 04 2012 Lonyai Gergely <aleph@mandriva.org> 3.2.14-1
+ Revision: 789152
- 3.2.14

* Fri Mar 23 2012 Lonyai Gergely <aleph@mandriva.org> 3.2.13-1
+ Revision: 786511
- 3.2.12

* Thu Mar 15 2012 Lonyai Gergely <aleph@mandriva.org> 3.2.11-1
+ Revision: 785074
- 3.2.11
- 3.2.11

* Mon Mar 05 2012 Lonyai Gergely <aleph@mandriva.org> 3.2.9-1
+ Revision: 782134
- 3.2.9

* Tue Feb 28 2012 Lonyai Gergely <aleph@mandriva.org> 3.2.8-1
+ Revision: 781326
- 3.2.7

* Tue Feb 21 2012 Lonyai Gergely <aleph@mandriva.org> 3.2.7-1
+ Revision: 778523
- 3.2.7

* Wed Feb 15 2012 Lonyai Gergely <aleph@mandriva.org> 3.2.6-1
+ Revision: 774116
- 3.2.6

* Thu Feb 09 2012 Lonyai Gergely <aleph@mandriva.org> 3.2.5-1
+ Revision: 772344
- 3.2.5

* Sat Feb 04 2012 Lonyai Gergely <aleph@mandriva.org> 3.2.4-1
+ Revision: 771190
- 3.2.4

* Fri Jan 27 2012 Lonyai Gergely <aleph@mandriva.org> 3.2.2-1
+ Revision: 769350
- Remove a duplicated record from %%files
- 3.2.2

* Wed Jan 18 2012 Lonyai Gergely <aleph@mandriva.org> 3.2.1-1
+ Revision: 762114
- Remove hexagon arch
  Add a file to %%files (devel|source)
- 3.2.1

* Fri Jan 13 2012 Lonyai Gergely <aleph@mandriva.org> 3.1.9-1
+ Revision: 760697
- 3.1.9

* Mon Jan 09 2012 Lonyai Gergely <aleph@mandriva.org> 3.1.8-1
+ Revision: 759228
- 3.1.8

* Fri Dec 23 2011 Lonyai Gergely <aleph@mandriva.org> 3.1.6-1
+ Revision: 744742
- 3.1.6

* Fri Dec 09 2011 Lonyai Gergely <aleph@mandriva.org> 3.1.5-1
+ Revision: 739712
- 3.1.5

* Tue Nov 29 2011 Lonyai Gergely <aleph@mandriva.org> 3.1.4-1
+ Revision: 735399
- 3.1.4

* Sun Nov 27 2011 Lonyai Gergely <aleph@mandriva.org> 3.1.3-1
+ Revision: 733678
- 3.1.3

* Fri Nov 25 2011 Lonyai Gergely <aleph@mandriva.org> 3.1.2-1
+ Revision: 733317
- 3.1.2

* Fri Nov 18 2011 Lonyai Gergely <aleph@mandriva.org> 3.1.1-1
+ Revision: 731665
- Remove last RPM_BUILD_DIR
- 3.1.1
- 3.0.9

* Mon Oct 31 2011 Lonyai Gergely <aleph@mandriva.org> 3.0.8-1
+ Revision: 708003
- 3.0.8
- 3.0.7

* Thu Sep 01 2011 Lonyai Gergely <aleph@mandriva.org> 3.0.4-1
+ Revision: 697748
- 3.0.4

* Tue Aug 23 2011 Lonyai Gergely <aleph@mandriva.org> 3.0.3-5
+ Revision: 696277
- dd i386 config: PROC_DEVICETREE support
- Chanege the memory option from 64G to 4G on i386 arch.
 - drop xen support on i386
 - add OLPC support on i386
  Add some network option to config
- Good bye IDE!

* Fri Aug 19 2011 Lonyai Gergely <aleph@mandriva.org> 3.0.3-4
+ Revision: 695294
- Add ATI KMS support

* Thu Aug 18 2011 Lonyai Gergely <aleph@mandriva.org> 3.0.3-1
+ Revision: 695133
- 3.0.3

* Wed Aug 17 2011 Lonyai Gergely <aleph@mandriva.org> 3.0.2-1
+ Revision: 695014
- 3.0.2
- Fix some makro
- fix the release numbering

* Sat Aug 06 2011 Lonyai Gergely <aleph@mandriva.org> 3.0.1-0.1.3
+ Revision: 693379
- 3.0.1

* Mon Aug 01 2011 Lonyai Gergely <aleph@mandriva.org> 3.0.0-3
+ Revision: 692708
- I try revert to the fast kernel. An option was very bad idea.

* Fri Jul 29 2011 Lonyai Gergely <aleph@mandriva.org> 3.0.0-2
+ Revision: 692218
- Change the modules comression to gzip, again

* Thu Jul 28 2011 Lonyai Gergely <aleph@mandriva.org> 3.0.0-1
+ Revision: 692156
- 3.0

* Tue Jul 26 2011 Lonyai Gergely <aleph@mandriva.org> 2.6.39.3-3
+ Revision: 691769
- Add XEN support to i386 (and the required: memory High Memory Support (64GB))

* Sun Jul 24 2011 Lonyai Gergely <aleph@mandriva.org> 2.6.39.3-2
+ Revision: 691480
- Force the ARCH in kernel compile
- Update the configs and fix the i386 config (again)
- Add a missing file to source package
- I commit a wrong i386_defconfig
- 2.6.39.3

* Sun May 22 2011 Thomas Backlund <tmb@mandriva.org> 2.6.38.7-1
+ Revision: 677266
- update to 2.6.38.7 (CVE-2011-1770, CVE-2011-1776, CVE-2011-1927)

* Wed May 11 2011 Thomas Backlund <tmb@mandriva.org> 2.6.38.6-1
+ Revision: 673511
- update to 2.6.38.6
- clean /lib/modules on kernel removal (#42962)

* Tue May 03 2011 Thomas Backlund <tmb@mandriva.org> 2.6.38.5-1
+ Revision: 664974
- update to 2.6.38.5

* Fri Apr 22 2011 Thomas Backlund <tmb@mandriva.org> 2.6.38.4-1
+ Revision: 656589
- update to 2.6.38.4

* Sat Apr 16 2011 Thomas Backlund <tmb@mandriva.org> 2.6.38.3-1
+ Revision: 653329
- update to 2.6.38.3
- fix generation of modules.description (thanks tv)

* Mon Mar 28 2011 Thomas Backlund <tmb@mandriva.org> 2.6.38.2-1
+ Revision: 648681
- update to 2.6.38.2 (CVE-2011-0726)

* Thu Mar 24 2011 Thomas Backlund <tmb@mandriva.org> 2.6.38.1-1
+ Revision: 648239
- update to 2.6.38.1

* Tue Mar 15 2011 Thomas Backlund <tmb@mandriva.org> 2.6.38-1
+ Revision: 644884
- update to 2.6.38 final
- update to 2.6.38-rc8

* Fri Mar 04 2011 Thomas Backlund <tmb@mandriva.org> 2.6.38-0.rc7.2.1
+ Revision: 642039
- update to 2.6.38-rc7-git2

* Thu Mar 03 2011 Thomas Backlund <tmb@mandriva.org> 2.6.38-0.rc7.1
+ Revision: 641424
- update filelists
- drop S5 as we ship an unprepared source tree
- update defconfigs
- rediff S2
- update to 2.6.38-rc7

* Fri Feb 25 2011 Thomas Backlund <tmb@mandriva.org> 2.6.37.2-1
+ Revision: 639805
- update to 2.6.37.2

* Wed Jan 05 2011 Thomas Backlund <tmb@mandriva.org> 2.6.37-1mdv2011.0
+ Revision: 628747
- update to 2.6.37 final

* Wed Dec 29 2010 Thomas Backlund <tmb@mandriva.org> 2.6.37-0.rc8.1mdv2011.0
+ Revision: 625960
- update to 2.6.37-rc8

* Fri Dec 24 2010 Thomas Backlund <tmb@mandriva.org> 2.6.37-0.rc7.2.1mdv2011.0
+ Revision: 624567
- update to 2.6.37-rc7-git2

* Tue Dec 21 2010 Thomas Backlund <tmb@mandriva.org> 2.6.37-0.rc7.1mdv2011.0
+ Revision: 623726
- update to 2.6.37-rc7

* Thu Dec 16 2010 Thomas Backlund <tmb@mandriva.org> 2.6.37-0.rc6.1mdv2011.0
+ Revision: 622269
- update to 2.6.37-rc6

* Tue Dec 07 2010 Thomas Backlund <tmb@mandriva.org> 2.6.37-0.rc5.1mdv2011.0
+ Revision: 613810
- update to 2.6.37-rc5

* Tue Nov 30 2010 Thomas Backlund <tmb@mandriva.org> 2.6.37-0.rc4.1mdv2011.0
+ Revision: 603504
- re-enable BKL as too many drivers still depend on it
- re-enable drivers depending on BKL
- update to 2.6.37-rc4

* Mon Nov 22 2010 Thomas Backlund <tmb@mandriva.org> 2.6.37-0.rc3.1mdv2011.0
+ Revision: 599780
- add toplevel Kconfig to -source and -devel rpms
- drop S3, fixed upstream
- rediff S2 to apply cleanly
- update defconfigs
- update to 2.6.37-rc3
- make kernel-source require diffutils as it uses both diff and cmp
  during build (mdv #61719)

* Thu Oct 21 2010 Thomas Backlund <tmb@mandriva.org> 2.6.36-1mdv2011.0
+ Revision: 587058
- update to 2.6.36 final
- make doc subpackage noarch

* Fri Oct 15 2010 Thomas Backlund <tmb@mandriva.org> 2.6.36-0.rc8.1.1mdv2011.0
+ Revision: 585822
- update to 2.6.36-rc8-git1
- update to 2.6.36-rc8

* Thu Oct 07 2010 Thomas Backlund <tmb@mandriva.org> 2.6.36-0.rc7.1mdv2011.0
+ Revision: 583952
- update to 2.6.36-rc7
- enable the new firewire stack (juju) so we can start testing apps
  against it (old stack is scheduled for removal around 2.6.37-39)
  (module-init-tools >= 3.6-12 have the new core blacklisted for
   now to avoid breakage)

* Wed Sep 29 2010 Thomas Backlund <tmb@mandriva.org> 2.6.36-0.rc6.1mdv2011.0
+ Revision: 582027
- update to 2.6.36-rc6

* Tue Sep 21 2010 Thomas Backlund <tmb@mandriva.org> 2.6.36-0.rc5.1mdv2011.0
+ Revision: 580325
- update to 2.6.36-rc5 (CVE-2010-3081, CVE-2010-3301)

* Mon Sep 13 2010 Thomas Backlund <tmb@mandriva.org> 2.6.36-0.rc4.1mdv2011.0
+ Revision: 577919
- remove tile arch from source/devel rpms
- rediff -devel patches
- update defconfigs
- update to 2.6.36-rc4
- raise CONFIG_NR_CPUS to 64 (mdv #60928)

* Fri Aug 27 2010 Thomas Backlund <tmb@mandriva.org> 2.6.35.4-1mdv2011.0
+ Revision: 573451
- update to 2.6.35.4 (CVE-2010-2803)

* Fri Aug 20 2010 Thomas Backlund <tmb@mandriva.org> 2.6.35.3-1mdv2011.0
+ Revision: 571524
- update to 2.6.35.3

* Sat Aug 14 2010 Thomas Backlund <tmb@mandriva.org> 2.6.35.2-1mdv2011.0
+ Revision: 569541
- sync defconfigs with main kernel
- update to 2.6.35.2

* Tue Aug 10 2010 Thomas Backlund <tmb@mandriva.org> 2.6.35.1-1mdv2011.0
+ Revision: 568859
- update to 2.6.35.1

* Mon Aug 02 2010 Thomas Backlund <tmb@mandriva.org> 2.6.35-1mdv2011.0
+ Revision: 564937
- update to 2.6.35 final
- drop sparc support
- enable CGROUPS on i586 too, and resync defconfigs

  + Thierry Vignaud <tv@mandriva.org>
    - new release

* Mon Jul 19 2010 Thierry Vignaud <tv@mandriva.org> 2.6.35-0.rc5.2mdv2011.0
+ Revision: 554959
- enable CGROUP for lxc and the like

* Tue Jul 13 2010 Thierry Vignaud <tv@mandriva.org> 2.6.35-0.rc5.1mdv2011.0
+ Revision: 552148
- new release

* Mon May 17 2010 Thomas Backlund <tmb@mandriva.org> 2.6.34-1mdv2010.1
+ Revision: 544893
- update to 2.6.34 final

* Sun May 09 2010 Thomas Backlund <tmb@mandriva.org> 2.6.34-0.rc6.6.1mdv2010.1
+ Revision: 544202
- update to 2.6.34-rc6-git6

* Wed May 05 2010 Thomas Backlund <tmb@mandriva.org> 2.6.34-0.rc6.4.1mdv2010.1
+ Revision: 542581
- update to 2.6.34-rc6-git4

* Fri Apr 30 2010 Thomas Backlund <tmb@mandriva.org> 2.6.34-0.rc6.1mdv2010.1
+ Revision: 541334
- update to 2.6.34-rc6

* Mon Apr 26 2010 Thomas Backlund <tmb@mandriva.org> 2.6.34-0.rc5.7.1mdv2010.1
+ Revision: 538813
- update to 2.6.34-rc5-git7 (ext4 corruption fix, ipv6 boot crash fix)

* Sun Apr 25 2010 Thomas Backlund <tmb@mandriva.org> 2.6.34-0.rc5.6.1mdv2010.1
+ Revision: 538537
- update to 2.6.34-rc5-git6

* Tue Apr 20 2010 Thomas Backlund <tmb@mandriva.org> 2.6.34-0.rc5.1mdv2010.1
+ Revision: 536944
- update to 2.6.34-rc5
- enable CONFIG_KSM (mdv #58384)

* Sat Apr 17 2010 Thomas Backlund <tmb@mandriva.org> 2.6.34-0.rc4.4.1mdv2010.1
+ Revision: 535896
- update to 2.6.34-rc4-git4

* Fri Apr 02 2010 Thomas Backlund <tmb@mandriva.org> 2.6.33.2-1mdv2010.1
+ Revision: 530769
- update to 2.6.33.2

* Mon Mar 22 2010 Thomas Backlund <tmb@mandriva.org> 2.6.33.1-2mdv2010.1
+ Revision: 526363
- bump release to get it past BS
- disable CONFIG_USB_PRINTER (like main kernel, #58293)
- update to 2.6.33.1

* Wed Feb 24 2010 Thomas Backlund <tmb@mandriva.org> 2.6.33-1mdv2010.1
+ Revision: 510768
- update to 2.6.33 final
- update to 2.6.33-rc8

* Sat Feb 06 2010 Thomas Backlund <tmb@mandriva.org> 2.6.33-0.rc7.1mdv2010.1
+ Revision: 501506
- update to 2.6.33-rc7

* Sat Feb 06 2010 Thomas Backlund <tmb@mandriva.org> 2.6.33-0.rc6.6.1mdv2010.1
+ Revision: 501300
- set CONFIG_SND_HDA_PATCH_LOADER=y in defconfigs
- set CONFIG_SND_HDA_INPUT_BEEP_MODE=2 in defconfigs
- update to 2.6.33-rc6-git6

* Tue Feb 02 2010 Thomas Backlund <tmb@mandriva.org> 2.6.33-0.rc6.1.1mdv2010.1
+ Revision: 499531
- update to 2.6.33-rc6-git1

* Fri Jan 29 2010 Thomas Backlund <tmb@mandriva.org> 2.6.33-0.rc6.1mdv2010.1
+ Revision: 498342
- update to 2.6.33-rc6

* Tue Jan 26 2010 Thomas Backlund <tmb@mandriva.org> 2.6.33-0.rc5.2.1mdv2010.1
+ Revision: 496874
- update to 2.6.33-rc5-git2

* Fri Jan 22 2010 Thomas Backlund <tmb@mandriva.org> 2.6.33-0.rc5.1mdv2010.1
+ Revision: 494855
- update to 2.6.33-rc5

* Sun Jan 17 2010 Thomas Backlund <tmb@mandriva.org> 2.6.33-0.rc4.4.1mdv2010.1
+ Revision: 492611
- update to 2.6.33-rc4-git4

* Fri Jan 15 2010 Thomas Backlund <tmb@mandriva.org> 2.6.33-0.rc4.2.1mdv2010.1
+ Revision: 491919
- add 'static' symlinks in /boot
- update to 2.6.33-rc4-git2
- enable EXT3_DEFAULTS_TO_ORDERED as data=writeback is a security
  issue and makes a mess on system crash
- enable NAMESPACES support (like main kernel, noted by Thierry)

* Wed Jan 13 2010 Thomas Backlund <tmb@mandriva.org> 2.6.33-0.rc4.1mdv2010.1
+ Revision: 490498
- update to 2.6.33-rc4

* Tue Jan 12 2010 Thomas Backlund <tmb@mandriva.org> 2.6.33-0.rc3.5.1mdv2010.1
+ Revision: 490395
- 2.6.33-rc3-git5

* Thu Jan 07 2010 Thomas Backlund <tmb@mandriva.org> 2.6.33-0.rc3.2.1mdv2010.1
+ Revision: 487377
- update to 2.6.33-rc3-git2

* Wed Jan 06 2010 Thomas Backlund <tmb@mandriva.org> 2.6.33-0.rc3.1mdv2010.1
+ Revision: 486589
- update to 2.6.33-rc3

* Tue Jan 05 2010 Thomas Backlund <tmb@mandriva.org> 2.6.33-0.rc2.6.1mdv2010.1
+ Revision: 486411
- update to 2.6.33-rc2-git6

* Thu Dec 31 2009 Thomas Backlund <tmb@mandriva.org> 2.6.33-0.rc2.2.1mdv2010.1
+ Revision: 484418
- update to 2.6.33-rc2-git2

* Fri Dec 25 2009 Thomas Backlund <tmb@mandriva.org> 2.6.33-0.rc2.1mdv2010.1
+ Revision: 482178
- update defconfigs
- update to 2.6.33-rc2

* Thu Dec 24 2009 Thomas Backlund <tmb@mandriva.org> 2.6.33-0.rc1.4.1mdv2010.1
+ Revision: 481931
- update to 2.6.33-rc1-git4
- re-enable wireless extensions (CFG80211_WEXT) that got disabled by mistake
- enable DEVTMPFS on x86_64 too, noted by Thierry

* Sun Dec 20 2009 Thomas Backlund <tmb@mandriva.org> 2.6.33-0.rc1.1.1mdv2010.1
+ Revision: 480437
- update to 2.6.33-rc1-git1
- disable MULTICORE_RAID456, it's not production ready (reported by Anssi)

* Fri Dec 18 2009 Thomas Backlund <tmb@mandriva.org> 2.6.33-0.rc1.1mdv2010.1
+ Revision: 479924
- add include/generated/* to -devel rpm
- include/asm* symlinks does not exist anymore
- rediff patches to apply cleanly
- update defconfigs
- update to 2.6.33-rc1

* Mon Dec 14 2009 Thomas Backlund <tmb@mandriva.org> 2.6.32.1-1mdv2010.1
+ Revision: 478634
- update to 2.6.32.1

* Thu Dec 03 2009 Thomas Backlund <tmb@mandriva.org> 2.6.32-1mdv2010.1
+ Revision: 472804
- update to 2.6.32 final

* Tue Nov 24 2009 Thomas Backlund <tmb@mandriva.org> 2.6.32-0.rc8.1.1mdv2010.1
+ Revision: 469673
- update to 2.6.32-rc8-git1

* Wed Nov 18 2009 Pascal Terjan <pterjan@mandriva.org> 2.6.32-0.rc7.1.1mdv2010.1
+ Revision: 467317
- Update to 2.6.32-rc7-git1

* Tue Nov 10 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31.6-1mdv2010.1
+ Revision: 464211
- update to 2.6.31.6 (CVE-2009-3612, CVE-2009-3621)

* Sat Oct 24 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31.5-1mdv2010.0
+ Revision: 459145
- update to 2.6.31.5

* Tue Oct 13 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31.4-1mdv2010.0
+ Revision: 457149
- update to 2.6.31.4 (CVE-2009-2903)

* Thu Oct 08 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31.3-1mdv2010.0
+ Revision: 456071
- update to 2.6.31.3 (tty_port bug)

* Mon Oct 05 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31.2-1mdv2010.0
+ Revision: 454215
- sync defconfigs with main kernel
- update to 2.6.31.2

* Thu Sep 24 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31.1-1mdv2010.0
+ Revision: 448457
- sync defconfigs with main kernel
- update to 2.6.31.1
- spec cleanups
- parallelize xargs invocations on smp machines

* Thu Sep 10 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31-1mdv2010.0
+ Revision: 436349
- update to 2.6.31 final

* Sun Sep 06 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31-0.rc9.1mdv2010.0
+ Revision: 432070
- update to 2.6.31-rc9

* Sat Aug 29 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31-0.rc8.1.1mdv2010.0
+ Revision: 422197
- update to 2.6.31-rc8-git1

* Fri Aug 28 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31-0.rc8.1mdv2010.0
+ Revision: 421900
- update to 2.6.31-rc8
- re-enable DRM_I915_KMS

* Wed Aug 26 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31-0.rc7.4.1mdv2010.0
+ Revision: 421573
- sync defconfigs with main kernel
- update to 2.6.31-rc7-git4

* Sat Aug 22 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31-0.rc7.2mdv2010.0
+ Revision: 419719
- bump release to get past BS
- disable MAC80211_DEFAULT_PS (powersaving) as it's known to cause instabilities
  and performance regressions on wireless drivers including iwlwifi and p54.
- update to 2.6.31-rc7

* Fri Aug 14 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31-0.rc6.1mdv2010.0
+ Revision: 416263
- update to 2.6.31-rc6

* Thu Aug 13 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31-0.rc5.9.1mdv2010.0
+ Revision: 415936
- sync defconfigs with main kernel
- update to 2.6.31-rc5-git9

* Fri Aug 07 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31-0.rc5.3.1mdv2010.0
+ Revision: 411281
- update to 2.6.31-rc5-git3

* Sat Aug 01 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31-0.rc5.1mdv2010.0
+ Revision: 405306
- update to 2.6.31-rc5

* Thu Jul 30 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31-0.rc4.4.1mdv2010.0
+ Revision: 404491
- update to 2.6.31-rc4-git4

* Tue Jul 28 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31-0.rc4.1.1mdv2010.0
+ Revision: 401434
- sync defconfigs with main kernel
- update to 2.6.31-rc4-git1

* Thu Jul 23 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31-0.rc4.1mdv2010.0
+ Revision: 398798
- update to 2.6.31-rc4

* Sun Jul 19 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31-0.rc3.4.3mdv2010.0
+ Revision: 397450
- update to 2.6.31-rc3-git4

* Sat Jul 18 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31-0.rc3.3.2mdv2010.0
+ Revision: 396965
- update to 2.6.31-rc3-git3

* Tue Jul 14 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31-0.rc3.1mdv2010.0
+ Revision: 395833
- update to 2.6.31-rc3

* Fri Jul 10 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31-0.rc2.5.3mdv2010.0
+ Revision: 394219
- update to 2.6.31-rc2-git5

* Sun Jul 05 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31-0.rc2.2mdv2010.0
+ Revision: 392595
- bump release to get past BS
- update to 2.6.31-rc2

* Thu Jun 25 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31-0.rc1.1mdv2010.0
+ Revision: 389080
- disable I2C_DESIGNWARE, COMEDI and VT6655 as they break the build
- update to 2.6.31-rc1

* Fri Jun 19 2009 Thomas Backlund <tmb@mandriva.org> 2.6.30-2mdv2010.0
+ Revision: 387291
- Unset CONFIG_UEVENT_HELPER_PATH, installer was adapted to not need
  this set in kernel config.
- Disabled CONFIG_COMEDI_PCI_DRIVERS. At least one module built with
  it enabled (s626) claims the pci id 1131:7146 for all subvendors
  and subdevice ids. The problem is that this will clash with many
  media/dvb cards that have the same main pci vendor and device ids,
  but properly specify/check subvendor and subdevice ids. For now
  just disable comedi pci drivers, in this specific case s626
  probably would need a specific subvendor/subdevice restriction in
  its pci id table or additional checks to avoid freezing when it is
  loaded on media/dvb cards with same vendor:device pci id. (#51314)
- set 32bit defconfig to i586, so all can use it

* Wed Jun 10 2009 Thomas Backlund <tmb@mandriva.org> 2.6.30-1mdv2010.0
+ Revision: 384769
- 2.6.30 final is out

* Thu Jun 04 2009 Thomas Backlund <tmb@mandriva.org> 2.6.30-0.rc8.1mdv2010.0
+ Revision: 382637
- enable SECURITY_TOMOYO again
- update to 2.6.30-rc8

* Mon May 25 2009 Thomas Backlund <tmb@mandriva.org> 2.6.30-0.rc7.2mdv2010.0
+ Revision: 379656
- resync defconfigs with main kernel
- disable TOMOYO as it breaks su (#51076)

* Sun May 24 2009 Thomas Backlund <tmb@mandriva.org> 2.6.30-0.rc7.1mdv2010.0
+ Revision: 379140
- update to 2.6.30-rc7

* Wed May 20 2009 Thomas Backlund <tmb@mandriva.org> 2.6.30-0.rc6.5.1mdv2010.0
+ Revision: 378082
- update defconfigs
- updte to 2.6.30-rc6-git5

* Sat May 16 2009 Thomas Backlund <tmb@mandriva.org> 2.6.30-0.rc6.2mdv2010.0
+ Revision: 376479
- bump release to get it past BS
- update to 2.6.30-rc6

* Sun May 10 2009 Thomas Backlund <tmb@mandriva.org> 2.6.30-0.rc5.1mdv2010.0
+ Revision: 374023
- remove microblaze arch from source and devel rpms
- update to 2.6.30-rc5

* Mon Apr 27 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29.2-1mdv2010.0
+ Revision: 369080
- update to 2.6.29.2: CVE-2009-1192, CVE-2009-0795
    * http://www.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.29.2

* Fri Apr 03 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29.1-1mdv2009.1
+ Revision: 363671
- update to 2.6.29.1

* Tue Mar 24 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-1mdv2009.1
+ Revision: 360871
- update to 2.6.29 final

* Fri Mar 13 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc8.1mdv2009.1
+ Revision: 354597
- update to 2.6.29-rc8

* Tue Mar 10 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc7.3.1mdv2009.1
+ Revision: 353464
- update to 2.6.29-rc7-git3

* Sat Mar 07 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc7.1.1mdv2009.1
+ Revision: 351777
- update to 2.6.29-rc7-git1

* Wed Mar 04 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc7.1mdv2009.1
+ Revision: 348224
- update to 2.6.29-rc7
- update to 2.6.29-rc6-git5
- update to 2.6.29-rc6-git1

* Mon Feb 23 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc6.2mdv2009.1
+ Revision: 344318
- add drivers/acpi/acpica header files to -devel rpms, needed by fglrx

* Mon Feb 23 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc6.1mdv2009.1
+ Revision: 344074
- update to 2.6.29-rc6

* Sat Feb 21 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc5.5.1mdv2009.1
+ Revision: 343699
- update to 2.6.29-rc5-git5

* Sat Feb 14 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc5.1mdv2009.1
+ Revision: 340288
- update to 2.6.29-rc5

* Mon Feb 09 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc4.1.1mdv2009.1
+ Revision: 338754
- update to 2.6.29-rc4-git1
  * fixes error case in mlock downgrade reversion

* Sun Feb 08 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc4.1mdv2009.1
+ Revision: 338619
- update defconfigs
- make HID core modular too
- try to build MFD_PCF50633 again
- update to 2.6.29-rc4

* Sun Feb 01 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc3.1mdv2009.1
+ Revision: 336059
- disable MFD_PCF50633 again as its still broken
- re-enable MFD_PCF50633
- update defconfigs
- update to 2.6.29-rc3

* Sun Jan 18 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc2.1mdv2009.1
+ Revision: 331024
- disable CONFIG_MFD_PCF50633 as it breaks the build
- reset releaseversion
- make CONFIG_IDE mudular like main kernel
- update defconfigs
- enable TOSHIBA_FIR again
- update to 2.6.29-rc2

* Sun Jan 11 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc1.2mdv2009.1
+ Revision: 328263
- bump release to get it past broken bs
- arch/x86/kernel/sigframe.h does not exist anymore
- disable TOSHIBA_FIR as it breaks the build
- sparc and sparc64 trees have been merged
- update defconfigs
- update to 2.6.29-rc1

* Thu Dec 25 2008 Thomas Backlund <tmb@mandriva.org> 2.6.28-1mdv2009.1
+ Revision: 318538
- update to 2.6.28 final

* Fri Dec 19 2008 Thomas Backlund <tmb@mandriva.org> 2.6.28-0.rc9.1mdv2009.1
+ Revision: 316355
- update defconfigs
- update to 2.6.28-rc9

* Mon Dec 15 2008 Thomas Backlund <tmb@mandriva.org> 2.6.28-0.rc8.3.1mdv2009.1
+ Revision: 314561
- update to 2.6.28-rc8-git3

* Mon Dec 08 2008 Thomas Backlund <tmb@mandriva.org> 2.6.28-0.rc7.6.1mdv2009.1
+ Revision: 311967
- update to 2.6.27-rc7-git6

* Wed Nov 19 2008 Thomas Backlund <tmb@mandriva.org> 2.6.28-0.rc5.2mdv2009.1
+ Revision: 304615
- simplify build process as we now build a single kernel
- update summary and description
- rename defconfigs
- obsolete smp-latest and smp-devel-latest
- specfile cleanups
- drop smp tag
- drop up kernel

* Sun Nov 16 2008 Thomas Backlund <tmb@mandriva.org> 2.6.28-0.rc5.1mdv2009.1
+ Revision: 303620
- update to 2.6.28-rc5

* Mon Nov 10 2008 Thomas Backlund <tmb@mandriva.org> 2.6.28-0.rc4.1mdv2009.1
+ Revision: 301812
- update defconfigs
- update to 2.6.28-rc4

* Mon Nov 03 2008 Thomas Backlund <tmb@mandriva.org> 2.6.28-0.rc3.1mdv2009.1
+ Revision: 299323
- update defconfigs
- update to 2.6.28-rc3

* Sun Oct 26 2008 Thomas Backlund <tmb@mandriva.org> 2.6.28-0.rc2.1mdv2009.1
+ Revision: 297517
- update to 2.6.28-rc2
- enable WIRELESS_OLD_REGULATORY to not break old userspace apps
- add include/trace to devel and source tree
- include/asm-um has been removed from tree
- include/asm-<arch> has been moved to arch/<arch>/include/asm
- update defconfigs
- update to 2.6.28-rc1-git1

* Thu Oct 23 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.27.3-1mdv2009.1
+ Revision: 296617
- Update to 2.6.27.3

* Sun Oct 19 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.6.27.2-1mdv2009.1
+ Revision: 295204
- Update to 2.6.27.2

* Thu Oct 16 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27.1-1mdv2009.1
+ Revision: 294483
- update to 2.6.27.1
  * disables CONFIG_DYNAMIC_FTRACE due to possible memory corruption
    on module unload (this is the reason e1000e cards broke)

* Fri Oct 10 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-1mdv2009.1
+ Revision: 291531
- update to 2.6.27 final

* Thu Oct 02 2008 Pascal Terjan <pterjan@mandriva.org> 2.6.27-0.rc8.3.1mdv2009.0
+ Revision: 290879
- Update to 2.6.27-rc8-git3 (contains e1000e workaround)

* Sun Sep 28 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-0.rc7.5.1mdv2009.0
+ Revision: 289102
- update to 2.6.27-rc7-git5
- update to 2.6.27-rc7-git4

* Wed Sep 10 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-0.rc6.1mdv2009.0
+ Revision: 283527
- update to 2.6.27-rc6

* Thu Sep 04 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-0.rc5.6.1mdv2009.0
+ Revision: 280816
- use same defconfigs as main in order to make it easier to
  find regressions introduced by patches in main kernel.
- update to 2.6.27-rc5-git6

* Fri Aug 29 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-0.rc5.1mdv2009.0
+ Revision: 277322
- update to 2.6.27-rc5

* Thu Aug 28 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-0.rc4.7.2mdv2009.0
+ Revision: 277041
- update to 2.6.27-rc4-git7

* Thu Aug 21 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-0.rc4.1mdv2009.0
+ Revision: 274522
- update to 2.6.27-rc4

* Wed Aug 20 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-0.rc3.6.1mdv2009.0
+ Revision: 274204
- update to 2.6.27-rc3-git6

* Thu Aug 07 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-0.rc2.2mdv2009.0
+ Revision: 265923
- spec filea cleanups
- remove include/asm symlink from -source
- fox more typos in spec
- check and clean -devel tree before we disable mrproper and other targets~
- dont prepare kernel-source tree
- dont remove bounds.h and asm-offsets.k from -devel rpms
- remove /lib/firmware, we use the separate kernel-firmware rpm
- require the newly added kernel-firmware
- drop kernel-linus-firmware
- add provides should-restart = system

* Wed Aug 06 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-0.rc2.1mdv2009.0
+ Revision: 264183
- update defconfigs
- update to 2.6.27-rc2
- move kernel firmwares to a separate rpm

* Sat Aug 02 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-0.rc1.2.1mdv2009.0
+ Revision: 260687
- drop 'git' from release to satisfy rpm versioning
- update to 2.6.27-rc1-git2
- kernel firmwares are now in /lib/firmware
- add /include/drm to -devel and -source rpms
- add /firmware to -source and -devel rpms
- disable IWLWIFI_LEDS and IWL4965_LEDS as they are  broken
- update defconfigs
- update disable-mrproper patch to apply cleanly
- update to 2.6.27-rc1

* Thu Jul 24 2008 Thomas Backlund <tmb@mandriva.org> 2.6.26-2mdv2009.0
+ Revision: 245390
- drop spec fix for #29744, #29074 (not needed anymore)
- update disable-mrproper patch to the same used in main and tmb series

* Mon Jul 14 2008 Thomas Backlund <tmb@mandriva.org> 2.6.26-1mdv2009.0
+ Revision: 234411
- update to 2.6.26 final

  + trem <trem@mandriva.org>
    - update to 2.6.26-rc9-git5

* Sun Jul 06 2008 Thomas Backlund <tmb@mandriva.org> 2.6.26-0.rc9.1mdv2009.0
+ Revision: 232067
- add dvb-core header files to -devel rpms so it's possible to build
  external dvb drivers without needing full source (#41418)
- do not remove modules.* before calling depmod in install
  (fixes missing modules.order file, noted by Anssi)
- spec fixes
- update to 2.6.26-rc9

* Thu Jun 26 2008 trem <trem@mandriva.org> 2.6.26-0.rc8.1mdv2009.0
+ Revision: 229181
- update to 2.6.26-rc8

* Mon Jun 16 2008 Thomas Backlund <tmb@mandriva.org> 2.6.26-0.rc6.git3.1mdv2009.0
+ Revision: 220677
- update to 2.6.26-rc6-git3
- disable CONFIG_USB_RIO500, as it will switch to libusb (#41504)
- update to 2.6.26-rc6
- remove -doc-latest as the -doc can be updated automatically
- fix spec for disabled -doc build

  + Luiz Fernando Capitulino <lcapitulino@mandriva.com>
    - Enable SLUB object allocator (disables SLAB)

* Thu Jun 05 2008 Thomas Backlund <tmb@mandriva.org> 2.6.26-0.rc5.1mdv2009.0
+ Revision: 215259
- update to 2.6.26-rc5

* Tue May 27 2008 trem <trem@mandriva.org> 2.6.26-0.rc4.1mdv2009.0
+ Revision: 211906
- update to 2.6.26-rc4
- update to 2.6.23-rc3-git7
- update the disable-mrproper patch

* Mon May 19 2008 trem <trem@mandriva.org> 2.6.26-0.rc3.1mdv2009.0
+ Revision: 208849
- update to 2.6.26-rc3

* Fri May 16 2008 trem <trem@mandriva.org> 2.6.26-0.rc2.git5.1mdv2009.0
+ Revision: 208147
- update to 2.6.26-rc2-git5

* Sun May 11 2008 Thomas Backlund <tmb@mandriva.org> 2.6.26-0.rc1.git7.1mdv2009.0
+ Revision: 205934
- fix -devel rpms
- update to 2.6.26-rc1-git7
- update to 2.6.26-rc1

* Fri May 02 2008 trem <trem@mandriva.org> 2.6.25.1-1mdv2009.0
+ Revision: 199963
- update to 2.6.25.1
- revert git change
- add -git to the kernel version
- update to 2.6.25-git17

* Thu Apr 17 2008 trem <trem@mandriva.org> 2.6.25-1mdv2009.0
+ Revision: 195432
- update to 2.6.25
- update to 2.6.25-rc9
- update to 2.6.25-rc8
- update to 2.6.25-rc7

* Mon Mar 24 2008 Thomas Backlund <tmb@mandriva.org> 2.6.25-0.rc6.1mdv2008.1
+ Revision: 189735
- update defconfigs
- fix license
- update to 2.6.25-rc6

* Mon Mar 10 2008 Thomas Backlund <tmb@mandriva.org> 2.6.25-0.rc5.1mdv2008.1
+ Revision: 183416
- update to 2.6.25-rc5

* Wed Mar 05 2008 Thomas Backlund <tmb@mandriva.org> 2.6.25-0.rc4.1mdv2008.1
+ Revision: 180028
- update to 2.6.25-rc4

* Mon Feb 25 2008 Thomas Backlund <tmb@mandriva.org> 2.6.25-0.rc3.1mdv2008.1
+ Revision: 174835
- disable LGUEST support as it's broken
- update defconfigs
- update to 2.6.25-rc3

* Sun Feb 17 2008 trem <trem@mandriva.org> 2.6.25-0.rc2.1mdv2008.1
+ Revision: 169623
- update to 2.6.25-rc2

* Thu Feb 14 2008 trem <trem@mandriva.org> 2.6.25-0.rc1.1mdv2008.1
+ Revision: 167198
- stop removing "%%{target_source}/arch/i386/boot/bzImage" on i386
- update to 2.6.25-rc1

* Mon Feb 11 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24.2-1mdv2008.1
+ Revision: 165121
- update to 2.6.24.2 (CVE-2008-0600)

* Sat Feb 09 2008 trem <trem@mandriva.org> 2.6.24.1-1mdv2008.1
+ Revision: 164485
- update to 2.6.24.1

* Sat Jan 26 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24-1mdv2008.1
+ Revision: 158253
- update to 2.6.24 final

* Thu Jan 24 2008 trem <trem@mandriva.org> 2.6.24-0.rc8.3mdv2008.1
+ Revision: 157717
- update to 2.6.24-rc8-git8

* Thu Jan 24 2008 trem <trem@mandriva.org> 2.6.24-0.rc8.2mdv2008.1
+ Revision: 157285
- update to 2.6.24-rc8-git5

* Sun Jan 20 2008 trem <trem@mandriva.org> 2.6.24-0.rc8.1mdv2008.1
+ Revision: 155388
- update to 2.6.24-rc8-git4
- update to 2.6.24-rc8-git3

  + Thomas Backlund <tmb@mandriva.org>
    - update to 2.6.24-rc8-git2
    - make 32bit kernels conflict arch(x86_64) so they cant be installed
      by mistake (#32631)

* Mon Jan 07 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24-0.rc7.1mdv2008.1
+ Revision: 146151
- change url to Mandriva wiki
- use make clean on -devel & source tree to not ship unneeded files
- fix build,source symlinks to -source tree to be created only if no
  matching -devel tree is installed, and to be removed only if they
  point at the -source tree
- update to 2.6.24-rc7

* Mon Dec 31 2007 Thomas Backlund <tmb@mandriva.org> 2.6.24-0.rc6.2mdv2008.1
+ Revision: 139812
- drop README.urpmi
- update source2 to apply cleanly
- remove /arch/i386/boot/bzImage symlink from kernel-source
- fix kernelupdate weblink
- update to 2.6.24-rc6-git7

* Sun Dec 23 2007 trem <trem@mandriva.org> 2.6.24-0.rc6.1mdv2008.1
+ Revision: 137271
- update to 2.6.24-rc6
- update to 2.6.24-rc6

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Dec 11 2007 Thomas Backlund <tmb@mandriva.org> 2.6.24-0.rc5.1mdv2008.1
+ Revision: 117424
- update to kernel.org 2.6.24-rc5
- update defconfigs

* Tue Dec 04 2007 Thomas Backlund <tmb@mandriva.org> 2.6.24-0.rc4.1mdv2008.1
+ Revision: 115449
- update to kernel.org 2.6.24-rc4-git1
- update defconfigs
- call installkernel with -L to avoid changing main kernel
  default symlinks

* Sun Nov 18 2007 Thomas Backlund <tmb@mandriva.org> 2.6.24-0.rc3.1mdv2008.1
+ Revision: 109995
- update to kernel.org 2.6.24-rc3-git1
- adapt specfile for i386/x86_64 merge into x86
- update defconfigs

* Sun Oct 14 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23.1-1mdv2008.1
+ Revision: 98270
- update to kernel.org 2.6.23.1
- disable mrproper target on -devel rpms to stop 3rdparty installers
  from wiping out needed files and thereby breaking builds
  (based on an initial patch by Danny used in kernel-multimedia series)

* Thu Oct 11 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23-1mdv2008.1
+ Revision: 96953
- update to kernel.org 2.6.23 final

  + trem <trem@mandriva.org>
    - back to kernel.org 2.6.23-rc8-git2
    - update to kernel.org 2.6.23-rc8-git4

* Fri Sep 28 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23-0.rc8.1mdv2008.0
+ Revision: 93689
- update to kernel.org 2.6.23-rc8-git2 (fixes CVE-2007-4571)

* Sun Sep 23 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23-0.rc7.2mdv2008.0
+ Revision: 92344
- update to kernel.org 2.6.23-rc7-git4 (fixes CVE-2007-4573)

* Thu Sep 20 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23-0.rc7.1mdv2008.0
+ Revision: 91544
- update to 2.6.23-rc7
- update defconfigs

* Thu Sep 13 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23-0.rc6.1mdv2008.0
+ Revision: 85321
- update to 2.6.23-rc6-git4

* Thu Sep 06 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23-0.rc5.2mdv2008.0
+ Revision: 81270
- update to 2.6.23-rc5-git1

* Sat Sep 01 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23-0.rc5.1mdv2008.0
+ Revision: 77733
- update to kernel.org 2.6.23-rc5
- fix #29744, #29074 in a cleaner way by disabling the sourcing of
  arch/s390/crypto/Kconfig
- update defconfigs

* Mon Aug 13 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23-0.rc3.1mdv2008.0
+ Revision: 62739
- update to kernel.org 2.6.23-rc3

* Sat Aug 04 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23-0.rc2.1mdv2008.0
+ Revision: 58956
- add xen to source and devel rpms
- arm26 arch is now gone
- update to kernel.org 2.6.23-rc2
- update defconfigs

* Fri Aug 03 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22.1-2mdv2008.0
+ Revision: 58692
- disable DEBUG_SLAB, as it's bad for performance, especially
  under heavier loads
- dont build -doc rpms
- fix build when building only up or smp

* Wed Jul 11 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22.1-1mdv2008.0
+ Revision: 51432
- update to kernel.org 2.6.22.1
  * NETFILTER: {ip, nf}_conntrack_sctp: fix remotely triggerable
    NULL ptr dereference (CVE-2007-2876)

* Mon Jul 09 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-1mdv2008.0
+ Revision: 50492
- update to kernel.org 2.6.22 final
- update defconfigs, make IDE modular

* Tue Jul 03 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc7.1mdv2008.0
+ Revision: 47488
- update to kernel.org 2.6.22-rc7
- add support for git patches
- update to 2.6.22-rc7-git1

* Mon Jun 25 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc6.1mdv2008.0
+ Revision: 44020
- update to kernel.org 2.6.22-rc6
- make buildroot arch-specific to allow dual build in same rpm tree
- update defconfig

* Sun Jun 24 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc5.2mdv2008.0
+ Revision: 43702
- kernel-devel rpms does not provide kernel-source anymore
- re-add build,source symlink logic to kernel-source as dkms needs it
  and can cope with the Makefile version mismatch
- update README.urpmi regarding the symlinks

* Sun Jun 17 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc5.1mdv2008.0
+ Revision: 40516
- update to kernel.org 2.6.22-rc5

* Tue Jun 05 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc4.1mdv2008.0
+ Revision: 35800
- update to kernel.org 2.6.22-rc4

* Sun May 27 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc3.1mdv2008.0
+ Revision: 31873
- provide versioned kernel-devel and kernel-source (MDV #31006)
- update to kernel.org 2.6.22-rc3

* Tue May 22 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc2.1mdv2008.0
+ Revision: 29732
- remove blackfin arch files
- update to kernel.org 2.6.22-rc2
- disable CONFIG_IRQBALANCE on i386-smp, in favour of the better
  working userspace irqbalance daemon from contribs (Requested by Austin)
- update defconfigs

* Fri May 18 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21.1-2mdv2008.0
+ Revision: 28291
- /sbin/depmod-25 is now renamed to /sbin/depmod
- modify kernel-linus-source description to point out:
  * only needed when building own kernels
  * othervise install a matching -devel- rpm
- update README.urpmi for the same reason
- enable CONFIG_TIMER_STATS (request by Michael Braun)

* Sat Apr 28 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21.1-1mdv2008.0
+ Revision: 19047
- kernel.org 2.6.21.1
  * IPV6: Fix for RT0 header ipv6 change
  * IPV4: Fix OOPS'er added to netlink fib
- Enable Tickless System (Dynamic Ticks (NO_HZ)) on i386 kernels

* Fri Apr 27 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-2mdv2008.0
+ Revision: 18743
- revert read-only -devel rpms until I find a better solution...

* Fri Apr 27 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-1mdv2008.0
+ Revision: 18448
- update to kernel.org 2.6.21 final
- make devel trees read-only (like in kernel-multimedia series),
  to try and work around broken dkms & co

* Sun Apr 22 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-0.rc7.1mdv2008.0
+ Revision: 17010
- update to 2.6.21-rc7
- update defconfigs
- enable CONFIG_X86_P4_CLOCKMOD again
- fix README.urpmi on -rc and -stable builds
- add drivers/md/dm.h to -devel rpms, needed for truecrypt builds (Danny)


* Wed Mar 21 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-0.rc3.4mdv2007.1
+ Revision: 147144
- add arch/s390/crypto/Kconfig for now, until fixed upstream,
  closes #29074, and fixes kernel-linus part of #29744

* Sun Mar 18 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-0.rc3.3mdv2007.1
+ Revision: 145685
- fix typo in -devel post script (Charles A Edwards)
- make the build work even if you only build up or smp (Charles A Edwards)
- fix typo in -smp-devel post script

* Tue Mar 13 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-0.rc3.2mdv2007.1
+ Revision: 142330
- CFQ is now the default i/o scheduler
- fix typo in post script (#29395)

* Wed Mar 07 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-0.rc3.1mdv2007.1
+ Revision: 134183
- update to kernel.org 2.6.21-rc3
- disable CONFIG_X86_P4_CLOCKMOD (broken build)
- update defconfigs

* Tue Mar 06 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-0.rc2.2mdv2007.1
+ Revision: 133974
- rename *-headers rpms to more appropriate *-devel
- make make *-devel-latest obsolete *-headers-latest to enable automatic update
- disable CONFIG_ACORN_PARTITION_CUMANA (#29006)

* Wed Feb 28 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-0.rc2.1mdv2007.1
+ Revision: 127920
- add patch101: fixes build on i386 and x86_64, from upsrteam linux-2.6.git,
  will be removed when 2.6.21-rc3 is released.
- update README.urpmi
- update to kernel.org 2.6.21-rc2
- update defconfigs

* Sat Feb 24 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-0.rc1.1mdv2007.1
+ Revision: 125309
- update to kernel.org 2.6.21-rc1
- update defconfigs

* Wed Feb 21 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.1-2mdv2007.1
+ Revision: 123564
- add missing /arch/i386/kernel/sigframe.h in header rpms (#28843)

* Wed Feb 21 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.1-1mdv2007.1
+ Revision: 123207
- update to kernel.org 2.6.21.1
  o Fix a free-wrong-pointer bug in nfs/acl server (CVE-2007-0772)

* Mon Feb 19 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20-3mdv2007.1
+ Revision: 122863
- add README.urpmi with info specific for this kernel set
- drop all patches, this kernel _has_ to stay unpatched, as it's
  a precompiled kernel.org reference kernel

* Sat Feb 17 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20-2mdv2007.1
+ Revision: 122200
- add bugfixes from upcoming 2.6.20.1 (will be removed when it's released)
  01_fix-missing-critical-phys_to_virt-in-lib_swiotlb.patch
  02_ieee1394-video1394-DMA-fix.patch
  03_ieee1394-fix-host-device-registering-when-nodemgr-disabled.patch
  04_fix-oops-in-xfrm_audit_log.patch
  05_md-raid5-fix-crash.patch
  06_md-raid5-fix-export-blk_recount_segments.patch
- fix the whole autoconf mess
  dont rely on /etc/init.d/kheader and /boot/kernel.h anymore
  drop all of the old autoconf hacks
  drop kernel-linus-source-stripped(-latest) rpms
  introduce kernel-linus-(smp-)headers(-latest) rpms to build 3rdparty
  drivers against (survives test: make mrproper oldconfig prepare scripts)
  kernel-linus-source rpm does not include any autoconf stuff anymore
- enable KVM support (requested by ahasenack)
- fix RC versioning

* Mon Feb 05 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20-1mdv2007.1
+ Revision: 116211
- update to kernel.org 2.6.20 final

* Wed Jan 31 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.0.rc7-1mdv2007.1
+ Revision: 115724
- update to kernel.org: 2.6.20-rc7

* Thu Jan 25 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.0.rc6-1mdv2007.1
+ Revision: 113431
- update to kernel.org: 2.6.20-rc6

* Tue Jan 16 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.0.rc5-2mdv2007.1
+ Revision: 109626
- fix install breakage due to spec cleanup (thanks Charles)
- fix kernel versioning mismatch (#28237)

* Sun Jan 14 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.0.rc5-1mdv2007.1
+ Revision: 108943
- finally move on to 2.6.20-rc5

* Thu Jan 11 2007 Thomas Backlund <tmb@mandriva.org> 2.6.19.2-1mdv2007.1
+ Revision: 107284
- kernel.org 2.6.19.2 (CVE: 2006-6106, 2006-6053, 2006-5823, 2006-6054, 2006-4814, file corruption fix, ...)
- disable BLK_DEV_UB (#28058)
- big spec cleanup: remove arches and flavours we dont build
- fix more provides
- fix source-stripped provides

* Sun Jan 07 2007 Thomas Backlund <tmb@mandriva.org> 2.6.19.1-2mdv2007.1
+ Revision: 105375
- fix utsrelease temporary location grep on i586 build
- fix the file content corruption bug that appeared in 2.6.19. Will be remowed when 2.6.19.2 is released
- finally add the *-latest virtual rpms
- fix UTS_RELEASE define in /include/linux/utsrelease.h (#28014)

* Tue Dec 12 2006 Thomas Backlund <tmb@mandriva.org> 2.6.19.1-1mdv2007.1
+ Revision: 95986
- fix autoconf
- update to kernel.org 2.6.19.1

* Wed Dec 06 2006 Thomas Backlund <tmb@mandriva.org> 2.6.19-3mdv2007.1
+ Revision: 91725
- fix patch command
- enable ARPD, IPV6_MIP6, IPV6_MULTIPLE_TABLES, IPV6_ROUTE_FWMARK, CONFIG_GFS2_FS, GFS2_FS_LOCKING_NOLOCK, GFS2_FS_LOCKING_DLM (#27479)
- Revert ACPI: SCI interrupt source override, will be removed when 2.6.19.1 is released

* Sun Dec 03 2006 Thomas Backlund <tmb@mandriva.org> 2.6.19-2mdv2007.1
+ Revision: 90141
- rename kernel-2.6-linus to kernel-linus in SVN
- rename spec to kernel-linus
- fix kernel-linus srpm name (Anssi Hannula)
- update to 2.6.19 final
- update specfile for 2.6.19-rc6
- update to 2.6.19-rc6
- bump release to allow reupload
- update to 2.6.19-rc5
- add support for stable series kernels
- update to 2.6.18 final
- update to 2.6.18-rc7
- fix spec for missing UTS_RELEASE (#24889)
- fix autoconf UTS_RELEASE
- update to 2.6.18-rc6
- fix autoconf for 2.6.18 auto.conf
- source and source-stripped needs to conflict each other
- use mkrel and distsuffix to make it work for backports
- update README.kernel-sources
- spec cosmetics
- dont build debug packages
- fix autoconf breakage due to bootloader-utils-1.13 change
- update for next build
- fix changelog
- fix release
- update to 2.6.18-rc5
- fix kernel-doc versioning and a rpmlint warning
- update to 2.6.18-rc4

  + Per Øyvind Karlsen <pkarlsen@mandriva.com>
    - fix typo
    - Fix target_arch for sparc64

  + Luiz Fernando Capitulino <lcapitulino@mandriva.com>
    - Updates to 2.6.18-rc2
    - Updates to 2.6.18-rc1
    - Updates to 2.6.17
    - Version reset: when I started with kernel-linus I wasn't too
      experienced with RPM packages and thought that packages' version
      should never been reset. Doing it now.
    - Adds new Mandriva tag
    - Updates to 2.6.17-rc6
    - Updates to 2.6.17-rc5
    - Updates to 2.6.17-rc4
    - Fixes 'kernel-source is upgraded but kernel is not' bug (#21345)
    - Introduces PPC support, patch and .config files from Christiaan Welvaart
      <cjw@daneel.dyndns.org>
    - x86 .configs update, the following changes have been made:
        o OBSOLETE and non-sense options have been disabled
        o New drivers and other interesting options (which were probably
          not automatically enabled by the bot) have been enabled
        o SMP kernel now supports: cpusets, 32 CPUs and 64 GB of memory
    - Updates sparc64 .config files, patch from Per Oyvind Karlsen
      <pkarlsen@mandriva.com>
    - Updates to 2.6.17-rc3
    - Updates sparc64 .config files, patch from Per Oyvind Karlsen
      <pkarlsen@mandriva.com>
    - This patch makes kernel image 'gzipped', it's needed to make it
      boot properly (and also makes sparc's kernel image consistent with
      other archs). Patch from Per Oyvind Karlsen <pkarlsen@mandriva.com>.
    - Updates to 2.6.17-rc2
    - Updates sparc64 .config files, patch from Per Oyvind Karlsen
      <pkarlsen@mandriva.com>
    - Updates to 2.6.17-rc1
    - Updates to 2.6.16
    - Minor typo
    - Updates to 2.6.16-rc6
    - Updates to 2.6.16-rc5
    - Changes to the kernel's stack to 8k bytes, as this question is polemic
      in two sides (proprietary drivers and performance) let's stay with the
      kernel's default.
    - - Updates to 2.6.16-rc4
    - New version
    - Changes some SMP options as suggested by Arnaud Patard <apatard@mandriva.com>
      basically, we're dropping BKL preemption support (because this is not
      supposed to only run on desktop systems), enabling software suspend and
      CPU hotpluging.
    - Introduces sparc64 support (patches from Per Oyvind Karlsen
      <pkarlsen@mandriva.com>)
    - Updates to 2.6.16-rc3
    - Some times I'm really stupid: forgot to add the spec changelog entry
      and to change the package's version on r1723.
    - Enables CONFIG_CC_OPTIMIZE_FOR_SIZE, to try to get a smaller kernel and
      other benefits.
    - Introduces 'update_configs' script (from mdv2006 stable kernel)
    - Updates to 2.6.16-rc2
    - Minor log fix
    - Commit in behalf of Oden Eriksson <oeriksson@mandriva.com>:
      - Fixes kernel headers generation
      - Fixes SUBLEVEL change in the kernel`s Makefile
      - Minor cleanups
    - Improves klinus_notice
    - Adds a note (in the package description) about kernel-linus's nature
    - Minor log fix, rpm prints some warnings with you write '%%prep' in the
      changelog section
    - Fixes embarrassing bug which causes any *.config file to be copied
      to the build directory
    - Comments out removal of unwanted files in %%prep section, this doesn't
      seen to be needed anymore and can cause to wanted files to be removed too
    - Adds comments in the top file about kernel-linus known issues
    - New spec file name (kernel-2.6.spec is already used by other package)
    - Adds all the kernel's .config file as 'Source', that way they're
      included in the src.rpm
    - Updates to 2.6.16-rc1
    - Updating package version, this will be the next release
    - Merges kernel-2.6-linus simplifications into the trunk
      (svn merge -r 1362:1428 svn+ssh://svn.mandriva.com/svn/mdv/branches/cooker/kernel-2.6-linus/current .)
    - Disables CONFIG_HWMON_DEBUG_CHIP, it's only interesting for
      developers
    - Provides kernel-source package should provides 'kernel-source', this
      makes life easier when using dkms
    - Minor log fix
    - Updates to 2.6.15
    - Fixes kernel-source package generation
    - Updates TODO list
    - Enables compilation for more architectures
    - s/ppc64/powerpc/
    - Minor %%patchlevel fix
    - Fixes Makefile hardcoded values
    - Updated to 2.6.15-rc7
    - Fixes Makefile hardcoded values
    - reverts r1345 and r1344. I was going to update the package for 2.6.15-rc7
      but there are some things to be done before, like a new release and tons
      of fixes.
    - Updates .config files for 2.6.15-rc7
    - Updates to 2.6.15-rc7
    - Enables more archs
    - Minor Changes
    - Introduces TODO list
    - Minor spec file fixes
    - Changes package name to 'kernel-linus'
    - Update version
    - Fixes br0ken compile with our current i386.config
    - Update hardcoded value to make the thing compile
    - This is a new package, removes all the changelog entries and adds the
      relevant one
    - Err, time-stamp are created automatically during build time, this files
      pulled in at the initial import step.. They shouldn't be here.
    - Introduces 'kernel-2.6-linus' RPM package source tree. This new package
      will provide the latest -rc kernels from Linus.

  + Andreas Hasenack <andreas@mandriva.com>
    - renamed mdv to packages because mdv is too generic and it's hosting only packages anyway

