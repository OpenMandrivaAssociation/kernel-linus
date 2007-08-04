# -*- Mode: rpm-spec -*-
#
# (c) Mandriva
#
# The kernel-2.6-linus package (and so this spec file) is under development,
# it does mean:
#
#    1. You can have nasty surprises when playing with the package
#    generation
#
#    2. Is easier to go and come back from Mordor than adding a new
#    architecture support
#
#    3. A known architecture with just a missing .config shouldn't be too
#    hard, but as this spec changes too fast, it's likely to be broken
# 
#
# if you try to understand kernel numbering, read docs/kernel_naming

%define kernelversion	2
%define patchlevel	6
%define sublevel	23

# kernel Makefile extraversion is substituted by 
# kpatch/kstable wich are either 0 (empty), rc (kpatch) or stable release (kstable)
%define kpatch		rc2
%define kstable		0

# kernel.org -git patch
%define kgit		0

# this is the releaseversion
%define mdvrelease 	1

# This is only to make life easier for people that creates derivated kernels
# a.k.a name it kernel-tmb :)
%define kname 		kernel-linus

%define rpmtag		%distsuffix
%if %kpatch
%define rpmrel		%mkrel 0.%{kpatch}.%{mdvrelease}
%else
%define rpmrel		%mkrel %{mdvrelease}
%endif

# theese two never change, they are used to fool rpm/urpmi/smart
%define fakever		1
%define fakerel		%mkrel 1

# When we are using a pre/rc patch, the tarball is a sublevel -1
%if %kpatch
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}
%define tar_ver	  	%{kernelversion}.%{patchlevel}.%(expr %{sublevel} - 1)
%else
%if %kstable
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}.%{kstable}
%define tar_ver   	%{kernelversion}.%{patchlevel}.%{sublevel}
%else
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}
%define tar_ver   	%{kversion}
%endif
%endif
%define kverrel   	%{kversion}-%{rpmrel}

# used for not making too long names for rpms or search paths
%if %kpatch
%define buildrpmrel     0.%{kpatch}.%{mdvrelease}%{rpmtag}
%else
%define buildrpmrel     %{mdvrelease}%{rpmtag}
%endif

%define buildrel        %{kversion}-%{buildrpmrel}

%define klinus_notice NOTE: This kernel has no Mandriva patches and no third-party drivers.

# having different top level names for packges means that you have to remove them by hard :(
%define top_dir_name    %{kname}-%{_arch}

%define build_dir       ${RPM_BUILD_DIR}/%{top_dir_name}
%define src_dir         %{build_dir}/linux-%{tar_ver}

# disable useless debug rpms...
%define _enable_debug_packages  %{nil}
%define debug_package           %{nil}

# build defines
%define build_doc 0
%define build_source 1
%define build_devel 1

%define build_up 1
%define build_smp 1

%define distro_branch %(perl -pe '/(\\d+)\\.(\\d)\\.?(\\d)?/; $_="$1.$2"' /etc/mandriva-release)

# End of user definitions
%{?_without_up: %global build_up 0}
%{?_without_smp: %global build_smp 0}
%{?_without_doc: %global build_doc 0}
%{?_without_source: %global build_source 0}
%{?_without_devel: %global build_devel 0}

%{?_with_up: %global build_up 1}
%{?_with_smp: %global build_smp 1}
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

# Aliases for amd64 builds (better make source links?)
%define target_cpu	%(echo %{_target_cpu} | sed -e "s/amd64/x86_64/")
%define target_arch	%(echo %{_arch} | sed -e "s/amd64/x86_64/" -e "s/sparc/%{_target_cpu}/")

# src.rpm description
Summary: 	The Linux kernel (the core of the Linux operating system)
Name:           %{kname}
Version:        %{kversion}
Release:        %{rpmrel}
License: 	GPL
Group: 		System/Kernel and hardware
ExclusiveArch: 	%{ix86} x86_64 sparc64
ExclusiveOS: 	Linux
URL: 		http://www.kernel.org/

####################################################################
#
# Sources
#
### This is for full SRC RPM
Source0:        ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/linux-%{tar_ver}.tar.bz2
Source1:        ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/linux-%{tar_ver}.tar.bz2.sign

Source4:  README.kernel-sources
Source5:  README.MandrivaLinux
Source6:  README.kernel-linus.urpmi

Source20: i386.config
Source21: i386-smp.config
Source22: x86_64.config
Source23: x86_64-smp.config
Source24: sparc64.config
Source25: sparc64-smp.config


####################################################################
#
# Patches

#
# Patch0 to Patch100 are for core kernel upgrades.
#

# Pre linus patch: ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing

%if %kpatch
Patch1:         ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}.bz2
Source10:       ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}.bz2.sign
%endif
%if %kstable
Patch1:         ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/patch-%{kversion}.bz2
Source10:       ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/patch-%{kversion}.bz2.sign
%endif
# kernel.org -git
%if %kgit
Patch2:         ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/snapshots/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}-git%{kgit}.bz2
Source11:       ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/snapshots/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}-git%{kgit}.bz2.sign
%endif

#END
####################################################################

# Defines for the things that are needed for all the kernels
%define requires1 module-init-tools >= 3.0-%mkrel 7
%define requires2 mkinitrd >= 3.4.43-%mkrel 10
%define requires3 bootloader-utils >= 1.9
%define requires4 sysfsutils module-init-tools >= 0.9.15

%define kprovides kernel = %{tar_ver}, alsa

BuildRoot: 	%{_tmppath}/%{name}-%{kversion}-build-%{_arch}
Autoreqprov: 	no
BuildRequires: 	gcc module-init-tools >= 0.9.15

%description
Source package to build the Linux kernel.

%{klinus_notice}



#
# kernel: UP kernel
#

%package -n %{kname}-%{buildrel}
Version:	%{fakever}
Release:	%{fakerel}
Summary: 	The Linux kernel (the core of the Linux operating system)
Group: 	  	System/Kernel and hardware
Provides: 	module-info, %kprovides
Requires: 	%requires1
Requires: 	%requires2
Requires: 	%requires3
Requires: 	%requires4

%description -n %{kname}-%{buildrel}
The kernel package contains the Linux kernel (vmlinuz), the core of your
Mandriva Linux operating system. The kernel handles the basic functions
of the operating system: memory allocation, process allocation, device
input and output, etc.

For instructions for update, see:
http://www.mandriva.com/security/kernelupdate

%{klinus_notice}



#
# kernel-smp: Symmetric MultiProcessing kernel
#

%package -n %{kname}-smp-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Summary:  The Linux Kernel compiled for SMP machines
Group: 	  System/Kernel and hardware
Provides: %kprovides
Requires: %requires1
Requires: %requires2
Requires: %requires3
Requires: %requires4

%description -n %{kname}-smp-%{buildrel}
This package includes a SMP version of the Linux %{kversion} kernel. It is
required only on machines with two or more CPUs, although it should work
fine on single-CPU boxes.

For instructions for update, see:
http://www.mandriva.com/security/kernelupdate

%{klinus_notice}



#
# kernel-source: kernel sources
#

%package -n %{kname}-source-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Provides: %{kname}-source, kernel-source = %{kverrel}, kernel-devel = %{kverrel}
Provides: %{kname}-source-%{kernelversion}.%{patchlevel}
Requires: glibc-devel, ncurses-devel, make, gcc, perl
Summary:  The source code for the Linux kernel
Group:    Development/Kernel
Autoreqprov: no

