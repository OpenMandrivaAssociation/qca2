%define build_debug 1
%{?_with_debug: %{expand: %%global build_debug 1}}

%define build_sys_rootcerts 1
%{?_without_sys_rootcerts: %{expand: %%global build_sys_rootcerts 0}}

%define branch_date 20070424

%define name_orig	qca
%define qtdir		%{_prefix}/lib/qt4
%define libqtcore4	%mklibname qtcore 4
%define qtcryptodir	%{qtdir}/plugins/%{_lib}/crypto
%define lib_major	2
%define lib_name	%mklibname %{name_orig} %{lib_major}
%define source_ver	%{version}-%branch_date
%define build_pkcs11    0

Name:		qca2
Version:	2.0
Release:	%mkrel 0.beta2.8
License:	LGPL
Summary:	Straightforward and cross-platform crypto API for Qt
Group:		System/Libraries
URL:		http://delta.affinix.com/qca
########################################################################################
#it is now part of kde : You can find it here:  http://webcvs.kde.org//kdesupport/qca/ #
########################################################################################
Source0:	http://delta.affinix.com/download/qca/%{version}/beta2/%{name_orig}-%{source_ver}.tar.bz2
# Patch0 should not be necessary, but Qt 4 in Cooker currently builds everything as
# debug, regardless that the documentation says that it should build as release. This
# breaks QCA's build.
Patch0:		%{name_orig}-2.0-beta2-config-release.patch
# I don't know if Patch1 is necessary for when Qt 4 in Cooker is fixed. Just in case
# it is needed, I'm leaving it here (it can't hurt). (This patch is the opposite of 0.)
Patch1:		%{name_orig}-2.0-beta2-config-debug.patch
# Patch2 allows one to force QCA to use the bundled certs.
Patch2:		%{name_orig}-2.0-beta2-certs-bundled.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	%{lib_name} = %{version}-%{release}
# Only Qt 4.1 is really needed, but older Qt RPMs had a different
# directory structure, so require a newer Qt RPM
BuildRequires:	qt4-devel >= 2:4.2
%if %{build_sys_rootcerts}
BuildRequires:	rootcerts
%endif
BuildRequires: cmake
BuildRequires:	libgcrypt-devel
BuildRequires:	libsasl-devel

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
%{qtdir}/bin/qcatool
%{_bindir}/qca2tool

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
%dir %{qtdir}/share/qca
%dir %{qtdir}/share/qca/certs
%doc %{qtdir}/share/qca/certs/README
%{qtdir}/share/qca/certs/rootcerts.pem
%endif

#------------------------------------------------------------------------------

%package	-n %{lib_name}
Summary:	Libraries for QCA
Group:		System/Libraries
# Older Qt RPMs had a different directory structure, so require a newer Qt RPM
Requires:	%{libqtcore4} >= 2:4.1.1
%if %{build_sys_rootcerts}
Requires:	rootcerts
Obsoletes:	%{name}-root-certificates
%else
Requires:	%{name}-root-certificates >= %{version}
%endif
Obsoletes:	%{lib_name}-static-devel 

%description	-n %{lib_name}
Libraries for QCA.

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%files -n %{lib_name}
%defattr(0644,root,root,0755)
%doc README COPYING INSTALL TODO
%dir %{qtcryptodir}
%defattr(0755,root,root,0755)
%{qtdir}/%{_lib}/libqca.so.*

#------------------------------------------------------------------------------

%package	-n %{lib_name}-devel
Summary:	Development files for QCA
Group:		Development/KDE and Qt
Requires:	%{lib_name} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description	-n %{lib_name}-devel
Development files for QCA.

