%define	major 1
%define libname %mklibname net %{major}
%define develname %mklibname net -d

Summary:	A C library for portable packet creation
Name:		libnet
Version:	1.1.4
Release:	%mkrel 1
License:	BSD
Group:		System/Libraries
URL:		http://www.sourceforge.net/projects/libnet-dev/
Source0:	http://downloads.sourceforge.net/libnet-dev/%{name}-%{version}.tar.gz
Patch0:		libnet-1.1.2.1-format_not_a_string_literal_and_no_format_arguments.diff
BuildRequires:	libpcap-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%patch0 -p0 -b .format_not_a_string_literal_and_no_format_arguments

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
%doc doc/BUGS doc/DESIGN_NOTES doc/MIGRATION doc/PACKET_BUILDING
%doc doc/RAWSOCKET_NON_SEQUITUR doc/TODO doc/html/ __dist_sample/sample/
%{_bindir}/libnet-config
%{_includedir}/libnet.h
%dir %{_includedir}/libnet
%{_includedir}/libnet/*.h
%{_libdir}/*.so
%{_mandir}/man3/*