%description -n %{kname}-source-%{buildrel}
The %{kname}-source package contains the source code files for the Linux 
kernel. Theese source files are only needed if you want to build your own 
custom kernel that is better tuned to your particular hardware.

If you only want the files needed to build 3rdparty (nVidia, Ati, dkms-*,...)
drivers against, install the *-devel-* rpm that is matching your kernel.

For instructions for update, see:
http://www.mandriva.com/security/kernelupdate

%{klinus_notice}



# 
# kernel-devel-up: stripped kernel sources 
#

%package -n %{kname}-devel-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Provides: kernel-devel = %{kverrel}
Summary:  The %{kname} devel files for 3rdparty modules build
Group:    Development/Kernel
Autoreqprov: no
Requires: glibc-devel, ncurses-devel, make, gcc, perl

%description -n %{kname}-devel-%{buildrel}
This package contains the kernel-devel files that should be enough to build 
3rdparty drivers against for use with %{kname}-%{buildrel}.

If you want to build your own kernel, you need to install the full 
%{kname}-source-%{buildrel} rpm.

%{klinus_notice}



# 
# kernel-devel-smp: stripped kernel sources 
#

%package -n %{kname}-smp-devel-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Provides: kernel-devel = %{kverrel}
Summary:  The %{kname}-smp devel files for 3rdparty modules build
Group:    Development/Kernel
Autoreqprov: no
Requires: glibc-devel, ncurses-devel, make, gcc, perl

%description -n %{kname}-smp-devel-%{buildrel}
This package contains the kernel-devel files that should be enough to build 
3rdparty drivers against for use with the %{kname}-smp-%{buildrel}.

If you want to build your own kernel, you need to install the full 
%{kname}-source-%{buildrel} rpm.

%{klinus_notice}



#
# kernel-doc: documentation for the Linux kernel
#

%package -n %{kname}-doc-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Summary:  Various documentation bits found in the kernel source
Group:    Books/Computer books

%description -n %{kname}-doc-%{buildrel}
This package contains documentation files form the kernel source. Various
bits of information about the Linux kernel and the device drivers shipped
with it are documented in these files. You also might want install this
package if you need a reference to the options that can be passed to Linux
kernel modules at load time.

For instructions for update, see:
http://www.mandriva.com/security/kernelupdate

%{klinus_notice}



#
# kernel-latest: virtual rpm
#

%package -n %{kname}-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-%{buildrel}

%description -n %{kname}-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname} installed...

%{klinus_notice}



#
# kernel-smp-latest: virtual rpm
#

%package -n %{kname}-smp-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-smp
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-smp-%{buildrel}

%description -n %{kname}-smp-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-smp installed...

%{klinus_notice}



#
# kernel-source-latest: virtual rpm
#

%package -n %{kname}-source-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-source
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-source-%{buildrel}

%description -n %{kname}-source-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-source installed...

%{klinus_notice}



#
# kernel-devel-latest: virtual rpm
#

%package -n %{kname}-devel-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-devel
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-devel-%{buildrel}
Obsoletes:	%{kname}-headers-latest

%description -n %{kname}-devel-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-devel installed...

%{klinus_notice}



#
# kernel-smp-devel-latest: virtual rpm
#

%package -n %{kname}-smp-devel-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-smp-devel
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-smp-devel-%{buildrel}
Obsoletes:	%{kname}-smp-headers-latest

%description -n %{kname}-smp-devel-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-smp-devel installed...

%{klinus_notice}



#
# kernel-doc-latest: virtual rpm
#

%package -n %{kname}-doc-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-doc
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-doc-%{buildrel}

%description -n %{kname}-doc-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-doc installed...

%{klinus_notice}



#
# End packages - here begins build stage
#
%prep
%setup -q -n %top_dir_name -c

pushd %src_dir
%if %kpatch
%patch1 -p1
%endif
%if %kstable
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

pushd ${RPM_SOURCE_DIR}

#
# Copy our defconfigs into place.
for i in i386 sparc64 x86_64; do
	cp -f $i.config %{build_dir}/linux-%{tar_ver}/arch/$i/defconfig
	cp -f $i-smp.config %{build_dir}/linux-%{tar_ver}/arch/$i/defconfig-smp
done
popd

# make sure the kernel has the sublevel we know it has...
LC_ALL=C perl -p -i -e "s/^SUBLEVEL.*/SUBLEVEL = %{sublevel}/" linux-%{tar_ver}/Makefile



%build
# Common target directories
%define _kerneldir /usr/src/%{kname}-%{buildrel}
%define _bootdir /boot
%define _modulesdir /lib/modules
%define _up_develdir /usr/src/%{kname}-devel-%{buildrel}
%define _smp_develdir /usr/src/%{kname}-devel-%{buildrel}smp



# Directories definition needed for building
%define temp_root %{build_dir}/temp-root
%define temp_source %{temp_root}%{_kerneldir}
%define temp_boot %{temp_root}%{_bootdir}
%define temp_modules %{temp_root}%{_modulesdir}
%define temp_up_devel %{temp_root}%{_up_develdir}
%define temp_smp_devel %{temp_root}%{_smp_develdir}



PrepareKernel() {
	name=$1
	extension=$2
	echo "Prepare compilation of kernel $extension"

	if [ "$name" ]; then
		config_name="defconfig-$name"
	else
		config_name="defconfig"
	fi

	# make sure EXTRAVERSION says what we want it to say
	%if %kstable
		LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = .%{kstable}-$extension/" Makefile
	%else
		LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -$extension/" Makefile
	%endif

	%smake -s mrproper
	cp arch/%{target_arch}/$config_name .config
	%smake oldconfig
}



BuildKernel() {
	KernelVer=$1
	echo "Building kernel $KernelVer"

	%kmake all

	## Start installing stuff
	install -d %{temp_boot}
	install -m 644 System.map %{temp_boot}/System.map-$KernelVer
	install -m 644 .config %{temp_boot}/config-$KernelVer

	%ifarch sparc64
	gzip -9c vmlinux > %{temp_boot}/vmlinuz-$KernelVer
	%else
	cp -f arch/%{target_arch}/boot/bzImage %{temp_boot}/vmlinuz-$KernelVer
	%endif

	# modules
	install -d %{temp_modules}/$KernelVer
	%smake INSTALL_MOD_PATH=%{temp_root} KERNELRELEASE=$KernelVer modules_install 
}



SaveDevel() {
	flavour=$1
	if [ "$flavour" = "up" ]; then
		DevelRoot=%{temp_up_devel}
	else
		DevelRoot=%{temp_smp_devel}
	fi
	mkdir -p $DevelRoot
	for i in $(find . -name Makefile -o -name Makefile-* -o -name Makefile.*); do cp -R --parents $i $DevelRoot;done
	for i in $(find . -name Kconfig -o -name Kconfig.* -o -name Kbuild -o -name Kbuild.*); do cp -R --parents $i $DevelRoot;done
	cp -fR include $DevelRoot
	cp -fR scripts $DevelRoot
	cp -fR arch/%{target_arch}/kernel/asm-offsets.{c,s} $DevelRoot/arch/%{target_arch}/kernel/
	%ifarch %{ix86}
	cp -fR arch/%{target_arch}/kernel/sigframe.h $DevelRoot/arch/%{target_arch}/kernel/
	%endif
	cp -fR .config Module.symvers $DevelRoot
	
### FIXME MDV bugs #29744, #29074, will be removed when fixed upstream
	mkdir -p $DevelRoot/arch/s390/crypto/
	cp -fR arch/s390/crypto/Kconfig $DevelRoot/arch/s390/crypto/
	
        # Needed for truecrypt build (Danny)
	cp -fR drivers/md/dm.h $DevelRoot/drivers/md/

	# fix permissions
	chmod -R a+rX $DevelRoot
}



