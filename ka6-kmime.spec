#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	24.12.0
%define		qtver		5.15.2
%define		kaname		kmime
Summary:	KMime
Name:		ka6-%{kaname}
Version:	24.12.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	ab189db00bbf3a5b641a8731afb05639
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= 5.9.0
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= 5.53.0
BuildRequires:	kf6-kcodecs-devel >= 5.51.0
BuildRequires:	kf6-ki18n-devel
BuildRequires:	kf6-ki18n-devel >= 5.51.0
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KMime is a library for handling mail messages and newsgroup articles.
Both mail messages and newsgroup articles are based on the same
standard called MIME, which stands for
- **Multipurpose Internet Mail Extensions**. In this document, the
  term `message` is used to refer to both mail messages and newsgroup
  articles.

%description -l pl.UTF-8
KMime jest biblioteką do obsługi wiadomości pocztowych i artykułów
grup Usenetowych. Zarówno wiadomości pocztowe i artykuły są oparte na
tym samym standardzie zwanym MIME
- **Multipurpose Internet Mail Extensions**, (**Uniweralne
  roszszerzenie poczty internetowej**). W tym dokumencie, termin
  `wiadomość` oznacza zarówno wiadomości pocztowe, jak i artykuły grup
  news.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libKPim6Mime.so.*.*
%ghost %{_libdir}/libKPim6Mime.so.6
%{_datadir}/qlogging-categories6/kmime.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KPim6/KMime
%{_libdir}/cmake/KPim6Mime
%{_libdir}/libKPim6Mime.so
