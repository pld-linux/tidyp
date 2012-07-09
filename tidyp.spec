#
# Conditional build:
%bcond_with	tests	# perform "make check" (broken, some file is missing)
#
Summary:	Clean up and pretty-print HTML/XHTML/XML
Summary(pl.UTF-8):	Czyszczenie i ładne wypisywanie HTML-a/XHTML-a/XML-a
Name:		tidyp
Version:	1.04
Release:	1
License:	W3C
Group:		Applications/Text
Source0:	http://github.com/downloads/petdance/tidyp/%{name}-%{version}.tar.gz
# Source0-md5:	00a6b804f6625221391d010ca37178e1
URL:		http://www.tidyp.com/
Requires:	libtidyp = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
tidyp is a fork of tidy on SourceForge. The library name is "tidyp",
and the command-line tool is also "tidyp" but all internal API stays
the same.

%description -l pl.UTF-8
tidyp to odgałęzienie projektu tidy z SourceForge. Nazwa biblioteki to
"tidyp", polecenie także nazywa się "tidyp", ale całe wewnętrzne API
pozostaje takie samo.

%package -n libtidyp
Summary:	Shared library for tidyp
Summary(pl.UTF-8):	Biblioteka współdzielona tidyp
Group:		Libraries

%description -n libtidyp
Shared library for tidyp.

%description -n libtidyp -l pl.UTF-8
Biblioteka współdzielona tidyp.

%package -n libtidyp-devel
Summary:	Development files for libtidyp
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libtidyp
Group:		Development/Libraries
Requires:	libtidyp = %{version}-%{release}

%description -n libtidyp-devel
Development files for libtidyp.

%description -n libtidyp-devel -l pl.UTF-8
Pliki programistyczne biblioteki libtidyp.

%package -n libtidyp-static
Summary:	Static libtidyp library
Summary(pl.UTF-8):	Statyczna biblioteka libtidyp
Group:		Development/Libraries
Requires:	libtidyp = %{version}-%{release}

%description -n libtidyp-static
Static libtidyp library.

%description -n libtidyp-static -l pl.UTF-8
Statyczna biblioteka libtidyp.

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
	--disable-dependency-tracking
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with tests}
%{__make} check
%endif

# no external dependencies
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libtidyp.la

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
%attr(755,root,root) %{_libdir}/libtidyp.so
%{_includedir}/tidyp

%files -n libtidyp-static
%defattr(644,root,root,755)
%{_libdir}/libtidyp.a
