%define build_sys_rootcerts 1
%{?_without_sys_rootcerts: %{expand: %%global build_sys_rootcerts 0}}

%define name_orig	qca
%define qtcryptodir	%{qt4plugins}/crypto
%define lib_major	2
%define lib_name	%mklibname %{name_orig} %{lib_major}
%define source_ver	%{version}

Name: qca2
Version: 2.0.2
Release: %mkrel 5
License: LGPL
Summary: Straightforward and cross-platform crypto API for Qt
Group: System/Libraries
URL: http://delta.affinix.com/qca
# From kde support module
Source: %{name_orig}-%{source_ver}.tar.bz2
Patch0: qca-2.0.2-fix-linkage.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: qt4-devel >= 2:4.5
%if %{build_sys_rootcerts}
BuildRequires: rootcerts
%endif
BuildRequires: cmake
BuildRequires: libgcrypt-devel
BuildRequires: libsasl-devel
BuildRequires: nss-devel
Obsoletes: qca >= 2.0

%description
The QCA library provides an easy API for a range of cryptographic
features, including SSL/TLS, X.509 certificates, SASL, symmetric
ciphers, public key ciphers, hashes and much more.

Functionality is supplied via plugins. This is useful for avoiding
dependence on a particular crypto library and makes upgrading easier,
as there is no need to recompile your application when adding or
upgrading a crypto plugin. Also, by pushing crypto functionality into
plugins, applications are free of legal issues, such as export
regulation.

