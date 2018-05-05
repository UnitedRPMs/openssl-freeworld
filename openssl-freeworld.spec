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
Version: 1.1.0h
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
		shared no-ssl3-method enable-ec_nistp_64_gcc_128 zlib-dynamic \
		linux-x86_64 \
		"-Wa,--noexecstack ${CPPFLAGS} ${CFLAGS} ${LDFLAGS}"

	make depend
	make

%install
make DESTDIR=%{buildroot} MANDIR=/usr/share/man/%{name} MANSUFFIX=%{name} install_sw install_ssldirs install_man_docs

mkdir -p %{buildroot}/%{_libdir}/%{name}/engines-%{soversion}/
touch %{buildroot}/%{_libdir}/%{name}/libcrypto.so.%{soversion}
chmod 755 %{buildroot}/%{_libdir}/%{name}/libcrypto.so.%{soversion}

touch %{buildroot}/%{_libdir}/%{name}/libssl.so.%{soversion}
chmod 755 %{buildroot}/%{_libdir}/%{name}/libssl.so.%{soversion}

touch %{buildroot}/%{_libdir}/%{name}/engines-%{soversion}/afalg.so
chmod 755 %{buildroot}/%{_libdir}/%{name}/engines-%{soversion}/afalg.so

touch %{buildroot}/%{_libdir}/%{name}/engines-%{soversion}/capi.so
chmod 755 %{buildroot}/%{_libdir}/%{name}/engines-%{soversion}/capi.so

touch %{buildroot}/%{_libdir}/%{name}/engines-%{soversion}/padlock.so
chmod 755 %{buildroot}/%{_libdir}/%{name}/engines-%{soversion}/padlock.so

# Install profile and ld.so.config files
install -Dm755 %{S:1} "%{buildroot}/etc/profile.d/%{name}.sh"
install -Dm644 %{S:2} "%{buildroot}/etc/ld.so.conf.d/%{name}.conf"

%files
%license LICENSE
%{opt_openssl}/bin/
%{_sysconfdir}/%{name}/
%{_mandir}/%{name}
%{_sysconfdir}/profile.d/%{name}.sh

%files libs
%{opt_openssl}/%{_lib}/%{name}/libcrypto.so.%{soversion}
%{opt_openssl}/%{_lib}/%{name}/libssl.so.%{soversion}
%{opt_openssl}/%{_lib}/%{name}/engines-%{soversion}/*.so
%ghost %{_libdir}/%{name}/libcrypto.so.%{soversion}
%ghost %{_libdir}/%{name}/libssl.so.%{soversion}
%ghost %{_libdir}/%{name}/engines-%{soversion}/afalg.so
%ghost %{_libdir}/%{name}/engines-%{soversion}/capi.so
%ghost %{_libdir}/%{name}/engines-%{soversion}/padlock.so
%{_sysconfdir}/ld.so.conf.d/%{name}.conf

%files static
%{opt_openssl}/%{_lib}/%{name}/*.a

%files devel
%{opt_openssl}/%{_lib}/%{name}/*.so
%{opt_openssl}/%{_lib}/%{name}/pkgconfig/
%{opt_openssl}/include/openssl/

%pre
ln -sf %{opt_openssl}/%{_lib}/%{name}/libcrypto.so.%{soversion} %{_libdir}/%{name}/libcrypto.so.%{soversion}
ln -sf %{opt_openssl}/%{_lib}/%{name}/libssl.so.%{soversion} %{_libdir}/%{name}/libssl.so.%{soversion}
ln -sf %{opt_openssl}/%{_lib}/%{name}/afalg.so %{_libdir}/%{name}/engines-%{soversion}/afalg.so
ln -sf %{opt_openssl}/%{_lib}/%{name}/capi.so %{_libdir}/%{name}/engines-%{soversion}/capi.so
ln -sf %{opt_openssl}/%{_lib}/%{name}/padlock.so %{_libdir}/%{name}/engines-%{soversion}/padlock.so

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%changelog
