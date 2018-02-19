Name:           ros-kinetic-laser_geometry
Version:        1.6.4
Release:        3%{?dist}
Summary:        ROS package laser_geometry

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/laser_geometry-release/archive/release/kinetic/laser_geometry/1.6.4-0.tar.gz#/ros-kinetic-laser_geometry-1.6.4-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  boost-devel
BuildRequires:  eigen3-devel
BuildRequires:  ros-kinetic-angles-devel
BuildRequires:  ros-kinetic-catkin-devel
BuildRequires:  ros-kinetic-cmake_modules-devel
BuildRequires:  ros-kinetic-roscpp-devel
BuildRequires:  ros-kinetic-rosunit-devel
BuildRequires:  ros-kinetic-sensor_msgs-devel
BuildRequires:  ros-kinetic-tf-devel

Requires:       numpy
Requires:       ros-kinetic-angles
Requires:       ros-kinetic-roscpp
Requires:       ros-kinetic-sensor_msgs
Requires:       ros-kinetic-tf


%description
This package contains a class for converting from a 2D laser scan as
defined by sensor_msgs/LaserScan into a point cloud as defined by
sensor_msgs/PointCloud or sensor_msgs/PointCloud2. In particular, it
contains functionality to account for the skew resulting from moving
robots or tilting laser scanners.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-kinetic-catkin

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
  --pkg laser_geometry




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,setup*,env.sh}

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


echo "This is a package automatically generated with rosfed." >> README_FEDORA
echo "See https://pagure.io/ros for more information." >> README_FEDORA
install -p -D -t %{buildroot}/%{_docdir}/%{name} README_FEDORA
echo %{_docdir}/%{name} >> files.list
install -p -D -t %{buildroot}/%{_docdir}/%{name}-devel README_FEDORA
echo %{_docdir}/%{name}-devel >> files_devel.list


%files -f files.list
%files devel -f files_devel.list


%changelog
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.6.4-3
- Split devel package
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.6.4-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.6.4-1
- Update auto-generated Spec file
