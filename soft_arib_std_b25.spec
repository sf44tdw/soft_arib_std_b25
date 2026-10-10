Name:           soft_arib_std_b25
Version:        0.2.5
Release:        1%{?dist}
Summary:        ARIB STD-B25 implementation without B-CAS card
License:        Unspecified
URL:            https://github.com/sf44tdw/soft_arib_std_b25
# git archive --format=tar.gz --prefix=%%{name}-%%{version}/ -o %%{name}-%%{version}.tar.gz HEAD
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libpcsclite)

%global soname_major 0

%description
Japanese TV standard "ARIB STD-B25" implementation without B-CAS card.
This source package builds the bcasid and softarib25 packages.

%package -n bcasid
Summary:        Tool to read B-CAS card information
Requires:       pcsc-lite
Requires:       pcsc-lite-ccid

%description -n bcasid
Provides the bcasid command, which reads information from a B-CAS card
through PC/SC and prints it (the output can be used as bcasid.inf).

%package -n softarib25
Summary:        ARIB STD-B25 descrambler (b25 command and libarib25)

%description -n softarib25
Provides the b25 command, libarib25 and libecmdecoder shared libraries and
the libarib25 development headers.

%prep
%autosetup

%build
%make_build all \
    CFLAGS="%{optflags} -fPIC" \
    CXXFLAGS="%{optflags} -fPIC" \
    LDFLAGS="%{build_ldflags}"

%install
install -d %{buildroot}%{_bindir} %{buildroot}%{_libdir} \
    %{buildroot}%{_includedir}/arib25
install -m755 build/bcasid %{buildroot}%{_bindir}/bcasid
install -m755 build/softarib25/b25 %{buildroot}%{_bindir}/b25
install -m755 build/libecmdecoder.so %{buildroot}%{_libdir}/libecmdecoder.so
install -m755 build/softarib25/libarib25.so \
    %{buildroot}%{_libdir}/libarib25.so.%{version}
ln -s libarib25.so.%{version} %{buildroot}%{_libdir}/libarib25.so.%{soname_major}
ln -s libarib25.so.%{soname_major} %{buildroot}%{_libdir}/libarib25.so
for h in arib_std_b25.h b_cas_card.h multi2.h ts_section_parser.h \
    portable.h ts_common_types.h; do
    install -m644 softarib25/src/$h %{buildroot}%{_includedir}/arib25/$h
done

%post -n softarib25 -p /sbin/ldconfig
%postun -n softarib25 -p /sbin/ldconfig

%files -n bcasid
%doc README
%{_bindir}/bcasid

%files -n softarib25
%doc README
%{_bindir}/b25
%{_libdir}/libecmdecoder.so
%{_libdir}/libarib25.so
%{_libdir}/libarib25.so.%{soname_major}
%{_libdir}/libarib25.so.%{version}
%{_includedir}/arib25/

%changelog
* Sat Oct 10 2026 Packager <packager@example.com> - 0.2.5-1
- Initial RPM packaging
