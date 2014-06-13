%define	major	1
%define libname	%mklibname net %{major}
%define devname	%mklibname net -d

Summary:	A C library for portable packet creation
Name:		libnet
Version:	1.1.6
Release:	8
License:	BSD
Group:		System/Libraries
Url:		http://www.sourceforge.net/projects/libnet-dev/
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

%package -n	%{devname}
Summary:	Development library and header files for the libnet library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
The libnet-devel package includes header files and libraries necessary for
developing programs which use the libnet library. Libnet is very handy with
which to write network tools and network test code. See the manpage and sample
test code for more detailed information.

%prep
%setup -q
# Keep the sample directory untouched by make
rm -rf __dist_sample
mkdir __dist_sample
cp -a sample __dist_sample
#fix build with new automake
sed -i -e 's,AM_CONFIG_HEADER,AC_CONFIG_HEADERS,g' configure.*
libtoolize --copy --force
autoreconf -fi

%build
%configure2_5x \
	--disable-static

%make

%install
%makeinstall_std INSTALL='install -p'

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

%files -n %{libname}
%{_libdir}/libnet.so.%{major}*

%files -n %{devname}
%doc README doc/CHANGELOG doc/COPYING
%doc doc/DESIGN_NOTES doc/MIGRATION doc/PACKET_BUILDING
%doc doc/RAWSOCKET_NON_SEQUITUR doc/TODO doc/html/ __dist_sample/sample/
%{_bindir}/libnet-config
%{_includedir}/libnet.h
%dir %{_includedir}/libnet
%{_includedir}/libnet/*.h
%{_libdir}/*.so
%{_mandir}/man3/*

