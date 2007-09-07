%define major 2
%define libname %mklibname nasl %{major}
%define libnamedev %mklibname nasl -d

Summary:	NASL is a scripting language designed for the Nessus security scanner
Name:		libnasl
Version:	2.2.10
Release:	%mkrel 1
License:	GPL
Group:		System/Libraries
URL:		http://www.nessus.org
#http://cgi.tenablesecurity.com/nessus3dl.php?file=libnasl-2.2.10.tar.gz&licence_accept=yes&t=5a144975306462c6d49d299ba1d6c0b2
Source0:	libnasl-%{version}.tar.gz
Patch0:		libnasl-2.2.3-pem.patch
Patch1:		libnasl-2.2.7-nasl-config.diff
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	openssl-devel
BuildRequires:	libnessus-devel = %{version}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
NASL is a scripting language designed for the Nessus security scanner.
Its aim is to allow anyone to write a test for a given security hole
in a few minutes, to allow people to share their tests without having
to worry about their operating system, and to garantee everyone that a
NASL script can not do anything nasty except performing a given
security test against a given target.  Thus, NASL allows you to easily
forge IP packets, or to send regular packets. It provides you some
convenient functions that will make the test of web and ftp server
more easy to write. NASL garantees you that a NASL script:
    * will not send any packet to a host other than the target host
    * will not execute any commands on your local system 

%package -n 	%{libname}
Summary:	Nasl - Nessus Attack Scripting Language
Group:		System/Libraries
Provides:	nessus-libs
Obsoletes:	nessus-libs

%description -n	%{libname}
Nasl - Nessus Attack Scripting Language.
These libraries are needed by nessus.

%package -n	%{libnamedev}
Summary:	Development libraries and headers for Nasl
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	libnasl-devel = %{version}
Obsoletes:	%{mklibname nasl 2 -d}

%description -n	%{libnamedev}
Development libraries and headers for Nasl.

%prep

%setup -q -n %{name}
%patch0 -p1 -b .pem
%patch1 -p0

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure* aclocal.m4

%build
%define __libtoolize /bin/true

%configure
# 2.0.6: parallel make is broken
make

%install
if [ -d %{buildroot} ]; then rm -rf %{buildroot}; fi
%makeinstall
perl -pi -e 's|^PREFIX=.*|PREFIX='%{buildroot}%{_prefix}'|' %{buildroot}%{_bindir}/nasl-config

# remove unwanted files
rm -rf	%{buildroot}%{_libdir}/%{name}/plugins_factory
rm -rf  %{buildroot}%{_localstatedir}/nessus/nessus_org.pem

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
if [ -d %{buildroot} ]; then rm -rf %{buildroot}; fi

%files -n %{libname}
%defattr(0644,root,root,755)
%attr(0755,root,root) %{_libdir}/*.so.*

%files -n %{libnamedev}
%defattr(0644,root,root,755)
%{_includedir}/nessus/*
%{_libdir}/*.so
%{_libdir}/*.*a
%attr(0755,root,root) %{_bindir}/nasl-config
%attr(0755,root,root) %{_bindir}/nasl
%{_mandir}/man1/*
