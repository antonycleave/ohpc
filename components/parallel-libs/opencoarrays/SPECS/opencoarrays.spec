#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

# OpenCoarrays library that is is dependent on compiler toolchain and MPI
%define ohpc_compiler_dependent 1
%define ohpc_mpi_dependent 1
%include %{_sourcedir}/OHPC_macros


# Base package name
%define pname opencoarrays

Name:           %{pname}-%{compiler_family}-%{mpi_family}%{PROJ_DELIM}
Summary:        ABI to leverage the parallel programming features of the Fortran 2018 DIS
License:        BSD-3-clause
Group:          %{PROJ_NAME}/parallel-libs
Version:        2.2.0
Release:        1%{?dist}
Source0:        https://github.com/sourceryinstitute/OpenCoarrays/releases/download/%{version}/OpenCoarrays-%{version}.tar.gz
Url:            http://www.opencoarrays.org
Requires:       lmod%{PROJ_DELIM} >= 7.6.1
BuildRequires:  cmake%{PROJ_DELIM}

#!BuildIgnore: post-build-checks

# Default library install path
%define install_path %{OHPC_LIBS}/%{compiler_family}/%{mpi_family}/%{pname}/%version

%description
OpenCoarrays is an open-source software project that supports the coarray 
Fortran (CAF) parallel programming features of the Fortran 2008 standard and 
several features proposed for Fortran 2015 in the draft Technical Specification 
TS 18508 Additional Parallel Features in Fortran.


%prep
%setup -q -n OpenCoarrays-%{version}


%build
# OpenHPC compiler/mpi designation
%ohpc_setup_compiler

module load cmake

%{__mkdir_p} build-opencoarrays
cd build-opencoarrays
cmake -DCMAKE_INSTALL_PREFIX=%{install_path} ..

make %{?_smp_mflags}


%install
# OpenHPC compiler/mpi designation
%ohpc_setup_compiler

cd build-opencoarrays
make DESTDIR=$RPM_BUILD_ROOT install

# OpenHPC module file
%{__mkdir} -p %{buildroot}%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the %{PNAME} library built with the %{compiler_family} compiler"
puts stderr "toolchain and the %{mpi_family} MPI stack."
puts stderr " "

puts stderr "\nVersion %{version}\n"

}
module-whatis "Name: %{pname} built with %{compiler_family} compiler and %{mpi_family} MPI"
module-whatis "Version: %{version}"
module-whatis "Category: runtime library"
module-whatis "Description: %{summary}"
module-whatis "%{url}"

set     version                     %{version}

prepend-path    PATH                %{install_path}/bin
prepend-path    INCLUDE             %{install_path}/include
prepend-path    LD_LIBRARY_PATH     %{install_path}/lib

setenv          %{PNAME}_DIR        %{install_path}
setenv          %{PNAME}_BIN        %{install_path}/bin
setenv          %{PNAME}_INC        %{install_path}/include
setenv          %{PNAME}_LIB        %{install_path}/lib

EOF

%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}/.version.%{version}
#%Module1.0#####################################################################
##
## version file for %{pname}-%{version}
##
set     ModulesVersion      "%{version}"
EOF

%{__mkdir} -p $RPM_BUILD_ROOT/%{_docdir}

%files
%{OHPC_PUB}
%doc LICENSE README.md INSTALL 