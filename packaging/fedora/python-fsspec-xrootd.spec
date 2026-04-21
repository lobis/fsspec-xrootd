%global pypi_name fsspec_xrootd

# Fedora names the source RPM and the installable binary RPM separately.
# For this library, users only install python3-fsspec-xrootd.
Name:           python-fsspec-xrootd
Version:        0.5.3
Release:        %autorelease
Summary:        XRootD implementation for fsspec

License:        BSD-3-Clause
URL:            https://github.com/scikit-hep/fsspec-xrootd
Source0:        %{pypi_source %{pypi_name}}

BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3dist(xrootd)
BuildRequires:  xrootd

%description
fsspec-xrootd provides an XRootD implementation for fsspec.


%package -n python3-fsspec-xrootd
Summary:        %{summary}
Requires:       python3dist(xrootd)

%description -n python3-fsspec-xrootd
fsspec-xrootd provides the root:// protocol implementation for fsspec using
the XRootD Python bindings.


%generate_buildrequires
%pyproject_buildrequires -x test


%prep
%autosetup -n %{pypi_name}-%{version}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files fsspec_xrootd


%check
# The full upstream suite exercises a local XRootD daemon and other
# environment-sensitive paths. Keep the RPM build on deterministic tests.
%pytest \
    tests/test_package.py \
    tests/test_basicio.py \
    -k 'invalid_server or invalid_parameters or async_impl or path_parsing'


%files -n python3-fsspec-xrootd -f %{pyproject_files}
%license LICENSE
%doc README.md
%{python3_sitelib}/fsspec_xrootd/*.pyi
%{python3_sitelib}/fsspec_xrootd/py.typed


%changelog