CreateFiles() {
	kernversion=$1
	output=../kernel_files.$kernversion

	echo "%defattr(-,root,root)" > $output
	echo "%{_bootdir}/config-${kernversion}" >> $output
	echo "%{_bootdir}/vmlinuz-${kernversion}" >> $output
	echo "%{_bootdir}/System.map-${kernversion}" >> $output
	echo "%dir %{_modulesdir}/${kernversion}/" >> $output
	echo "%{_modulesdir}/${kernversion}/kernel" >> $output
	echo "%{_modulesdir}/${kernversion}/modules.*" >> $output
	echo "%doc README.kernel-sources" >> $output
	echo "%doc README.MandrivaLinux" >> $output
	echo "%doc README.urpmi" >> $output
}



CreateKernel() {
	flavour=$1

	if [ "$flavour" = "up" ]; then
		KernelVer=%{buildrel}
		PrepareKernel "" %{buildrpmrel}
	else
		KernelVer=%{buildrel}$flavour
		PrepareKernel $flavour %{buildrpmrel}$flavour
	fi

	BuildKernel $KernelVer
	%if %build_devel
	    SaveDevel $flavour
	%endif
        CreateFiles $KernelVer
}



###
# DO it...
###



# Create a simulacro of buildroot
rm -rf %{temp_root}
install -d %{temp_root}



#make sure we are in the directory
cd %src_dir

%if %build_smp
CreateKernel smp
%endif

%if %build_up
CreateKernel up
%endif



# We don't make to repeat the depend code at the install phase
%if %build_source
PrepareKernel "" %{buildrpmrel}custom
# From > 2.6.13 prepare-all is deprecated and relies on include/linux/autoconf
# To have modpost and others scripts, one has to use the target scripts
%smake -s prepare
%smake -s scripts
%endif



###
### install
###
%install
install -m 644 %{SOURCE4}  .
install -m 644 %{SOURCE5}  .
install -m 644 %{SOURCE6}  README.urpmi

cd %src_dir
# Directories definition needed for installing
%define target_source %{buildroot}/%{_kerneldir}
%define target_boot %{buildroot}%{_bootdir}
%define target_modules %{buildroot}%{_modulesdir}
%define target_up_devel %{buildroot}%{_up_develdir}
%define target_smp_devel %{buildroot}%{_smp_develdir}

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
for i in alpha arm arm26 avr32 blackfin cris frv h8300 ia64 mips m32r m68k m68knommu parisc powerpc ppc sh sh64 s390 v850 xtensa; do
	rm -rf %{target_source}/arch/$i
	rm -rf %{target_source}/include/asm-$i

### FIXME MDV bugs #29744, #29074, will be removed when fixed upstream
	mkdir -p %{target_source}/arch/s390/crypto/
	cp -fR arch/s390/crypto/Kconfig %{target_source}/arch/s390/crypto/
%if %build_devel
%if %build_up
	rm -rf %{target_up_devel}/arch/$i
	rm -rf %{target_up_devel}/include/asm-$i
%endif
%if %build_smp
	rm -rf %{target_smp_devel}/arch/$i
	rm -rf %{target_smp_devel}/include/asm-$i
%endif
### FIXME MDV bugs #29744, #29074, will be removed when fixed upstream
%if %build_up
	mkdir -p %{target_up_devel}/arch/s390/crypto/
	cp -fR arch/s390/crypto/Kconfig %{target_up_devel}/arch/s390/crypto/
%endif
%if %build_smp
	mkdir -p %{target_smp_devel}/arch/s390/crypto/
	cp -fR arch/s390/crypto/Kconfig %{target_smp_devel}/arch/s390/crypto/
%endif
# Needed for truecrypt build (Danny)
%if %build_up
	cp -fR drivers/md/dm.h %{target_up_devel}/drivers/md/
%endif
%if %build_smp
	cp -fR drivers/md/dm.h %{target_smp_devel}/drivers/md/
%endif
%endif	
done

# remove arch files based on target arch
%ifnarch %{ix86} x86_64
	rm -rf %{target_source}/arch/i386
	rm -rf %{target_source}/arch/x86_64
	rm -rf %{target_source}/include/asm-i386
	rm -rf %{target_source}/include/asm-x86_64
%if %build_devel
%if %build_up
	rm -rf %{target_up_devel}/arch/i386
	rm -rf %{target_up_devel}/arch/x86_64
	rm -rf %{target_up_devel}/include/asm-i386
	rm -rf %{target_up_devel}/include/asm-x86_64
%endif
%if %build_smp
	rm -rf %{target_smp_devel}/arch/i386
	rm -rf %{target_smp_devel}/arch/x86_64
	rm -rf %{target_smp_devel}/include/asm-i386
	rm -rf %{target_smp_devel}/include/asm-x86_64
%endif
%endif
%endif
%ifnarch sparc sparc64
	rm -rf %{target_source}/arch/sparc
	rm -rf %{target_source}/arch/sparc64
	rm -rf %{target_source}/include/asm-sparc
	rm -rf %{target_source}/include/asm-sparc64
%if %build_devel
%if %build_up
	rm -rf %{target_up_devel}/arch/sparc
	rm -rf %{target_up_devel}/arch/sparc64
	rm -rf %{target_up_devel}/include/asm-sparc
	rm -rf %{target_up_devel}/include/asm-sparc64
%endif
%if %build_smp
	rm -rf %{target_smp_devel}/arch/sparc
	rm -rf %{target_smp_devel}/arch/sparc64
	rm -rf %{target_smp_devel}/include/asm-sparc
	rm -rf %{target_smp_devel}/include/asm-sparc64
%endif
%endif	
%endif


# other misc files
rm -f %{target_source}/{.config.old,.config.cmd,.tmp_gas_check,.mailmap,.missing-syscalls.d}

#endif %build_source
%endif



# gzipping modules
find %{target_modules} -name "*.ko" | xargs gzip -9



# We used to have a copy of PrepareKernel here
# Now, we make sure that the thing in the linux dir is what we want it to be

for i in %{target_modules}/*; do
  rm -f $i/build $i/source $i/modules.*
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
	echo $modules | xargs /sbin/modinfo-25 \
	| perl -lne 'print "$name\t$1" if $name && /^description:\s*(.*)/; $name = $1 if m!^filename:\s*(.*)\.k?o!; $name =~ s!.*/!!' > modules.description
	popd
done
popd



###
### clean
###

%clean
rm -rf %{buildroot}
# We don't want to remove this, the whole reason of its existence is to be 
# able to do several rpm --short-circuit -bi for testing install 
# phase without repeating compilation phase
#rm -rf %{temp_root} 



###
### scripts
###

### UP kernel
%preun -n %{kname}-%{buildrel}
/sbin/installkernel -R %{buildrel}
if [ -L /lib/modules/%{buildrel}/build ]; then
    rm -f /lib/modules/%{buildrel}/build
fi
if [ -L /lib/modules/%{buildrel}/source ]; then
    rm -f /lib/modules/%{buildrel}/source
fi
exit 0

