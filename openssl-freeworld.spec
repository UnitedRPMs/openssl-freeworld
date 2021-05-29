%global debug_package %{nil}

# For the curious:
# 0.9.5a soversion = 0
# 0.9.6  soversion = 1
# 0.9.6a soversion = 2
# 0.9.6c soversion = 3
# 0.9.7a soversion = 4
# 0.9.7ef soversion = 5
# 0.9.8ab soversion = 6
# 0.9.8g soversion = 7
# 0.9.8jk + EAP-FAST soversion = 8
# 1.0.0 soversion = 10
# 1.1.0 soversion = 1.1 (same as upstream although presence of some symbols
#                        depends on build configuration options)
%define soversion 1.1

%global opt_openssl /opt/openssl-freeworld

Summary: Utilities from the general purpose cryptography library with TLS implementation
Name: openssl-freeworld
Version: 1.1.1k
Release: 1%{?dist}

Source: https://www.openssl.org/source/openssl-%{version}.tar.gz
Source1: %{name}.sh
Source2: %{name}.conf
Patch:	ca-dir.patch

License: OpenSSL
Group: System Environment/Libraries
URL: http://www.openssl.org/
BuildRequires: gcc
BuildRequires: coreutils, krb5-devel, perl-interpreter, sed, zlib-devel, /usr/bin/cmp
BuildRequires: lksctp-tools-devel
BuildRequires: /usr/bin/rename
BuildRequires: /usr/bin/pod2man
BuildRequires: perl(Test::Harness), perl(Test::More), perl(Math::BigInt)
BuildRequires: perl(Module::Load::Conditional), perl(File::Temp)
BuildRequires: perl(Time::HiRes)
BuildRequires: perl(FindBin), perl(lib), perl(File::Compare), perl(File::Copy)
Requires: coreutils
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

%package libs
Summary: A general purpose cryptography library with TLS implementation
Group: System Environment/Libraries
Requires: ca-certificates >= 2008-5
Requires: crypto-policies

%description libs
OpenSSL is a toolkit for supporting cryptography. The openssl-libs
package contains the libraries that are used by various applications which
support cryptographic algorithms and protocols.

%package devel
Summary: Files for development of applications which will use OpenSSL
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: krb5-devel%{?_isa}, zlib-devel%{?_isa}
Requires: pkgconfig

%description devel
OpenSSL is a toolkit for supporting cryptography. The openssl-devel
package contains include files needed to develop applications which
support various cryptographic algorithms and protocols.

%package static
Summary:  Libraries for static linking of applications which will use OpenSSL
Group: Development/Libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description static
OpenSSL is a toolkit for supporting cryptography. The openssl-static
package contains static libraries needed for static linking of
applications which support various cryptographic algorithms and
protocols.

%prep
%autosetup -n openssl-%{version} -p 1

%build
	./Configure --prefix=/opt/%{name} --openssldir=/etc/%{name} --libdir=%{_lib}/%{name} \
		shared enable-ssl3-method enable-ssl3 enable-ec_nistp_64_gcc_128 zlib-dynamic \
		linux-x86_64 enable-md2 enable-camellia \
                enable-seed enable-rfc3779 \
	        enable-cms enable-rc5 enable-weak-ssl-ciphers \
                enable-sctp \
		"-Wa,--noexecstack ${CPPFLAGS} ${CFLAGS} ${LDFLAGS}"

	make depend
	make

%install
make DESTDIR=%{buildroot} MANDIR=/usr/share/man/%{name} MANSUFFIX=%{name} install_sw install_ssldirs install_man_docs

mkdir -p %{buildroot}/%{_libdir}/%{name}/engines-%{soversion}/
ln -sf ../../..%{opt_openssl}/%{_lib}/%{name}/libcrypto.so.%{soversion} %{buildroot}%{_libdir}/%{name}/libcrypto.so.%{soversion}
ln -sf ../../..%{opt_openssl}/%{_lib}/%{name}/libssl.so.%{soversion} %{buildroot}%{_libdir}/%{name}/libssl.so.%{soversion}
ln -sf ../../../..%{opt_openssl}/%{_lib}/%{name}/engines-%{soversion}/afalg.so %{buildroot}%{_libdir}/%{name}/engines-%{soversion}/afalg.so
ln -sf ../../../..%{opt_openssl}/%{_lib}/%{name}/engines-%{soversion}/capi.so %{buildroot}%{_libdir}/%{name}/engines-%{soversion}/capi.so
ln -sf ../../../..%{opt_openssl}/%{_lib}/%{name}/engines-%{soversion}/padlock.so %{buildroot}%{_libdir}/%{name}/engines-%{soversion}/padlock.so
# Install profile and ld.so.config files
#install -Dm755 %{S:1} "%{buildroot}/etc/profile.d/%{name}.sh"
#install -Dm644 %{S:2} "%{buildroot}/etc/ld.so.conf.d/%{name}.conf"

%files
%license LICENSE
%{opt_openssl}/bin/
%{_sysconfdir}/%{name}/
%{_mandir}/%{name}
#{_sysconfdir}/profile.d/{name}.sh

%files libs
%{opt_openssl}/%{_lib}/%{name}/libcrypto.so.%{soversion}
%{opt_openssl}/%{_lib}/%{name}/libssl.so.%{soversion}
%{opt_openssl}/%{_lib}/%{name}/engines-%{soversion}/*.so
%{_libdir}/%{name}/libcrypto.so.%{soversion}
%{_libdir}/%{name}/libssl.so.%{soversion}
%{_libdir}/%{name}/engines-%{soversion}/afalg.so
%{_libdir}/%{name}/engines-%{soversion}/capi.so
%{_libdir}/%{name}/engines-%{soversion}/padlock.so
#{_sysconfdir}/ld.so.conf.d/{name}.conf

%files static
%{opt_openssl}/%{_lib}/%{name}/*.a

%files devel
%{opt_openssl}/%{_lib}/%{name}/*.so
%{opt_openssl}/%{_lib}/%{name}/pkgconfig/
%{opt_openssl}/include/openssl/

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%changelog

* Fri May 28 2021 - David Va <davidva AT tutanota DOT com> 1.1.1k-1
- Updated to 1.1.1k release

* Wed May 20 2020 - David Va <davidva AT tutanota DOT com> 1.1.1g-1
- Updated to 1.1.1g release

* Wed Dec 25 2019 Sérgio Basto <sergio@serjux.com> - 1.1.1d-1
- Update to 1.1.1d release

* Tue Dec 24 2019 Sérgio Basto <sergio@serjux.com> - 1.1.1c-2
- Without ghost files and symlinks on pre install (of wrong package)


* Wed Jun 05 2019 - David Va <davidva AT tutanota DOT com> 1.1.1c-1
- Updated to 1.1.1c

* Sat May 05 2018 - David Va <davidva AT tutanota DOT com> 1.1.0h-1
- Initial build
