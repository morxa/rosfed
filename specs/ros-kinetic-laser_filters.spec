Name:           ros-kinetic-laser_filters
Version:        1.8.5
Release:        8%{?dist}
Summary:        ROS package laser_filters

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/laser_filters-release/archive/release/kinetic/laser_filters/1.8.5-0.tar.gz#/ros-kinetic-laser_filters-1.8.5-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  eigen3-devel
BuildRequires:  poco-devel
BuildRequires:  tinyxml-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  ros-kinetic-angles-devel
BuildRequires:  ros-kinetic-catkin-devel
BuildRequires:  ros-kinetic-filters-devel
BuildRequires:  ros-kinetic-laser_geometry-devel
BuildRequires:  ros-kinetic-message_filters-devel
BuildRequires:  ros-kinetic-pluginlib-devel
BuildRequires:  ros-kinetic-roscpp-devel
BuildRequires:  ros-kinetic-rostest-devel
BuildRequires:  ros-kinetic-sensor_msgs-devel
BuildRequires:  ros-kinetic-tf-devel

Requires:       ros-kinetic-angles
Requires:       ros-kinetic-filters
Requires:       ros-kinetic-laser_geometry
Requires:       ros-kinetic-message_filters
Requires:       ros-kinetic-pluginlib
Requires:       ros-kinetic-roscpp
Requires:       ros-kinetic-sensor_msgs
Requires:       ros-kinetic-tf


%description
Assorted filters designed to operate on 2D planar laser scanners,
which use the sensor_msgs/LaserScan type.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-kinetic-catkin-devel
Requires:       eigen3-devel
Requires:       poco-devel
Requires:       tinyxml-devel
Requires:       tinyxml2-devel
Requires:       ros-kinetic-angles-devel
Requires:       ros-kinetic-filters-devel
Requires:       ros-kinetic-laser_geometry-devel
Requires:       ros-kinetic-message_filters-devel
Requires:       ros-kinetic-pluginlib-devel
Requires:       ros-kinetic-roscpp-devel
Requires:       ros-kinetic-rostest-devel
Requires:       ros-kinetic-sensor_msgs-devel
Requires:       ros-kinetic-tf-devel

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

DESTDIR=%{buildroot} ; export DESTDIR


catkin_make_isolated \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCATKIN_ENABLE_TESTING=OFF \
  --source . \
  --install \
  --install-space %{_libdir}/ros/ \
  --pkg laser_filters




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



# replace unversioned python shebang
for file in $(grep -rIl '^#!.*python\s*$') ; do
  sed -i.orig '/^#!.*python\s*$/ { s/python/python2/ }' $file
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
install -p -D -t %{buildroot}/%{_docdir}/%{name} README_FEDORA
echo %{_docdir}/%{name} >> files.list
install -p -D -t %{buildroot}/%{_docdir}/%{name}-devel README_FEDORA
echo %{_docdir}/%{name}-devel >> files_devel.list


%files -f files.list
%files devel -f files_devel.list


%changelog
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.8.5-8
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.8.5-7
- devel also requires: the devel package of each run dependency
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.8.5-6
- Also add upstream's exec_depend as Requires:
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.8.5-5
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.8.5-4
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.8.5-3
- Add Recommends: for all BRs to the devel subpackage
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.8.5-2
- Split devel package
* Sun Nov 19 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.8.5-1
- Update to latest release
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.8.3-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.8.3-1
- Update auto-generated Spec file
