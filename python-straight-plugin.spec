#
# Conditional build:
%bcond_with	tests	# do not perform "make test"
%bcond_without	python3 # CPython 3.x module

%define	subver	-post-1
Summary:	Python plugin loader
Name:		python-straight-plugin
Version:	1.4.0
Release:	1
License:	BSD
Group:		Libraries/Python
Source0:	http://pypi.python.org/packages/source/s/straight.plugin/straight.plugin-%{version}%{subver}.tar.gz
# Source0-md5:	e1a22847055f377fa4c9a99d733eb44c
URL:		https://github.com/ironfroggy/straight.plugin/
BuildRequires:	rpmbuild(macros) >= 1.710
BuildRequires:	python-2to3
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
straight.plugin is a Python plugin loader inspired by twisted.plugin
with two important distinctions:

- Fewer dependencies
- Python 3 compatible

The system is used to allow multiple Python packages to provide
plugins within a namespace package, where other packages will locate
and utilize. The plugins themselves are modules in a namespace package
where the namespace identifies the plugins in it for some particular
purpose or intent.

%package -n python3-straight-plugin
Summary:	Python plugin loader
Group:		Libraries/Python

%description -n python3-straight-plugin
straight.plugin is a Python plugin loader inspired by twisted.plugin
with two important distinctions:

- Fewer dependencies
- Python 3 compatible

The system is used to allow multiple Python packages to provide
plugins within a namespace package, where other packages will locate
and utilize. The plugins themselves are modules in a namespace package
where the namespace identifies the plugins in it for some particular
purpose or intent.

%prep
%setup -q -c
mv straight.plugin-%{version}%{subver} py2

%if %{with python3}
cp -a py2 py3
2to3 --write --nobackups py3
%endif

%build
cd py2
%py_build
cd -

%if %{with python3}
cd py3
%py3_build
cd -
%endif

%install
rm -rf $RPM_BUILD_ROOT
cd py2
%py_install
cd -
%py_postclean

%if %{with python3}
cd py3
%py3_install
cd -
%endif

%if %{with tests}
cd py2
%{__python} tests.py
cd -

%if %{with python3}
cd py3
%{__python3} tests.py
cd -
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/straight
%{py_sitescriptdir}/straight.plugin-*-py*.egg-info
%{py_sitescriptdir}/straight.plugin-*-py*-nspkg.pth

%if %{with python3}
%files -n python3-straight-plugin
%defattr(644,root,root,755)
%{py3_sitescriptdir}/straight
%{py3_sitescriptdir}/straight.plugin-*-py*.egg-info
%{py3_sitescriptdir}/straight.plugin-*-py*-nspkg.pth
%endif
