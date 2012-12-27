%define build_sys_rootcerts 1
%{?_without_sys_rootcerts: %{expand: %%global build_sys_rootcerts 0}}

%define name_orig	qca
%define qtcryptodir	%{qt4plugins}/crypto
%define lib_major	2
%define lib_name	%mklibname %{name_orig} %{lib_major}

Name:		qca2
Version:	2.0.3
Release:	2
License:	LGPL
Summary:	Straightforward and cross-platform crypto API for Qt
Group:		System/Libraries
URL:		http://delta.affinix.com/qca
# From kde support module
Source0:	%{name_orig}-%{version}.tar.xz
Patch0:		qca-2.0.3-gcc.patch
Patch1:		qca-botan-1.10.patch
BuildRequires:	qt4-devel >= 2:4.5
%if %{build_sys_rootcerts}
BuildRequires:	rootcerts
%endif
BuildRequires:	cmake
BuildRequires:	libgcrypt-devel
BuildRequires:	libsasl-devel
BuildRequires:	pkgconfig(nss)
Obsoletes:	qca >= 2.0
Requires:	%{lib_name} = %{version}-%{release}

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
Requires:	%{lib_name} = %{version}-%{release}

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

%package	-n %{lib_name}
Summary:	Libraries for QCA
Group:		System/Libraries
%if %{build_sys_rootcerts}
Requires:	rootcerts
Obsoletes:	%{name}-root-certificates < %{version}-%{release}
%else
Requires:	%{name}-root-certificates >= %{version}-%{release}
%endif

%description -n %{lib_name}
Libraries for QCA.

%files -n %{lib_name}
%dir %{qtcryptodir}
%defattr(0755,root,root,0755)
%{qt4lib}/libqca.so.%{lib_major}*

#------------------------------------------------------------------------------

%define libdev %mklibname -d qca

%package -n %{libdev}
Summary:	Development files for QCA
Group:		Development/KDE and Qt
Requires:	%{lib_name} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{mklibname qca 2 -d} = %{version}-%{release}

%description -n %{libdev}
Development files for QCA.