%post -n %{kname}-%{buildrel}
/sbin/installkernel %{buildrel}
if [ -d /usr/src/%{kname}-devel-%{buildrel} ]; then
    ln -sf /usr/src/%{kname}-devel-%{buildrel} /lib/modules/%{buildrel}/build
    ln -sf /usr/src/%{kname}-devel-%{buildrel} /lib/modules/%{buildrel}/source
fi

%postun -n %{kname}-%{buildrel}
/sbin/kernel_remove_initrd %{buildrel}



### SMP kernel
%preun -n %{kname}-smp-%{buildrel}
/sbin/installkernel -R %{buildrel}smp
if [ -L /lib/modules/%{buildrel}smp/build ]; then
    rm -f /lib/modules/%{buildrel}smp/build
fi
if [ -L /lib/modules/%{buildrel}smp/source ]; then
    rm -f /lib/modules/%{buildrel}smp/source
fi
exit 0

%post -n %{kname}-smp-%{buildrel}
/sbin/installkernel %{buildrel}smp
if [ -d /usr/src/%{kname}-devel-%{buildrel}smp ]; then
    ln -sf /usr/src/%{kname}-devel-%{buildrel}smp /lib/modules/%{buildrel}smp/build
    ln -sf /usr/src/%{kname}-devel-%{buildrel}smp /lib/modules/%{buildrel}smp/source
fi

%postun -n %{kname}-smp-%{buildrel}
/sbin/kernel_remove_initrd %{buildrel}smp



### kernel-devel
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



### kernel-smp-devel
%post -n %{kname}-smp-devel-%{buildrel}
# place /build and /source symlinks in place.
if [ -d /lib/modules/%{buildrel}smp ]; then
    ln -sf /usr/src/%{kname}-devel-%{buildrel}smp /lib/modules/%{buildrel}smp/build
    ln -sf /usr/src/%{kname}-devel-%{buildrel}smp /lib/modules/%{buildrel}smp/source
fi

%preun -n %{kname}-smp-devel-%{buildrel}
# we need to delete <modules>/{build,source} at uninstall
if [ -L /lib/modules/%{buildrel}smp/build ]; then
    rm -f /lib/modules/%{buildrel}smp/build
fi
if [ -L /lib/modules/%{buildrel}smp/source ]; then
    rm -f /lib/modules/%{buildrel}smp/source
fi
exit 0



### kernel-source
%post -n %{kname}-source-%{buildrel}
for i in /lib/modules/%{buildrel}*; do
	if [ -d $i ]; then
	        rm -f $i/{build,source}
	        ln -sf /usr/src/%{kname}-%{buildrel} $i/build
	        ln -sf /usr/src/%{kname}-%{buildrel} $i/source
	fi
done
								
%preun -n %{kname}-source-%{buildrel}
for i in /lib/modules/%{buildrel}/{build,source}; do
	if [ -L $i ]; then
		rm -f $i
	fi
done
exit 0
												

###
### file lists
###

%if %build_up
%files -n %{kname}-%{buildrel} -f kernel_files.%{buildrel}
%endif

%if %build_smp
%files -n %{kname}-smp-%{buildrel} -f kernel_files.%{buildrel}smp
%endif

%if %build_source
%files -n %{kname}-source-%{buildrel}
%defattr(-,root,root)
%dir %{_kerneldir}
%dir %{_kerneldir}/arch
%dir %{_kerneldir}/include
%{_kerneldir}/.config
%{_kerneldir}/.gitignore
%{_kerneldir}/COPYING
%{_kerneldir}/CREDITS
%{_kerneldir}/Documentation
%{_kerneldir}/Kbuild
%{_kerneldir}/MAINTAINERS
%{_kerneldir}/Makefile
%{_kerneldir}/README
%{_kerneldir}/REPORTING-BUGS
### FIXME MDV bugs #29744, #29074, will be removed when fixed upstream
%{_kerneldir}/arch/s390
%ifarch sparc sparc64
%{_kerneldir}/arch/sparc
%{_kerneldir}/arch/sparc64
%endif
%ifarch %{ix86} x86_64
%{_kerneldir}/arch/i386
%{_kerneldir}/arch/x86_64
%endif
%{_kerneldir}/arch/um
%{_kerneldir}/block
%{_kerneldir}/crypto
%{_kerneldir}/drivers
%{_kerneldir}/fs
%{_kerneldir}/include/Kbuild
%{_kerneldir}/include/acpi
%{_kerneldir}/include/asm
%{_kerneldir}/include/asm-generic
%ifarch sparc sparc64
%{_kerneldir}/include/asm-sparc
%{_kerneldir}/include/asm-sparc64
%endif
%ifarch %{ix86} x86_64
%{_kerneldir}/include/asm-i386
%{_kerneldir}/include/asm-x86_64
%endif
%{_kerneldir}/include/asm-um
%{_kerneldir}/include/config
%{_kerneldir}/include/crypto
%{_kerneldir}/include/linux
%{_kerneldir}/include/math-emu
%{_kerneldir}/include/net
%{_kerneldir}/include/pcmcia
%{_kerneldir}/include/scsi
%{_kerneldir}/include/sound
%{_kerneldir}/include/video
%{_kerneldir}/include/media
%{_kerneldir}/include/mtd
%{_kerneldir}/include/rxrpc
%{_kerneldir}/include/keys
%{_kerneldir}/include/rdma
%{_kerneldir}/init
%{_kerneldir}/ipc
%{_kerneldir}/kernel
%{_kerneldir}/lib
%{_kerneldir}/mm
%{_kerneldir}/net
%{_kerneldir}/security
%{_kerneldir}/scripts
%{_kerneldir}/sound
%{_kerneldir}/usr
%doc README.kernel-sources
%doc README.MandrivaLinux
%doc README.urpmi
%endif

%if %build_devel
# kernel-devel
%if %build_up
%files -n %{kname}-devel-%{buildrel}
# this defattr makes tree readonly, to try and work around broken dkms & co
#defattr(0444,root,root,0555)
%defattr(-,root,root)
%dir %{_up_develdir}
%dir %{_up_develdir}/arch
%dir %{_up_develdir}/include
%{_up_develdir}/.config
%{_up_develdir}/Documentation
%{_up_develdir}/Kbuild
%{_up_develdir}/Makefile
%{_up_develdir}/Module.symvers
### FIXME MDV bugs #29744, #29074, will be removed when fixed upstream
%{_up_develdir}/arch/s390
%ifarch sparc sparc64
%{_up_develdir}/arch/sparc
%{_up_develdir}/arch/sparc64
%endif
%ifarch %{ix86} x86_64
%{_up_develdir}/arch/i386
%{_up_develdir}/arch/x86_64
%endif
%{_up_develdir}/arch/um
%{_up_develdir}/block
%{_up_develdir}/crypto
%{_up_develdir}/drivers
%{_up_develdir}/fs
%{_up_develdir}/include/Kbuild
%{_up_develdir}/include/acpi
%{_up_develdir}/include/asm
%{_up_develdir}/include/asm-generic
%ifarch sparc sparc64
%{_up_develdir}/include/asm-sparc
%{_up_develdir}/include/asm-sparc64
%endif
%ifarch %{ix86} x86_64
%{_up_develdir}/include/asm-i386
%{_up_develdir}/include/asm-x86_64
%endif
%{_up_develdir}/include/asm-um
%{_up_develdir}/include/config
%{_up_develdir}/include/crypto
%{_up_develdir}/include/keys
%{_up_develdir}/include/linux
%{_up_develdir}/include/math-emu
%{_up_develdir}/include/mtd
%{_up_develdir}/include/net
%{_up_develdir}/include/pcmcia
%{_up_develdir}/include/rdma
%{_up_develdir}/include/scsi
%{_up_develdir}/include/sound
%{_up_develdir}/include/video
%{_up_develdir}/include/media
%{_up_develdir}/include/rxrpc
%{_up_develdir}/init
%{_up_develdir}/ipc
%{_up_develdir}/kernel
%{_up_develdir}/lib
%{_up_develdir}/mm
%{_up_develdir}/net
%{_up_develdir}/scripts
%{_up_develdir}/security
%{_up_develdir}/sound
%{_up_develdir}/usr
%doc README.kernel-sources
%doc README.MandrivaLinux
%doc README.urpmi
%endif

