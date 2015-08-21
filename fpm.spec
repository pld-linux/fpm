#
# Conditional build:
%bcond_with	tests		# build without tests

Summary:	fpm - package building and mangling
Name:		fpm
Version:	1.4.0
Release:	1
License:	MIT-like
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{name}-%{version}.gem
# Source0-md5:	4d82b0484db150928330b04bb44c92a2
Patch0:		templates.patch
Patch1:		tmppath.patch
URL:		https://github.com/jordansissel/fpm
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildRequires:	sed >= 4.0
%if %{with tests}
BuildRequires:	ruby-insist < 0.1
BuildRequires:	ruby-insist >= 0.0.5
BuildRequires:	ruby-pry
BuildRequires:	ruby-rspec < 3.1
BuildRequires:	ruby-rspec >= 3.0.0
BuildRequires:	ruby-stud
%endif
Requires:	ruby-arr-pm < 0.1
Requires:	ruby-arr-pm >= 0.0.10
Requires:	ruby-backports >= 2.6.2
Requires:	ruby-cabin >= 0.6.0
Requires:	ruby-childprocess
Requires:	ruby-clamp < 1
Requires:	ruby-clamp >= 0.6
Requires:	ruby-ffi
Requires:	ruby-json >= 1.7.7
Suggests:	rpm-build
Obsoletes:	ruby-fpm <= 1.4.0-2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Convert directories, rpms, python eggs, rubygems, and more to rpms,
debs, solaris packages and more. Win at package management without
wasting pointless hours debugging bad rpm specs!

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
# write .gemspec
%__gem_helper spec

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir},%{_bindir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a templates $RPM_BUILD_ROOT%{ruby_vendorlibdir}/%{name}
cp -p %{name}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/fpm
%{ruby_vendorlibdir}/%{name}.rb
%{ruby_vendorlibdir}/%{name}
%{ruby_specdir}/%{name}-%{version}.gemspec