%files -n %{libdev}
%{_libdir}/pkgconfig/qca2.pc
%{qt4dir}/mkspecs/features/crypto.prf
%dir %{qt4include}/QtCrypto
%{qt4include}/QtCrypto/*
%{qt4lib}/libqca.so

#------------------------------------------------------------------------------

%package plugin-gnupg
Summary:	GnuPG plugin for QCA
Group:		Development/KDE and Qt
Provides:	qca2-gnupg = %{version}-%{release}
Provides:	qca-gnupg = %{version}-%{release}
Provides:	%{lib_name}-plugin-gnupg = %{version}-%{release}
Provides:	qca2-plugin-gnupg-%{_lib} = %{version}-%{release}
Obsoletes:	qca2-plugin-gnupg-%{_lib} < 2.0.0-5

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
Provides:	qca2-openssl = %{version}-%{release}
Provides:	qca-ossl = %{version}-%{release}
Provides:	qca2-tls = %{version}-%{release}
Provides:	%{lib_name}-plugin-openssl = %{version}-%{release}
Provides:	qca2-plugin-openssl-%{_lib} = %{version}-%{release}
Obsoletes:	qca2-plugin-openssl-%{_lib} < 2.0.0-5

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
Provides:	qca2-pkcs11 = %{version}-%{release}
Provides:	qca2-plugin-pkcs11-%{_lib} = %{version}-%{release}
Obsoletes:	qca2-plugin-pkcs11-%{_lib} < 2.0.0-5
Provides:	%{lib_name}-plugin-pkcs11 = %{version}-%{release}

%description plugin-pkcs11
This is a plugin to provide PKCS11 capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-pkcs11
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-pkcs11.*

#------------------------------------------------------------------------------

%package plugin-cyrus-sasl
Summary:	Cyrus-sasl plugin for QCA
Group:		Development/KDE and Qt
BuildRequires:	libsasl2-devel
Provides:	qca2-sasl = %{version}-%{release}
Provides:	qca2-plugin-cyrus-sasl-%{_lib} = %{version}-%{release}
Obsoletes:	qca2-plugin-cyrus-sasl-%{_lib} < 2.0.0-5
Provides:	%{lib_name}-plugin-cyrus-sasl = %{version}-%{release}

%description plugin-cyrus-sasl
This is a plugin to provide cyrus-sasl capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-cyrus-sasl
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-cyrus-sasl.*

#------------------------------------------------------------------------------

%package plugin-logger
Summary:	Logger plugin for QCA
Group:		Development/KDE and Qt
Provides:	qca2-logger = %{version}-%{release}
Provides:	qca2-plugin-logger-%{_lib} = %{version}-%{release}
Obsoletes:	qca2-plugin-logger-%{_lib} < 2.0.0-5
Provides:	%{lib_name}-plugin-logger = %{version}-%{release}

%description plugin-logger
This is a plugin to provide logger capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-logger
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-logger.*

#------------------------------------------------------------------------------

%package plugin-gcrypt
Summary:	GCrypt plugin for QCA
Group:		Development/KDE and Qt
Provides:	qca2-gcrypt = %{version}-%{release}
Provides:	qca2-plugin-gcrypt-%{_lib} = %{version}-%{release}
Obsoletes:	qca2-plugin-gcrypt-%{_lib} < 2.0.0-5
Provides:	%{lib_name}-plugin-gcrypt = %{version}-%{release}

%description plugin-gcrypt
This is a plugin to provide gcrypt capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-gcrypt
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-gcrypt.*

#------------------------------------------------------------------------------

%package plugin-nss
Summary:	Logger plugin for QCA
Group:		Development/KDE and Qt
Provides:	qca2-nss = %{version}-%{release}
Provides:	qca2-plugin-nss-%{_lib} = %{version}-%{release}
Obsoletes:	qca2-plugin-nss-%{_lib} < 2.0.0-5
Provides:	%{lib_name}-plugin-nss = %{version}-%{release}

%description plugin-nss
This is a plugin to provide nss capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-nss
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-nss.*

#------------------------------------------------------------------------------

%package plugin-softstore
Summary:	Logger plugin for QCA
Group:		Development/KDE and Qt
Provides:	qca2-softstore = %{version}-%{release}
Provides:	qca2-plugin-softstore-%{_lib} = %{version}-%{release}
Obsoletes:	qca2-plugin-softstore-%{_lib} < 2.0.0-5
Provides:	%{lib_name}-plugin-softstore = %{version}-%{release}

%description plugin-softstore
This is a plugin to provide softstore capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-softstore
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-softstore.*

#------------------------------------------------------------------------------

%package plugin-botan
Summary:	Botan plugin for QCA
Group:		Development/KDE and Qt
Provides:	qca2-botan = %{version}-%{release}
Provides:	%{lib_name}-plugin-botan = %{version}-%{release}

%description plugin-botan
This is a plugin to allow the Qt Cryptographic Architecture (QCA) to
use the Botan cryptography library as its backend.

%files plugin-botan
%attr(0755,root,root) %{qt4plugins}/crypto/libqca-botan.*

#------------------------------------------------------------------------------

%prep
%setup -q -n %{name_orig}-%{version}
%patch0 -p1
%patch1 -p1 -b .botan-1.10~

%build
%cmake_qt4 \
	-DCMAKE_INSTALL_PREFIX=%{qt4dir} \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DPKGCONFIG_INSTALL_PREFIX=%{_libdir}/pkgconfig \
	-DBOTANCONFIG_EXECUTABLE=%_bindir/botan-config-1.10
%make


%install
%makeinstall_std -C build

# Make directory for plugins
install -d -m 755 %{buildroot}/%{qtcryptodir}

mkdir -p %{buildroot}%{_mandir}
mv %{buildroot}%{qt4dir}/share/man/man1 %{buildroot}%{_mandir}


%changelog
* Sun Oct 23 2011 José Melo <ze@mandriva.org> 2.0.3-1
+ Revision: 705764
- xz source
- no need to list doc files in a lib package
- xz source
- seams source file was not commited...
- 2.0.3
- remove useless macro
- clean buildroot and defattr
- remove clean section
- drop mkrel

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 2.0.2-6.1111917.4
+ Revision: 669367
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0.2-6.1111917.3mdv2011.0
+ Revision: 607259
- rebuild

* Wed Apr 07 2010 Funda Wang <fwang@mandriva.org> 2.0.2-6.1111917.1mdv2010.1
+ Revision: 532464
- use upstream new snapshot with all patches merged

  + Eugeni Dodonov <eugeni@mandriva.com>
    - Properly check if openssl has md2 enabled.
    - Disable md2 to comply with openssl 1.0.0.

* Tue Apr 06 2010 Funda Wang <fwang@mandriva.org> 2.0.2-6.1081513.1mdv2010.1
+ Revision: 532172
- build with latest kde snapshot (for openssl 1.0)
- rebuild for new openssl

* Thu Mar 25 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0.2-5mdv2010.1
+ Revision: 527401
- rebuilt against nss-3.12.6

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0.2-4mdv2010.1
+ Revision: 511633
- rebuilt against openssl-0.9.8m

* Sun Oct 04 2009 Funda Wang <fwang@mandriva.org> 2.0.2-3mdv2010.0
+ Revision: 453291
- finally fix linkage
- obsoletes old qca-2.x

* Tue Sep 01 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.0.2-2mdv2010.0
+ Revision: 423714
- rebuild

  + Helio Chissini de Castro <helio@mandriva.com>
    - New upstream version extracted from kdesupport module
    - Rename devel and plugin package names.

  + Adam Williamson <awilliamson@mandriva.org>
    - turn qca2 back into plain old qca #3
    - turn qca2 back into plain old qca #2
    - turn qca2 back into plain old qca

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun Jun 08 2008 Funda Wang <fwang@mandriva.org> 2.0.1-2mdv2009.0
+ Revision: 216809
- conflicts with qca1-devel for /usr/lib/libqca.so

* Mon Jun 02 2008 Helio Chissini de Castro <helio@mandriva.com> 2.0.1-1mdv2009.0
+ Revision: 214395
- New upstream version, 2.0.1, needed for current KDE 4.
- Plugins are back for good. No more conflicts. Plugin naming package are kept to avoid upgrade issues.
- qcatool bin link are removed. qt4 is main now

* Tue May 27 2008 Helio Chissini de Castro <helio@mandriva.com> 2.0.0-3mdv2009.0
+ Revision: 211908
- Qt libraries and plugins are in _libdir now

* Tue May 27 2008 Helio Chissini de Castro <helio@mandriva.com> 2.0.0-2mdv2009.0
+ Revision: 211495
- Rebuild against new qt4

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Oct 29 2007 Nicolas Lécureuil <nlecureuil@mandriva.com> 2.0.0-1mdv2008.1
+ Revision: 103550
- 2.0.0
  Remove merged patch

* Sun Sep 16 2007 David Walluck <walluck@mandriva.org> 2.0.0-0.beta7.4mdv2008.0
+ Revision: 88024
- add symlink from qca.pc to qca2.pc for debian compat

* Fri Aug 10 2007 Helio Chissini de Castro <helio@mandriva.com> 2.0.0-0.beta7.3mdv2008.0
+ Revision: 61634
- Minor spec fix

* Fri Jul 06 2007 Helio Chissini de Castro <helio@mandriva.com> 2.0.0-0.beta7.2mdv2008.0
+ Revision: 49132
- Add patch for proper extended cmake crypto entries

* Fri Jul 06 2007 Helio Chissini de Castro <helio@mandriva.com> 2.0.0-0.beta7.1mdv2008.0
+ Revision: 49006
- beta 7
- Mofified to match the cmake qt4 macros

* Thu Jun 28 2007 Nicolas Lécureuil <nlecureuil@mandriva.com> 2.0.0-0.beta6.1mdv2008.0
+ Revision: 45494
- New version beta6

* Tue Apr 24 2007 Laurent Montel <lmontel@mandriva.org> 2.0-0.beta2.8mdv2008.0
+ Revision: 17762
- Fix buildrequires
- New version (need by kopete2)


* Tue Jan 09 2007 Laurent Montel <lmontel@mandriva.com> 2.0-0.beta2.7mdv2007.0
+ Revision: 106622
- Update from branch
- Provides as libqca2-devel and not libqca which is build against qt3
  and not qt4

  + cdugal <cdugal>
    - Removed version require for rootcerts.
    - Cleaned up spec.

  + Andreas Hasenack <andreas@mandriva.com>
    - renamed mdv to packages because mdv is too generic and it's hosting only packages anyway

  + Helio Chissini de Castro <helio@mandriva.com>
    - Removed wrong provides on static-devel
    - Cliff Dugal's changes
    - Fixed devel Provides as per Buchan Milne's instructions
    - mklibname in a macro, then use that macro for Provides
    - Minor modfication from Cliff Dugal and Davi Walluck
    - qt4 is not nice with parallel building :-(
    - New layout for package. Thanks to Cliff Dugal for his work.
    - New upstream release beta2
    - New package thanks to Cliff Dugal. Post adjusts will be needed
    - Fix pkgconfig install dir
    - Fix typo
    - Be assure that lib is installed in proper arch dir
    - First package for qca2 ready. A good solution to sit in Qt space for this
      specific qca sets comes to avoid problems between old and new qca packages
    - Copy old qca package to create new qca2 package
      A    svn+ssh://helio@svn.mandriva.com/svn/mdv/cooker/qca2
    - Proper patch for libdir
    - Patch for lib64 should be applied just for 64
    - Initial svn import
    - Relocate plugins for correct arch path, lib64 or lib.
    - Cleaned spec removing old perl changes for lib64. Now just one patch is needed
    - Create current for qca package

