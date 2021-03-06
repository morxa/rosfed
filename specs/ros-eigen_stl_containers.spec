Name:           ros-eigen_stl_containers
Version:        melodic.0.1.8
Release:        1%{?dist}
Summary:        ROS package eigen_stl_containers

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/eigen_stl_containers-release/archive/release/melodic/eigen_stl_containers/0.1.8-0.tar.gz#/ros-melodic-eigen_stl_containers-0.1.8-source0.tar.gz


BuildArch: noarch

# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel

BuildRequires:  eigen3-devel
BuildRequires:  ros-melodic-catkin-devel
BuildRequires:  ros-melodic-cmake_modules-devel


Provides:  ros-melodic-eigen_stl_containers = 0.1.8-1
Obsoletes: ros-melodic-eigen_stl_containers < 0.1.8-1
Obsoletes: ros-kinetic-eigen_stl_containers < 0.1.8-1


%description
This package provides a set of typedef's that allow using Eigen
datatypes in STL containers

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       ros-melodic-catkin-devel
Requires:       eigen3-devel
Requires:       ros-melodic-cmake_modules-devel

Provides: ros-melodic-eigen_stl_containers-devel = 0.1.8-1
Obsoletes: ros-melodic-eigen_stl_containers-devel < 0.1.8-1
Obsoletes: ros-kinetic-eigen_stl_containers-devel < 0.1.8-1

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.



%prep

%setup -c -T
tar --strip-components=1 -xf %{SOURCE0}

%build
# nothing to do here


%install

PYTHONUNBUFFERED=1 ; export PYTHONUNBUFFERED

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
FFLAGS="${FFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FFLAGS ; \
FCFLAGS="${FCFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FCFLAGS ; \
%{?__global_ldflags:LDFLAGS="${LDFLAGS:-%__global_ldflags}" ; export LDFLAGS ;} \

source %{_libdir}/ros/setup.bash

# substitute shebang before install block because we run the local catkin script
for f in $(grep -rl python .) ; do
  sed -i.orig '/^#!.*python\s*$/ { s/python/python3/ }' $f
  touch -r $f.orig $f
  rm $f.orig
done

DESTDIR=%{buildroot} ; export DESTDIR


catkin_make_isolated \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCATKIN_ENABLE_TESTING=OFF \
  -DPYTHON_VERSION=%{python3_version} \
  -DPYTHON_VERSION_NODOTS=%{python3_version_nodots} \
  --source . \
  --install \
  --install-space %{_libdir}/ros/ \
  --pkg eigen_stl_containers




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,local_setup*,setup*,env.sh}

touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files_devel.list

find . -maxdepth 1 -type f -iname "*readme*" | sed "s:^:%%doc :" >> files.list
find . -maxdepth 1 -type f -iname "*license*" | sed "s:^:%%license :" >> files.list



# replace cmake python macro in shebang
for file in $(grep -rIl '^#!.*@PYTHON_EXECUTABLE@*$' %{buildroot}) ; do
  sed -i.orig 's:^#!\s*@PYTHON_EXECUTABLE@\s*:%{__python3}:' $file
  touch -r $file.orig $file
  rm $file.orig
done

# replace unversioned python shebang
for file in $(grep -rIl '^#!.*python\s*$' %{buildroot}) ; do
  sed -i.orig '/^#!.*python\s*$/ { s/python/python3/ }' $file
  touch -r $file.orig $file
  rm $file.orig
done

# replace "/usr/bin/env $interpreter" with "/usr/bin/$interpreter"
for interpreter in bash sh python2 python3 ; do
  for file in $(grep -rIl "^#\!.*${interpreter}" %{buildroot}) ; do
    sed -i.orig "s:^#\!\s*/usr/bin/env\s\+${interpreter}.*:#!/usr/bin/${interpreter}:" $file
    touch -r $file.orig $file
    rm $file.orig
  done
done


echo "This is a package automatically generated with rosfed." >> README_FEDORA
echo "See https://pagure.io/ros for more information." >> README_FEDORA
install -m 0644 -p -D -t %{buildroot}/%{_docdir}/%{name} README_FEDORA
echo %{_docdir}/%{name} >> files.list
install -m 0644 -p -D -t %{buildroot}/%{_docdir}/%{name}-devel README_FEDORA
echo %{_docdir}/%{name}-devel >> files_devel.list


%files -f files.list
%files devel -f files_devel.list


%changelog
* Wed Jul 24 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.1.8-1
- Update to latest release
* Fri Jul 12 2019 Till Hofmann <thofmann@fedoraproject.org> - 0.1.8-10
- Remove ROS distro from package name
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.1.8-9
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.1.8-8
- devel also requires: the devel package of each run dependency
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.1.8-7
- Also add upstream's exec_depend as Requires:
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.1.8-6
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.1.8-5
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.1.8-4
- Add Recommends: for all BRs to the devel subpackage
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.1.8-3
- Split devel package
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.1.8-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.1.8-1
- Update auto-generated Spec file
