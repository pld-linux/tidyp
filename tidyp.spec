Summary:	Clean up and pretty-print HTML/XHTML/XML
Name:		tidyp
Version:	1.04
Release:	1
License:	W3C
Group:		Applications/Text
URL:		http://www.tidyp.com/
Source0:	http://github.com/downloads/petdance/tidyp/%{name}-%{version}.tar.gz
# Source0-md5:	00a6b804f6625221391d010ca37178e1
Requires:	libtidyp = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
tidyp is a fork of tidy on SourceForge. The library name is "tidyp",
and the command-line tool is also "tidyp" but all internal API stays
the same.

%package -n libtidyp
Summary:	Shared libraries for tidyp
Group:		Libraries

%description -n libtidyp
Shared libraries for tidyp.

%package -n libtidyp-devel
Summary:	Development files for libtidyp
Group:		Development/Libraries
Requires:	libtidyp = %{version}-%{release}

%description -n libtidyp-devel
Development files for libtidyp.

%prep
%setup -q

# Fix permissions for debuginfo
chmod -x src/{mappedio.*,version.h}

# Fix timestamp order to avoid trying to re-run autotools
touch aclocal.m4
find . -name Makefile.in -exec touch {} \;
touch configure

%build
%configure \
	--disable-static \
	--disable-dependency-tracking
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with tests}
%{__make} check
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libtidyp -p /sbin/ldconfig
%postun	-n libtidyp -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_bindir}/tidyp

%files -n libtidyp
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtidyp-%{version}.so.*.*.*
%ghost %{_libdir}/libtidyp-%{version}.so.0

%files -n libtidyp-devel
%defattr(644,root,root,755)
%{_includedir}/tidyp
%{_libdir}/libtidyp.so
%exclude %{_libdir}/libtidyp.la
