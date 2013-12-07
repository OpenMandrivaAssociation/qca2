%define build_sys_rootcerts 1
%{?_without_sys_rootcerts: %{expand: %%global build_sys_rootcerts 0}}

%define qtcryptodir	%{qt4plugins}/crypto
%define oname	qca
%define major	2
%define libname	%mklibname %{oname} %{major}
%define devname %mklibname -d qca


Summary:	Straightforward and cross-platform crypto API for Qt
Name:		qca2
Version:	2.0.3
Release:	4
License:	LGPLv2
Group:		System/Libraries
Url:		http://delta.affinix.com/qca
# From kde support module
Source0:	%{oname}-%{version}.tar.xz
Patch0:		qca-2.0.3-gcc.patch
Patch1:		qca-botan-1.10.patch
%if %{build_sys_rootcerts}
BuildRequires:	rootcerts
%endif
BuildRequires:	cmake
BuildRequires:	qt4-devel >= 2:4.5
BuildRequires:	sasl-devel = 2.1.25
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	pkgconfig(nss)

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
%doc README COPYING INSTALL TODO
%{_mandir}/man1/*
%defattr(0755,root,root,0755)
%{qt4dir}/bin/qcatool2

#------------------------------------------------------------------------------

%if ! %{build_sys_rootcerts}
%package -n %{name}-root-certificates
Summary:	Common root CA certificates for QCA
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description	-n %{name}-root-certificates
Provides root Certificate Authority certificates for the QCA library.
These certificates are the same ones that are included in Mozilla.

%files -n %{name}-root-certificates
%dir %{qt4dir}/share/qca
%dir %{qt4dir}/share/qca/certs
%doc %{qt4dir}/share/qca/certs/README
%{qt4dir}/share/qca/certs/rootcerts.pem
%endif

#------------------------------------------------------------------------------

%package	-n %{libname}
Summary:	Libraries for QCA
Group:		System/Libraries
%if %{build_sys_rootcerts}
Requires:	rootcerts
Obsoletes:	%{name}-root-certificates < %{version}-%{release}
%else
Requires:	%{name}-root-certificates >= %{version}-%{release}
%endif

%description -n %{libname}
Libraries for QCA.

%files -n %{libname}
%dir %{qtcryptodir}
%defattr(0755,root,root,0755)
%{qt4lib}/libqca.so.%{major}*

#------------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for QCA
Group:		Development/KDE and Qt
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Development files for QCA.

%files -n %{devname}
%{_libdir}/pkgconfig/qca2.pc
%{qt4dir}/mkspecs/features/crypto.prf
%dir %{qt4include}/QtCrypto
%{qt4include}/QtCrypto/*
%{qt4lib}/libqca.so

#------------------------------------------------------------------------------

%package plugin-gnupg
Summary:	GnuPG plugin for QCA
Group:		Development/KDE and Qt

%description plugin-gnupg
This is a plugin to provide GnuPG capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-gnupg
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-gnupg.*

#------------------------------------------------------------------------------

%package plugin-openssl
Summary:	OpenSSL plugin for QCA
Group:		Development/KDE and Qt
BuildRequires:	pkgconfig(openssl)
Provides:	qca2-plugin-openssl-%{_lib} = %{version}-%{release}

%description plugin-openssl
This is a plugin to provide OpenSSL capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-openssl
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-ossl.*

#------------------------------------------------------------------------------

%package plugin-pkcs11
Summary:	PKCS11 plugin for QCA
Group:		Development/KDE and Qt
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libpkcs11-helper-1)

%description plugin-pkcs11
This is a plugin to provide PKCS11 capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-pkcs11
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-pkcs11.*

#------------------------------------------------------------------------------

%package plugin-cyrus-sasl
Summary:	Cyrus-sasl plugin for QCA
Group:		Development/KDE and Qt
BuildRequires:	sasl-devel

%description plugin-cyrus-sasl
This is a plugin to provide cyrus-sasl capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-cyrus-sasl
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-cyrus-sasl.*

#------------------------------------------------------------------------------

%package plugin-logger
Summary:	Logger plugin for QCA
Group:		Development/KDE and Qt

%description plugin-logger
This is a plugin to provide logger capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-logger
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-logger.*

#------------------------------------------------------------------------------

%package plugin-gcrypt
Summary:	GCrypt plugin for QCA
Group:		Development/KDE and Qt

%description plugin-gcrypt
This is a plugin to provide gcrypt capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-gcrypt
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-gcrypt.*

#------------------------------------------------------------------------------

%package plugin-nss
Summary:	Logger plugin for QCA
Group:		Development/KDE and Qt

%description plugin-nss
This is a plugin to provide nss capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-nss
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-nss.*

#------------------------------------------------------------------------------

%package plugin-softstore
Summary:	Logger plugin for QCA
Group:		Development/KDE and Qt

%description plugin-softstore
This is a plugin to provide softstore capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-softstore
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-softstore.*

#------------------------------------------------------------------------------

%package plugin-botan
Summary:	Botan plugin for QCA
Group:		Development/KDE and Qt
BuildRequires:	pkgconfig(botan-1.10)

%description plugin-botan
This is a plugin to allow the Qt Cryptographic Architecture (QCA) to
use the Botan cryptography library as its backend.

%files plugin-botan
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-botan.*

#------------------------------------------------------------------------------

%prep
%setup -qn %{oname}-%{version}
%apply_patches

%build
%cmake_qt4 \
	-DCMAKE_INSTALL_PREFIX=%{qt4dir} \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DPKGCONFIG_INSTALL_PREFIX=%{_libdir}/pkgconfig \
	-DBOTANCONFIG_EXECUTABLE=%{_bindir}/botan-config-1.10
%make

%install
%makeinstall_std -C build

# Make directory for plugins
install -d -m 755 %{buildroot}/%{qtcryptodir}

mkdir -p %{buildroot}%{_mandir}
mv %{buildroot}%{qt4dir}/share/man/man1 %{buildroot}%{_mandir}