%files	-n %{lib_name}-devel
%defattr(0644,root,root,0755)
%{_libdir}/pkgconfig/qca.pc
%dir %{qtdir}/include/QtCrypto
%{qtdir}/include/QtCrypto/*.h
%{qtdir}/include/QtCrypto/QtCrypto
%{qtdir}/%{_lib}/libqca.so
#%{qtdir}/mkspecs/features/crypto.prf


%package -n %{lib_name}-plugin-gnupg
Summary: GnuPG plugin for QCA
Group: Development/KDE and Qt
Requires: %{lib_name} >= 2.0
Requires: gnupg
Provides: qca2-plugin-gnupg
Obsoletes:	qca2-plugin-gnupg-%{_lib}


%description -n %{lib_name}-plugin-gnupg
This is a plugin to provide GnuPG capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-gnupg
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qtdir}/plugins/%{_lib}/crypto/libqca-gnupg.so

#------------------------------------------------------------------------------

%package -n %{lib_name}-plugin-openssl
Summary:       OpenSSL plugin for QCA
Group:         Development/KDE and Qt
Requires: %{lib_name} >= 2.0
BuildRequires: openssl-devel
Provides: qca2-plugin-openssl
Obsoletes:  qca2-plugin-openssl-%{_lib}

%description -n %{lib_name}-plugin-openssl
This is a plugin to provide OpenSSL capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-openssl
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{qtdir}/plugins/%{_lib}/crypto/libqca-openssl.so

#------------------------------------------------------------------------------
%if %build_pkcs11
%package -n %{lib_name}-plugin-pkcs11
Summary: PKCS11 plugin for QCA
Group: Development/KDE and Qt
Requires: %{lib_name} >= 2.0
BuildRequires: openssl-devel
Provides: qca2-plugin-pkcs11
Obsoletes:	qca2-plugin-pkcs11-%{_lib}

%description -n %{lib_name}-plugin-pkcs11
This is a plugin to provide PKCS11 capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-pkcs11
%defattr(0644,root,root,0755)
%attr(0755,root,root) 
%{qtdir}/plugins/%{_lib}/crypto/libqca-pkcs11.so
%endif


%package -n %{lib_name}-plugin-cyrus-sasl
Summary: cyrus-sasl plugin for QCA
Group: Development/KDE and Qt
Requires: %{lib_name} >= 2.0
BuildRequires: openssl-devel
Provides: qca2-plugin-cyrus-sasl

%description -n %{lib_name}-plugin-cyrus-sasl
This is a plugin to provide cyrus-sasl capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-cyrus-sasl
%defattr(0644,root,root,0755)
%attr(0755,root,root)
%{qtdir}/plugins/%{_lib}/crypto/libqca-cyrus-sasl.so


%package -n %{lib_name}-plugin-gcrypt
Summary: gcrypt plugin for QCA
Group: Development/KDE and Qt
Requires: %{lib_name} >= 2.0
BuildRequires: openssl-devel
Provides: qca2-plugin-gcrypt

%description -n %{lib_name}-plugin-gcrypt
This is a plugin to provide gcrypt capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-gcrypt
%defattr(0644,root,root,0755)
%attr(0755,root,root)
%{qtdir}/plugins/%{_lib}/crypto/libqca-gcrypt.so


%package -n %{lib_name}-plugin-logger
Summary: logger plugin for QCA
Group: Development/KDE and Qt
Requires: %{lib_name} >= 2.0
BuildRequires: openssl-devel
Provides: qca2-plugin-gcrypt

%description -n %{lib_name}-plugin-logger
This is a plugin to provide gcrypt capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-logger
%defattr(0644,root,root,0755)
%attr(0755,root,root)
%{qtdir}/plugins/%{_lib}/crypto/libqca-logger.so



%package -n %{lib_name}-plugin-nss
Summary: nss plugin for QCA
Group: Development/KDE and Qt
Requires: %{lib_name} >= 2.0
BuildRequires: openssl-devel
Provides: qca2-plugin-gcrypt

%description -n %{lib_name}-plugin-nss
This is a plugin to provide gcrypt capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files -n %{lib_name}-plugin-nss
%defattr(0644,root,root,0755)
%attr(0755,root,root)
%{qtdir}/plugins/%{_lib}/crypto/libqca-nss.so


#------------------------------------------------------------------------------

%prep
%setup -q -n %{name_orig}-%{source_ver}
#%if %{build_debug}
#%patch1 -p1 -b .debugpatch
#%else
#%patch0 -p1 -b .releasepatch
#%endif
#%patch2 -p1 -b .certstorepathfix


%build
cd $RPM_BUILD_DIR/%{name_orig}-%{source_ver}
mkdir build
cd build
export QTDIR=/usr/lib/qt4/
export PATH=$QTDIR/bin:$PATH
cmake -DCMAKE_INSTALL_PREFIX=$QTDIR  \
%if "%{_lib}" != "lib"
      	-DLIB_SUFFIX=64 \
%endif
	../

%make


%install
rm -rf %{buildroot}
cd $RPM_BUILD_DIR/%{name_orig}-%{source_ver}
cd build

make DESTDIR=%buildroot install

# Make directory for plugins
install -d -m 755 %{buildroot}/%{qtcryptodir}

# Move pkgconfig files to right place
install -d -m 755 %{buildroot}/%{_libdir}
mv %{buildroot}/%{qtdir}/%_lib/pkgconfig %{buildroot}/%{_libdir}/

# Make symlink in /usr/bin to qcatool
install -d -m 755 %{buildroot}/%{_bindir}
ln -s %{qtdir}/bin/qcatool %{buildroot}/%{_bindir}/qca2tool

%if %{build_debug} && %{?_enable_debug_packages:0}%{!?_enable_debug_packages:1}
# Tell spec-helper not to stip files.
export DONT_STRIP=1
%endif


%clean
rm -rf %buildroot