# kernel-smp-devel
%if %build_smp
%files -n %{kname}-smp-devel-%{buildrel}
# this defattr makes tree readonly, to try and work around broken dkms & co
#defattr(0444,root,root,0555)
%defattr(-,root,root)
%dir %{_smp_develdir}
%dir %{_smp_develdir}/arch
%dir %{_smp_develdir}/include
%{_smp_develdir}/.config
%{_smp_develdir}/Documentation
%{_smp_develdir}/Kbuild
%{_smp_develdir}/Makefile
%{_smp_develdir}/Module.symvers
### FIXME MDV bugs #29744, #29074, will be removed when fixed upstream
%{_smp_develdir}/arch/s390
%ifarch sparc sparc64
%{_smp_develdir}/arch/sparc
%{_smp_develdir}/arch/sparc64
%endif
%ifarch %{ix86} x86_64
%{_smp_develdir}/arch/i386
%{_smp_develdir}/arch/x86_64
%endif
%{_smp_develdir}/arch/um
%{_smp_develdir}/block
%{_smp_develdir}/crypto
%{_smp_develdir}/drivers
%{_smp_develdir}/fs
%{_smp_develdir}/include/Kbuild
%{_smp_develdir}/include/acpi
%{_smp_develdir}/include/asm
%{_smp_develdir}/include/asm-generic
%ifarch sparc sparc64
%{_smp_develdir}/include/asm-sparc
%{_smp_develdir}/include/asm-sparc64
%endif
%ifarch %{ix86} x86_64
%{_smp_develdir}/include/asm-i386
%{_smp_develdir}/include/asm-x86_64
%endif
%{_smp_develdir}/include/asm-um
%{_smp_develdir}/include/config
%{_smp_develdir}/include/crypto
%{_smp_develdir}/include/keys
%{_smp_develdir}/include/linux
%{_smp_develdir}/include/math-emu
%{_smp_develdir}/include/mtd
%{_smp_develdir}/include/net
%{_smp_develdir}/include/pcmcia
%{_smp_develdir}/include/rdma
%{_smp_develdir}/include/scsi
%{_smp_develdir}/include/sound
%{_smp_develdir}/include/video
%{_smp_develdir}/include/media
%{_smp_develdir}/include/rxrpc
%{_smp_develdir}/init
%{_smp_develdir}/ipc
%{_smp_develdir}/kernel
%{_smp_develdir}/lib
%{_smp_develdir}/mm
%{_smp_develdir}/net
%{_smp_develdir}/scripts
%{_smp_develdir}/security
%{_smp_develdir}/sound
%{_smp_develdir}/usr
%doc README.kernel-sources
%doc README.MandrivaLinux
%doc README.urpmi
#endif %build_devel
%endif
%endif