%files
%defattr(0644,root,root,0755)
%doc README COPYING INSTALL TODO
%defattr(0755,root,root,0755)
%{qt4dir}/bin/qcatool2
%_mandir/man1/*

#------------------------------------------------------------------------------

%if ! %{build_sys_rootcerts}
%package -n %{name}-root-certificates
Summary:	Common root CA certificates for QCA
Group:		System/Libraries
Requires:	%{lib_name} = %{version}-%{release}

%description	-n %{name}-root-certificates
Provides root Certificate Authority certificates for the QCA library.
These certificates are the same ones that are included in Mozilla.

%files -n %{name}-root-certificates
%defattr(0644,root,root,0755)
%dir %{qt4dir}/share/qca
%dir %{qt4dir}/share/qca/certs
%doc %{qt4dir}/share/qca/certs/README
%{qt4dir}/share/qca/certs/rootcerts.pem
%endif

#------------------------------------------------------------------------------

%package	-n %{lib_name}
Summary:	Libraries for QCA
Group:		System/Libraries
%if %{build_sys_rootcerts}
Requires: rootcerts
Obsoletes: %{name}-root-certificates
%else
Requires: %{name}-root-certificates >= %{version}
%endif
Obsoletes: %{mklibname qca 2 -d -s}
Obsoletes: %{mklibname qca 2 -s}

%description	-n %{lib_name}
Libraries for QCA.

%files -n %{lib_name}
%defattr(0644,root,root,0755)
%doc README COPYING INSTALL TODO
%dir %{qtcryptodir}
%defattr(0755,root,root,0755)
%{qt4lib}/libqca.so.*

#------------------------------------------------------------------------------

%define libdev %mklibname -d qca 

%package -n %{libdev}
Summary: Development files for QCA
Group: Development/KDE and Qt
Requires: %{lib_name} = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}
Provides: %{mklibname qca 2 -d} = %{version}-%{release}
Obsoletes: %{mklibname qca 2 -d -s}
Obsoletes: %{mklibname qca 2 -s}

%description -n %{libdev}
Development files for QCA.

%files -n %{libdev}
%defattr(0644,root,root,0755)
%{_libdir}/pkgconfig/qca2.pc
%{qt4dir}/mkspecs/features/crypto.prf
%dir %{qt4include}/QtCrypto
%{qt4include}/QtCrypto/*
%{qt4lib}/libqca.so

#------------------------------------------------------------------------------

%package plugin-gnupg
Summary: GnuPG plugin for QCA
Group: Development/KDE and Qt
Provides: qca2-gnupg = %version
Provides: %{lib_name}-plugin-gnupg = %version
Obsoletes: %{lib_name}-plugin-gnupg < %version
Provides: qca2-plugin-gnupg-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-gnupg-%{_lib} < 2.0.0-5

%description plugin-gnupg
This is a plugin to provide GnuPG capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-gnupg
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-gnupg.*

#------------------------------------------------------------------------------

%package plugin-openssl
Summary: OpenSSL plugin for QCA
Group: Development/KDE and Qt
BuildRequires: openssl-devel
Provides: qca2-openssl = %version
Provides: qca2-tls = %version
Provides: qca2-plugin-openssl-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-openssl-%{_lib} < 2.0.0-5
Provides: %{lib_name}-plugin-openssl = %version
Obsoletes: %{lib_name}-plugin-openssl < %version

%description plugin-openssl
This is a plugin to provide OpenSSL capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-openssl
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-ossl.*

#------------------------------------------------------------------------------

%package plugin-pkcs11
Summary: PKCS11 plugin for QCA
Group: Development/KDE and Qt
BuildRequires: openssl-devel
BuildRequires: pkcs11-helper-devel
Provides: qca2-pkcs11 = %version
Provides: qca2-plugin-pkcs11-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-pkcs11-%{_lib} < 2.0.0-5
Provides: %{lib_name}-plugin-pkcs11 = %version
Obsoletes: %{lib_name}-plugin-pkcs11 < %version

%description plugin-pkcs11
This is a plugin to provide PKCS11 capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-pkcs11
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-pkcs11.*

#------------------------------------------------------------------------------

%package plugin-cyrus-sasl
Summary: Cyrus-sasl plugin for QCA
Group: Development/KDE and Qt
BuildRequires: libsasl2-devel
Provides: qca2-sasl = %version
Provides: qca2-plugin-cyrus-sasl-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-cyrus-sasl-%{_lib} < 2.0.0-5
Provides: %{lib_name}-plugin-cyrus-sasl = %version
Obsoletes: %{lib_name}-plugin-cyrus-sasl < %version

%description plugin-cyrus-sasl
This is a plugin to provide cyrus-sasl capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-cyrus-sasl
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-cyrus-sasl.*

#------------------------------------------------------------------------------

%package plugin-logger
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca2-logger = %version
Provides: qca2-plugin-logger-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-logger-%{_lib} < 2.0.0-5
Provides: %{lib_name}-plugin-logger = %version
Obsoletes: %{lib_name}-plugin-logger < %version

%description plugin-logger
This is a plugin to provide logger capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-logger
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-logger.*

#------------------------------------------------------------------------------

%package plugin-gcrypt
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca2-gcrypt = %version
Provides: qca2-plugin-gcrypt-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-gcrypt-%{_lib} < 2.0.0-5
Provides: %{lib_name}-plugin-gcrypt = %version
Obsoletes: %{lib_name}-plugin-gcrypt < %version

%description plugin-gcrypt
This is a plugin to provide gcrypt capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-gcrypt
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-gcrypt.*

#------------------------------------------------------------------------------

%package plugin-nss
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca2-nss = %version
Provides: qca2-plugin-nss-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-nss-%{_lib} < 2.0.0-5
Provides: %{lib_name}-plugin-nss = %version
Obsoletes: %{lib_name}-plugin-nss < %version

%description plugin-nss
This is a plugin to provide nss capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-nss
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-nss.*

#------------------------------------------------------------------------------

%package plugin-softstore
Summary: Logger plugin for QCA
Group: Development/KDE and Qt
Provides: qca2-softstore = %version
Provides: qca2-plugin-softstore-%{_lib} = %{version}-%{release}
Obsoletes: qca2-plugin-softstore-%{_lib} < 2.0.0-5
Provides: %{lib_name}-plugin-softstore = %version
Obsoletes: %{lib_name}-plugin-softstore < %version

%description plugin-softstore
This is a plugin to provide softstore capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-softstore
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-softstore.*

#------------------------------------------------------------------------------

%prep
%setup -q -n %{name_orig}-%{source_ver}
%patch0 -p0

%build
%cmake_qt4 \
	-DCMAKE_INSTALL_PREFIX=%{qt4dir} \
	-DLIB_INSTALL_DIR=%_libdir \
	-DPKGCONFIG_INSTALL_PREFIX=%_libdir/pkgconfig

%make


%install
rm -rf %{buildroot}
%makeinstall_std -C build

# Make directory for plugins
install -d -m 755 %{buildroot}/%{qtcryptodir}

mkdir -p %{buildroot}/%{_mandir}
mv %{buildroot}/%qt4dir/share/man/man1 %{buildroot}/%{_mandir}

%clean
rm -rf %buildroot
