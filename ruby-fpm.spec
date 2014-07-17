#
# Conditional build:
%bcond_with	tests		# build without tests

%define	pkgname	fpm
Summary:	fpm - package building and mangling
Name:		ruby-%{pkgname}
Version:	1.0.2
Release:	2
License:	GPL v2+ or Ruby
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	d962faaf4e728bea52f3b7d0de3db29e
URL:		https://github.com/jordansissel/fpm
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildRequires:	sed >= 4.0
%if %{with tests}
BuildRequires:	ruby-insist < 0.1
BuildRequires:	ruby-insist >= 0.0.5
BuildRequires:	ruby-minitest
BuildRequires:	ruby-pry
BuildRequires:	ruby-rspec
BuildRequires:	ruby-stud
%endif
Requires:	ruby-arr-pm < 0.1
Requires:	ruby-arr-pm >= 0.0.8
Requires:	ruby-backports >= 2.6.2
Requires:	ruby-cabin >= 0.6.0
Requires:	ruby-childprocess
Requires:	ruby-clamp < 1
Requires:	ruby-clamp >= 0.6
Requires:	ruby-ffi
Requires:	ruby-ftw < 0.1
Requires:	ruby-ftw >= 0.0.30
Requires:	ruby-json >= 1.7.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Convert directories, rpms, python eggs, rubygems, and more to rpms,
debs, solaris packages and more. Win at package management without
wasting pointless hours debugging bad rpm specs!

%prep
%setup -q -n %{pkgname}-%{version}
%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*

%build
%__gem_helper spec

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir},%{_bindir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/fpm
%{ruby_vendorlibdir}/%{pkgname}.rb
%{ruby_vendorlibdir}/%{pkgname}
%{ruby_specdir}/%{pkgname}-%{version}.gemspec
