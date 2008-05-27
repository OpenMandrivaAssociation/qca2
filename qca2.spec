%define build_debug 0
%{?_with_debug: %{expand: %%global build_debug 1}}

%define build_sys_rootcerts 1
%{?_without_sys_rootcerts: %{expand: %%global build_sys_rootcerts 0}}

%define name_orig	qca
%define qtcryptodir	%{qt4plugins}/crypto
%define lib_major	2
%define lib_name	%mklibname %{name_orig} %{lib_major}
%define source_ver	%{version}

Name: qca2
Version: 2.0.0
Release: %mkrel 2
License: LGPL
Summary: Straightforward and cross-platform crypto API for Qt
Group: System/Libraries
URL: http://delta.affinix.com/qca
Source0: http://delta.affinix.com/download/qca/%{version}/beta7/%{name_orig}-%{source_ver}.tar.bz2
Patch0:	%{name_orig}-2.0.0-beta6-fixbuild.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: qt4-devel >= 2:4.2
%if %{build_sys_rootcerts}
BuildRequires: rootcerts
%endif
BuildRequires: cmake
BuildRequires: libgcrypt-devel
BuildRequires: libsasl-devel
BuildRequires: nss-devel
Requires: qt4-common >= 4.3

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
%_bindir/qcatool

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
%{qt4lib}/libqca.so.*

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
%{_libdir}/pkgconfig/qca2.pc
%{qt4dir}/mkspecs/features/crypto.prf
%dir %{qt4include}/QtCrypto
%{qt4include}/QtCrypto/*
%{qt4lib}/libqca.so

#------------------------------------------------------------------------------
%prep
%setup -q -n %{name_orig}-%{source_ver}
%patch0 -p0

%build
%cmake_qt4 \
	-DCMAKE_INSTALL_PREFIX=$QTDIR 

%make


%install
rm -rf %{buildroot}
cd build

make DESTDIR=%buildroot install

# Make directory for plugins
install -d -m 755 %{buildroot}/%{qtcryptodir}

# Move pkgconfig files to right place
install -d -m 755 %{buildroot}/%{_libdir}
mv %{buildroot}/%{qt4dir}/%_lib/pkgconfig %{buildroot}/%{_libdir}/
ln -s qca.pc %{buildroot}%{_libdir}/pkgconfig/qca2.pc

# qcatool on bindir until qt4 is main env
install -d -m 755 %{buildroot}/%{_bindir}
ln -s %{qt4dir}/bin/qcatool %{buildroot}/%{_bindir}/qcatool

%clean
rm -rf %buildroot



