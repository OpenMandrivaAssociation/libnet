%define	major 1
%define libname %mklibname net %{major}
%define develname %mklibname net -d

Summary:	A C library for portable packet creation
Name:		libnet
Version:	1.1.6
Release:	2
License:	BSD
Group:		System/Libraries
URL:		http://www.sourceforge.net/projects/libnet-dev/
Source0:	http://downloads.sourceforge.net/libnet-dev/%{name}-%{version}.tar.gz
BuildRequires:	libpcap-devel


%description
Libnet is an API to help with the construction and handling of network packets.
It provides a portable framework for low-level network packet writing and
handling (use libnet in conjunction with libpcap and you can write some really
cool stuff). Libnet includes packet creation at the IP layer and at the link
layer as well as a host of supplementary and complementary functionality.

%package -n	%{libname}
Summary:	A C library for portable packet creation
Group: 		System/Libraries

%description -n	%{libname}
Libnet is an API to help with the construction and handling of network packets.
It provides a portable framework for low-level network packet writing and
handling (use libnet in conjunction with libpcap and you can write some really
cool stuff). Libnet includes packet creation at the IP layer and at the link
layer as well as a host of supplementary and complementary functionality.

%package -n	%{develname}
Summary:	Development library and header files for the libnet library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	libnet%{major}-devel = %{version}-%{release}
Provides:	net-devel = %{version}-%{release}
Provides:	net2-devel = %{version}-%{release}
Provides:	%{mklibname net 2 -d} = %{version}-%{release}
Obsoletes:	%{mklibname net 2 -d}
Conflicts:	%{mklibname net 1.0.2 -d}
Conflicts:	%{mklibname net 1.1.0 -d}
# 1.1.3 should be api compatible with 1.1.2*
Provides:	%{mklibname net 1.1.2 -d} = %{version}-%{release}
Obsoletes:	%{mklibname net 1.1.2 -d}

%description -n	%{develname}
The libnet-devel package includes header files and libraries necessary for
developing programs which use the libnet library. Libnet is very handy with
which to write network tools and network test code. See the manpage and sample
test code for more detailed information.

%prep

%setup -q -n libnet-%{version}

# Keep the sample directory untouched by make
rm -rf __dist_sample
mkdir __dist_sample
cp -a sample __dist_sample

%build

%configure2_5x

%make

%install
rm -rf %{buildroot}

%makeinstall_std INSTALL='install -p'

# Don't install any static .a and libtool .la files
rm -f %{buildroot}%{_libdir}/%{name}.{a,la}

# Prepare samples directory and perform some fixes
rm -rf __dist_sample/sample/win32
rm -f __dist_sample/sample/Makefile.{am,in}
sed -e 's@#include "../include/libnet.h"@#include <libnet.h>@' \
  __dist_sample/sample/libnet_test.h > __dist_sample/sample/libnet_test.h.new
touch -c -r __dist_sample/sample/libnet_test.h{,.new}
mv -f __dist_sample/sample/libnet_test.h{.new,}

# Remove makefile relics from documentation
rm -f doc/html/Makefile*

# Correct wrong line endings at CHANGELOG and CONTRIB
for file in CHANGELOG CONTRIB; do
  sed -e 's/\r$//' doc/$file > doc/$file.new
  touch -c -r doc/$file doc/$file.new
  mv -f doc/$file.new doc/$file
done

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc README doc/CHANGELOG doc/COPYING
%attr(0755,root,root) %{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc doc/DESIGN_NOTES doc/MIGRATION doc/PACKET_BUILDING
%doc doc/RAWSOCKET_NON_SEQUITUR doc/TODO doc/html/ __dist_sample/sample/
%{_bindir}/libnet-config
%{_includedir}/libnet.h
%dir %{_includedir}/libnet
%{_includedir}/libnet/*.h
%{_libdir}/*.so
%{_mandir}/man3/*




%changelog
* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1.5-3mdv2011.0
+ Revision: 662386
- mass rebuild

* Mon Mar 14 2011 Thomas Spuhler <tspuhler@mandriva.org> 1.1.5-2
+ Revision: 644468
- updated for rebuild

* Thu Nov 11 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.5-1mdv2011.0
+ Revision: 596291
- 1.1.5
- format string errors got fifed upstrem

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.4-2mdv2010.1
+ Revision: 519024
- rebuild

* Wed Jun 17 2009 Frederik Himpe <fhimpe@mandriva.org> 1.1.4-1mdv2010.0
+ Revision: 386817
- Update to new version 1.1.4
- Drop header inclusion fix patch: integrated upstream

* Thu Jun 04 2009 Oden Eriksson <oeriksson@mandriva.com> 1.1.3-2mdv2010.0
+ Revision: 382684
- fix one bug with a borked include (P1)

* Wed May 27 2009 Oden Eriksson <oeriksson@mandriva.com> 1.1.3-1mdv2010.0
+ Revision: 380255
- import libnet


* Wed May 27 2009 Oden Eriksson <oeriksson@mandriva.com> 1.1.3-1mdv2009.1
- 1.1.3 (new fork) (new major)
- sync with fedora

* Tue Dec 16 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.2.1-8mdv2009.1
+ Revision: 314861
- added P2,P3,P4,P5 from debian
- added P6 to make it build (thanks pixel)

* Wed Aug 06 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.1.2.1-7mdv2009.0
+ Revision: 264848
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu May 29 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.2.1-6mdv2009.0
+ Revision: 213001
- rebuild

* Sun Jan 13 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.1.2.1-5mdv2008.1
+ Revision: 150716
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun Aug 19 2007 Oden Eriksson <oeriksson@mandriva.com> 1.1.2.1-4mdv2008.0
+ Revision: 66940
- fix buildprereq rpmlint upload blocker


* Wed Nov 01 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1.2.1-3mdv2007.0
+ Revision: 74837
- Import libnet1.1.2

* Wed Jul 26 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1.2.1-3mdk
- rebuild

* Fri Mar 17 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1.2.1-2mdk
- fix deps

* Fri Mar 17 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1.2.1-1mdk
- the libnet cleanup campaign

* Thu Oct 06 2005 Oden Eriksson <oeriksson@mandriva.com> 1.1.2.1-4mdk
- added P1 to make dhcp_probe compile
- fix naming

* Wed Jan 19 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.1.2.1-3mdk
- add a virtual provides to make it easier to distinguise this 
  package from other libnet packages
- update descriptions

* Tue Jan 11 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.1.2.1-2mdk
- fix typo in description (kelk1)

* Sat Jun 26 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.1.2.1-1mdk
- 1.1.2.1
- added P0 (PLD)
- use the %%configure2_5x macro
- true libifiction