%if %build_doc
%files -n %{kname}-doc-%{buildrel}
%defattr(-,root,root)
%doc linux-%{tar_ver}/Documentation/*
%endif

%if %build_up
%files -n %{kname}-latest
%defattr(-,root,root)
%endif

%if %build_smp
%files -n %{kname}-smp-latest
%defattr(-,root,root)
%endif

%if %build_source
%files -n %{kname}-source-latest
%defattr(-,root,root)
%endif

%if %build_devel
%files -n %{kname}-devel-latest
%defattr(-,root,root)

%files -n %{kname}-smp-devel-latest
%defattr(-,root,root)
%endif

%if %build_doc
%files -n %{kname}-doc-latest
%defattr(-,root,root)
%endif



%changelog
* Sat Aug  4 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23-0.rc2.1mdv
- update to kernel.org 2.6.23-rc2
- update defconfigs

* Fri Aug  3 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22.1-2mdv
- disable DEBUG_SLAB, as it's bad for performance, especially
  under heavier loads
  
* Thu Jul 12 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22.1-1mdv
- update to kernel.org 2.6.22.1
  * NETFILTER: {ip, nf}_conntrack_sctp: fix remotely triggerable 
    NULL ptr dereference (CVE-2007-2876)

* Mon Jul  9 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-1mdv
- update to kernel.org 2.6.22 final
- update defconfigs, make IDE modular

* Tue Jul  3 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc7.1mdv
- update to kernel.org 2.6.22-rc7
- add support for git patches
- update to 2.6.22-rc7-git1

* Mon Jun 25 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc6.1mdv
- update to kernel.org 2.6.22-rc6
- make buildroot arch-specific to allow dual build in same rpm tree
- update defconfig

* Sun Jun 24 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc5.2mdv
- kernel-devel rpms does not provide kernel-source anymore
- re-add build,source symlink logic to kernel-source as dkms needs it
  and can cope with the Makefile version mismatch 
- update README.urpmi regarding the symlinks

* Sun Jun 17 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc5.1mdv
- update to kernel.org 2.6.22-rc5

* Tue Jun  5 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc4.1mdv
- update to kernel.org 2.6.22-rc4

* Sun May 27 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc3.1mdv
- update to kernel.org 2.6.22-rc3
- provide versioned kernel-devel and kernel-source (MDV #31006)

* Tue May 22 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc2.1mdv
- update to kernel.org 2.6.22-rc2
- disable CONFIG_IRQBALANCE on i386-smp, in favour of the better
  working userspace irqbalance daemon from contribs (Requested by Austin)
- remove blackfin arch files
- update defconfigs

* Fri May 18 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21.1-2mdv
- update kernel-linus-source description to point out:
  * only needed when building own kernels
  * othervise install a matching -devel- rpm
- update README.urpmi for the same reason
- enable CONFIG_TIMER_STATS (request by Michael Braun)
- /sbin/depmod-25 is now renamed to /sbin/depmod

* Sat Apr 28 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21.1-1mdv
- kernel.org 2.6.21.1
  * IPV6: Fix for RT0 header ipv6 change
  * IPV4: Fix OOPS'er added to netlink fib
- Enable Tickless System (Dynamic Ticks (NO_HZ)) on i386 kernels

* Fri Apr 27 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-2mdv
- revert read-only -devel rpms until I find a better solution...

* Thu Apr 26 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-1mdv
- update to kernel.org 2.6.21 final
- make devel trees read-only (like in kernel-multimedia series),
  to try and work around broken dkms & co
  
* Sun Apr 22 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-0.rc7.1mdv
- update to 2.6.21-rc7
- update defconfigs
- enable CONFIG_X86_P4_CLOCKMOD again
- fix README.urpmi on -rc and -stable builds
- add drivers/md/dm.h to -devel rpms, needed for truecrypt builds (Danny)

* Wed Mar 21 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-0.rc3.4mdv
- add arch/s390/crypto/Kconfig for now, until fixed upstream,
  closes #29074, and fixes kernel-linus part of #29744

* Sun Mar 18 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-0.rc3.3mdv
- fix typo in -devel post script (Charles A Edwards)
- make the build work even if you only build up or smp (Charles A Edwards)
- fix typo in -smp-devel post script

* Thu Mar 15 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-0.rc3.2mdv
- fix typo in post script (#29395)
- CFQ is now the default i/o scheduler

* Wed Mar 07 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-0.rc3.1mdv
- update to kernel.org 2.6.21-rc3
- disable CONFIG_X86_P4_CLOCKMOD (broken build)
- update defconfigs

* Tue Mar 06 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-0.rc2.2mdv
- disable CONFIG_ACORN_PARTITION_CUMANA (#29006)
- rename *-headers rpms to more appropriate *-devel
- make make *-devel-latest obsolete *-headers-latest to enable automatic update

* Wed Feb 28 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-0.rc2.1mdv
- update to kernel.org 2.6.21-rc2
- add patch101: fixes build on i386 and x86_64, from upsrteam linux-2.6.git,
  will be removed when 2.6.21-rc3 is released.
- update defconfigs

* Sat Feb 24 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-0.rc1.1mdv
- update to kernel.org 2.6.21-rc1
- update defconfigs

* Wed Feb 21 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.1-2mdv
- add missing /arch/i386/kernel/sigframe.h in header rpms (#28843)

* Wed Feb 21 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.1-1mdv
- update to kernel.org 2.6.20.1
  o Fix a free-wrong-pointer bug in nfs/acl server (CVE-2007-0772)
  
* Mon Feb 19 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20-3mdv
- add README.urpmi with info specific for this kernel set
- drop all patches, this kernel _has_ to stay unpatched, as it's
  a precompiled kernel.org reference kernel

* Sat Feb 17 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20-2mdv
- fix RC versioning
- enable KVM support (requested by ahasenack)
- fix the whole autoconf mess
  dont rely on /etc/init.d/kheader and /boot/kernel.h anymore
  drop all of the old autoconf hacks     
  drop kernel-linus-source-stripped(-latest) rpms
  introduce kernel-linus-(smp-)headers(-latest) rpms to build 3rdparty 
  drivers against (survives test: make mrproper oldconfig prepare scripts)
  kernel-linus-source rpm does not include any autoconf stuff anymore
- add bugfixes from upcoming 2.6.20.1 (will be removed when it's released)
  01_fix-missing-critical-phys_to_virt-in-lib_swiotlb.patch
  02_ieee1394-video1394-DMA-fix.patch
  03_ieee1394-fix-host-device-registering-when-nodemgr-disabled.patch
  04_fix-oops-in-xfrm_audit_log.patch
  05_md-raid5-fix-crash.patch
  06_md-raid5-fix-export-blk_recount_segments.patch
  
* Mon Feb  5 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20-1mdv
- update to kernel.org 2.6.20 final

* Wed Jan 31 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.0.rc7-1mdv
- update to kernel.org: 2.6.20-rc7

* Thu Jan 25 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.0.rc6-1mdv
- update to kernel.org: 2.6.20-rc6

* Tue Jan 16 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.0.rc5-2mdv
- fix install breakage due to spec cleanup (thanks Charles)
- fix kernel versioning mismatch (#28237)

* Sun Jan 14 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20-rc5-1mdv
- finally move on to 2.6.20-rc5

* Wed Jan 10 2007 Thomas Backlund <tmb@mandriva.org> 2.6.19.2-1mdv
- update to kernel.org 2.6.19.2:
    - bonding: incorrect bonding state reported via ioctl
    - dvb-core: fix bug in CRC-32 checking on 64-bit systems
    - x86-64: Mark rdtsc as sync only for netburst, not for core2
    - Fix for shmem_truncate_range() BUG_ON()
    - ebtables: don't compute gap before checking struct type
    - asix: Fix typo for AX88772 PHY Selection
    - IPV4/IPV6: Fix inet{,6} device initialization order
    - UDP: Fix reversed logic in udp_get_port()
    - SPARC64: Fix "mem=xxx" handling
    - SPARC64: Handle ISA devices with no 'regs' property
    - SOUND: Sparc CS4231: Use 64 for period_bytes_min
    - NET: Don't export linux/random.h outside __KERNEL__
    - ramfs breaks without CONFIG_BLOCK
    - i2c: fix broken ds1337 initialization
    - fix aoe without scatter-gather [Bug 7662]
    - handle ext3 directory corruption better (CVE-2006-6053)
    - ext2: skip pages past number of blocks in ext2_find_entry (CVE-2006-6054)
    - connector: some fixes for ia64 unaligned access errors
    - SOUND: Sparc CS4231: Fix IRQ return value and initialization
    - V4L: Fix broken TUNER_LG_NTSC_TAPE radio support
    - V4L: cx2341x: audio_properties is an u16, not u8
    - dm-crypt: Select CRYPTO_CBC
    - sha512: Fix sha384 block size
    - read_zero_pagealigned() locking fix
    - fix OOM killing of swapoff
    - sched: fix bad missed wakeups in the i386, x86_64, ia64, ACPI and APM idle code
    - sparc32: add offset in pci_map_sg()
    - V4L: cx88: Fix leadtek_eeprom tagging
    - Revert "zd1211rw: Removed unneeded packed attributes
    - VM: Fix nasty and subtle race in shared mmap'ed page writeback
    - Fix incorrect user space access locking in mincore() (CVE-2006-4814)
    - Bluetooth: Add packet size checks for CAPI messages (CVE-2006-6106)
    - DVB: lgdt330x: fix signal / lock status detection bug
    - cciss: fix XFER_READ/XFER_WRITE in do_cciss_request
    - NetLabel: correctly fill in unused CIPSOv4 level and category mappings
    - Fix up page_mkclean_one(): virtual caches, s390
    - corrupted cramfs filesystems cause kernel oops (CVE-2006-5823)
    - PKTGEN: Fix module load/unload races
    - IB/srp: Fix FMR mapping for 32-bit kernels and addresses above 4G
    - kbuild: don't put temp files in source
    - ARM: Add sys_*at syscalls
    - Buglet in vmscan.c
    - i386: CPU hotplug broken with 2GB VMSPLIT
    - ieee1394: ohci1394: add PPC_PMAC platform code to driver probe
    - libata: handle 0xff status properly
    - SCSI: add missing cdb clearing in scsi_execute()
    - sched: remove __cpuinitdata anotation to cpu_isolated_ma
    - ieee80211softmac: Fix mutex_lock at exit of ieee80211_softmac_get_genie
    - softmac: Fixed handling of deassociation from AP
    - zd1211rw: Call ieee80211_rx in tasklet
    - smc911x: fix netpoll compilation faliure
- drop Patch100: merged upstream
- disable BLK_DEV_UB (#28058)
- fix source-stripped provides (thanks Thierry)
- big spec cleanup: remove all arches and flavours we dont build

* Sun Jan  7 2007 Thomas Backlund <tmb@mandriva.org> 2.6.19.1-2mdv
- fix UTS_RELEASE define in /include/linux/utsrelease.h (#28014)
- fix utsrelease temporary location grep on i586 build
- finally add the *-latest virtual rpms
- add patch100: fix the file content corruption bug that appeared in 2.6.19. 
  Will be remowed when 2.6.19.2 is released

* Tue Dec 12 2006 Thomas Backlund <tmb@mandriva.org> 2.6.19.1-1mdv
- update to kernel.org 2.6.19.1:
    - NETLINK: Put {IFA,IFLA}_{RTA,PAYLOAD} macros back for userspace
    - forcedeth: Disable INTx when enabling MSI in forcedeth
    - x86: Fix boot hang due to nmi watchdog init code
    - m32r: make userspace headers platform-independent
    - softirq: remove BUG_ONs which can incorrectly trigger
    - autofs: fix error code path in autofs_fill_sb()
    - PM: Fix swsusp debug mode testproc
    - compat: skip data conversion in compat_sys_mount when data_page is NULL
    - drm-sis linkage fix
    - add bottom_half.h
    - NETLINK: Restore API compatibility of address and neighbour bits
    - IrDA: Incorrect TTP header reservation
    - IPSEC: Fix inetpeer leak in ipv4 xfrm dst entries
    - USB: Fix oops in PhidgetServo
    - XFRM: Use output device disable_xfrm for forwarded packets
    - TOKENRING: Remote memory corruptor in ibmtr.c
    - do_coredump() and not stopping rewrite attacks? (CVE-2006-6304)
    - IB/ucm: Fix deadlock in cleanup
    - softmac: fix unbalanced mutex_lock/unlock in ieee80211softmac_wx_set_mlme
    - NETFILTER: bridge netfilter: deal with martians correctly
    - NETFILTER: Fix iptables compat hook validation
    - NETFILTER: Fix {ip, ip6, arp}_tables hook validation
    - SUNHME: Fix for sunhme failures on x86
    - PKT_SCHED act_gact: division by zero
    - Revert "ACPI: SCI interrupt source override"
    - cryptoloop: Select CRYPTO_CBC
    - NET_SCHED: policer: restore compatibility with old iproute binaries
    - EBTABLES: Prevent wraparounds in checks for entry components' sizes
    - EBTABLES: Deal with the worst-case behaviour in loop checks
    - EBTABLES: Verify that ebt_entries have zero ->distinguisher
    - EBTABLES: Fix wraparounds in ebt_entries verification
    - softmac: remove netif_tx_disable when scanning
    - IPV6 NDISC: Calculate packet length correctly for allocation
- drop patch100: merged upstream
- fix autoconf
																    
* Wed Dec  6 2006 Thomas Backlund <tmb@mandriva.org> 2.6.19-3mdv
- add patch100: revert: ACPI: SCI interrupt source override,
  breaks atleast RTL8139, will be in 2.6.19.1
- enable ARPD, IPV6_MIP6, IPV6_MULTIPLE_TABLES, IPV6_ROUTE_FWMARK
  CONFIG_GFS2_FS, GFS2_FS_LOCKING_NOLOCK, GFS2_FS_LOCKING_DLM (#27479)

* Sat Dec  2 2006 Thomas Backlund <tmb@mandriva.org> 2.6.19-2mdv
- rename kernel-2.6-linus to kernel-linus in SVN and specfile
- fix kernel-linus srpm name (Anssi Hannula)

* Fri Dec  1 2006 Thomas Backlund <tmb@mandriva.org> 2.6.19--1mdv
- update to 2.6.19 final

* Fri Nov 17 2006 Thomas Backlund <tmb@mandriva.org> 2.6.19-0.rc6-1mdv
- update to 2.6.19-rc6

* Sat Nov 11 2006 Thomas Backlund <tmb@mandriva.org> 2.6.19-0.rc5-2mdv
- bump release to reupload

* Thu Nov  9 2006 Thomas Backlund <tmb@mandriva.org> 2.6.19-0.rc5-1mdv
- add support for stable series kernels
- update to kernel.org 2.6.19-rc5

* Wed Sep 20 2006 Thomas Backlund <tmb@mandriva.org> 2.6.18-1mdv
- update to 2.6.18 final

* Wed Sep 13 2006 Thomas Backlund <tmb@mandriva.org> 2.6.18-rc7-1mdv
- update to 2.6.18-rc7

* Wed Sep  6 2006 Thomas Backlund <tmb@mandriva.org> 2.6.18-rc6-3mdv
- fix spec for missing UTS_RELEASE (#24889)

* Tue Sep  5 2006 Thomas Backlund <tmb@mandriva.org> 2.6.18-rc6-2mdv
- fix autoconf UTS_RELEASE relocation from version.h to 
  utsrelease.h (#24889)

* Mon Sep  4 2006 Thomas Backlund <tmb@mandriva.org> 2.6.18-rc6-1mdv
- update to 2.6.18-rc6
- fix rpmlint warnings

* Sun Sep  3 2006 Thomas Backlund <tmb@mandriva.org> 2.6.18-rc5.6mdv
- change source15 to fix autoconf part that bootloader-utils-1.13
  broke (#24889)
- fix autoconf to work with 2.6.18 series auto.conf (#24889)
- stop building useless debug rpms
- spec cleanup  s/mdk/mdv/g
- update README.kernel-sources 
- use mkrel and distsuffix to make it work for backports
- source and source-stripped needs to conflict each other

* Mon Aug 28 2006 Thomas Backlund <tmb@mandriva.org> 2.6.18-rc5-5mdv
- Updates to 2.6.18-rc5
- update defconfigs
- fix target_arch on sparc64 (pkarlsen@mandriva.com)

* Tue Aug  8 2006 Thomas Backlund <tmb@mandriva.org> 2.6.18-rc4-4mdv
- Updates to 2.6.18-rc4
- Spec cleaning
- update defconfigs
- update README files
- fix previous changelog year s/2008/2006/g

* Tue Jul 18 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-07-18 20:38:40 (41569)
- Updates to 2.6.18-rc2

* Sun Jul 09 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-07-09 16:54:32 (38600)
- Updates to 2.6.18-rc1

* Tue Jun 20 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-06-20 15:23:55 (37658)
- Updates to 2.6.17
- Version reset: when I started with kernel-linus I wasn't too
  experienced with RPM packages and thought that packages' version
  should never been reset. Doing it now.

* Fri Jun 09 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-06-09 15:44:06 (36901)
- Adds new Mandriva tag

* Tue Jun 06 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-06-06 16:20:10 (36699)
- Updates to 2.6.17-rc6

* Mon May 29 2006 Andreas Hasenack <andreas@mandriva.com>
+ 2006-05-29 14:36:37 (31646)
- renamed mdv to packages because mdv is too generic and it's hosting only packages anyway

* Thu May 25 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-05-25 17:05:48 (31590)
- Updates to 2.6.17-rc5

* Fri May 12 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-05-12 15:49:33 (27159)
- Updates to 2.6.17-rc4

* Mon May 08 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-05-08 22:18:55 (27006)
- Fixes 'kernel-source is upgraded but kernel is not' bug (#21345)

* Thu May 04 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-05-04 21:20:52 (26917)
- Introduces PPC support, patch and .config files from Christiaan Welvaart
  <cjw@daneel.dyndns.org>

* Thu May 04 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-05-04 20:07:28 (26913)
- x86 .configs update, the following changes have been made:
    o OBSOLETE and non-sense options have been disabled
    o New drivers and other interesting options (which were probably
      not automatically enabled by the bot) have been enabled
    o SMP kernel now supports: cpusets, 32 CPUs and 64 GB of memory

* Fri Apr 28 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-04-28 16:21:36 (26756)
- Updates sparc64 .config files, patch from Per Oyvind Karlsen
  <pkarlsen@mandriva.com>

* Thu Apr 27 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-04-27 23:02:25 (26741)
- Updates to 2.6.17-rc3

* Wed Apr 26 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-04-26 21:04:42 (26694)
- Updates sparc64 .config files, patch from Per Oyvind Karlsen
  <pkarlsen@mandriva.com>

* Wed Apr 26 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-04-26 21:02:18 (26693)
- This patch makes kernel image 'gzipped', it's needed to make it
  boot properly (and also makes sparc's kernel image consistent with
  other archs). Patch from Per Oyvind Karlsen <pkarlsen@mandriva.com>.

* Wed Apr 19 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-04-19 15:31:31 (26557)
- Updates to 2.6.17-rc2

* Tue Apr 04 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-04-04 20:41:08 (26277)
- Updates sparc64 .config files, patch from Per Oyvind Karlsen
  <pkarlsen@mandriva.com>

* Mon Apr 03 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-04-03 19:15:29 (26268)
- Updates to 2.6.17-rc1

* Mon Mar 20 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-03-20 17:13:33 (26030)
- Updates to 2.6.16

* Fri Mar 17 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-03-17 19:06:45 (26002)
- Minor typo

* Sun Mar 12 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-03-12 16:42:36 (1942)
- Updates to 2.6.16-rc6

* Tue Feb 28 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-02-28 01:09:44 (1817)
- Updates to 2.6.16-rc5

* Tue Feb 21 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-02-21 14:47:10 (1800)
- Changes to the kernel's stack to 8k bytes, as this question is polemic
  in two sides (proprietary drivers and performance) let's stay with the
  kernel's default.

* Sun Feb 19 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-02-19 19:53:40 (1789)
- - Updates to 2.6.16-rc4

* Wed Feb 15 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-02-15 21:35:55 (1741)
- New version

* Wed Feb 15 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-02-15 13:45:39 (1738)
- Changes some SMP options as suggested by Arnaud Patard <apatard@mandriva.com>
  basically, we're dropping BKL preemption support (because this is not
  supposed to only run on desktop systems), enabling software suspend and
  CPU hotpluging.

* Tue Feb 14 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-02-14 16:44:07 (1736)
- Introduces sparc64 support (patches from Per Oyvind Karlsen
  <pkarlsen@mandriva.com>)

* Mon Feb 13 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-02-13 16:49:28 (1730)
- Updates to 2.6.16-rc3

* Fri Feb 10 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-02-10 18:23:18 (1724)
- Some times I'm really stupid: forgot to add the spec changelog entry
  and to change the package's version on r1723.

* Fri Feb 10 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-02-10 18:14:00 (1723)
- Enables CONFIG_CC_OPTIMIZE_FOR_SIZE, to try to get a smaller kernel and
  other benefits.

* Fri Feb 03 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-02-03 13:51:35 (1566)
- Introduces 'update_configs' script (from mdv2006 stable kernel)
- Updates to 2.6.16-rc2

* Sat Jan 28 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-01-28 17:12:11 (1493)
- Minor log fix
- Commit in behalf of Oden Eriksson <oeriksson@mandriva.com>:
  - Fixes kernel headers generation
  - Fixes SUBLEVEL change in the kernel`s Makefile
  - Minor cleanups

* Fri Jan 27 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-01-27 19:23:09 (1492)
- Improves klinus_notice

* Thu Jan 26 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-01-26 20:00:11 (1480)
- Adds a note (in the package description) about kernel-linus's nature

* Thu Jan 19 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-01-19 17:20:01 (1442)
- Minor log fix, rpm prints some warnings with you write '%%prep' in the
  changelog section

* Wed Jan 18 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-01-18 22:57:31 (1441)
- Fixes embarrassing bug which causes any *.config file to be copied
  to the build directory
- Comments out removal of unwanted files in %%prep section, this doesn't
  seen to be needed anymore and can cause to wanted files to be removed too
- Adds comments in the top file about kernel-linus known issues

* Wed Jan 18 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-01-18 21:22:00 (1440)
- New spec file name (kernel-2.6.spec is already used by other package)
- Adds all the kernel's .config file as 'Source', that way they're
  included in the src.rpm

* Tue Jan 17 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-01-17 16:26:42 (1436)
- Updates to 2.6.16-rc1

* Mon Jan 16 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-01-16 20:54:13 (1432)
- Updating package version, this will be the next release

* Sun Jan 15 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-01-15 20:47:24 (1429)
- Merges kernel-2.6-linus simplifications into the trunk
  (svn merge -r 1362:1428 svn+ssh://svn.mandriva.com/svn/mdv/branches/cooker/kernel-2.6-linus/current .)

* Thu Jan 05 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-01-05 18:04:27 (1380)
- Disables CONFIG_HWMON_DEBUG_CHIP, it's only interesting for
  developers

* Thu Jan 05 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-01-05 17:44:32 (1379)
- Provides kernel-source package should provides 'kernel-source', this
  makes life easier when using dkms

* Tue Jan 03 2006 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2006-01-03 13:40:22 (1359)
- Minor log fix
- Updates to 2.6.15

* Fri Dec 30 2005 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2005-12-30 16:42:34 (1356)
- Fixes kernel-source package generation

* Wed Dec 28 2005 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2005-12-28 19:17:07 (1353)
- Updates TODO list

* Wed Dec 28 2005 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2005-12-28 19:12:46 (1352)
- Enables compilation for more architectures
- s/ppc64/powerpc/
- Minor %%patchlevel fix

* Tue Dec 27 2005 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2005-12-27 18:32:49 (1351)
- Fixes Makefile hardcoded values
- Updated to 2.6.15-rc7

* Tue Dec 27 2005 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2005-12-27 13:18:43 (1349)
- Fixes Makefile hardcoded values

* Mon Dec 26 2005 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2005-12-26 17:56:36 (1346)
- reverts r1345 and r1344. I was going to update the package for 2.6.15-rc7
  but there are some things to be done before, like a new release and tons
  of fixes.

* Mon Dec 26 2005 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2005-12-26 13:35:00 (1345)
- Updates .config files for 2.6.15-rc7

* Mon Dec 26 2005 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2005-12-26 13:21:13 (1344)
- Updates to 2.6.15-rc7
- Enables more archs
- Minor Changes

* Thu Dec 22 2005 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2005-12-22 19:52:16 (1343)
- Introduces TODO list

* Thu Dec 22 2005 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2005-12-22 18:57:21 (1342)
- Minor spec file fixes
- Changes package name to 'kernel-linus'
- Update version

* Thu Dec 22 2005 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2005-12-22 13:26:14 (1336)
- Fixes br0ken compile with our current i386.config

* Wed Dec 21 2005 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2005-12-21 21:28:55 (1330)
- Update hardcoded value to make the thing compile

* Wed Dec 21 2005 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2005-12-21 20:21:15 (1327)
- This is a new package, removes all the changelog entries and adds the
  relevant one

* Wed Dec 21 2005 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2005-12-21 20:10:37 (1326)
- Err, time-stamp are created automatically during build time, this files
  pulled in at the initial import step.. They shouldn't be here.

* Wed Dec 21 2005 Luiz Fernando Capitulino <lcapitulino@mandriva.com>
+ 2005-12-21 19:30:42 (1325)
- Introduces 'kernel-2.6-linus' RPM package source tree. This new package
  will provide the latest -rc kernels from Linus.
