Name:           ros-kinetic-camera_calibration_parsers
Version:        1.11.13
Release:        1%{?dist}
Summary:        ROS package camera_calibration_parsers

License:        BSD
URL:            http://ros.org/wiki/camera_calibration_parsers

Source0:        https://github.com/ros-gbp/image_common-release/archive/release/kinetic/camera_calibration_parsers/1.11.13-0.tar.gz#/ros-kinetic-camera_calibration_parsers-1.11.13-source0.tar.gz



BuildRequires:  boost-devel
BuildRequires:  pkgconfig
BuildRequires:  python2-devel
BuildRequires:  yaml-cpp-devel
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-rosbash
BuildRequires:  ros-kinetic-rosconsole
BuildRequires:  ros-kinetic-roscpp
BuildRequires:  ros-kinetic-roscpp_serialization
BuildRequires:  ros-kinetic-rosunit
BuildRequires:  ros-kinetic-sensor_msgs

Requires:       ros-kinetic-roscpp
Requires:       ros-kinetic-roscpp_serialization
Requires:       ros-kinetic-sensor_msgs

%description
camera_calibration_parsers contains routines for reading and writing
camera calibration parameters.


%prep

%setup -c -T
tar --strip-components=1 -xf %{SOURCE0}

%build
# nothing to do here


%install
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
FFLAGS="${FFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FFLAGS ; \
FCFLAGS="${FCFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FCFLAGS ; \
%{?__global_ldflags:LDFLAGS="${LDFLAGS:-%__global_ldflags}" ; export LDFLAGS ;} \


source %{_libdir}/ros/setup.bash

DESTDIR=%{buildroot} ; export DESTDIR

catkin_make_isolated \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  --source . \
  --install \
  --install-space %{_libdir}/ros/ \
  --pkg camera_calibration_parsers

rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,setup*,env.sh}

find %{buildroot}/%{_libdir}/ros/{bin,etc,include,lib/pkgconfig,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list


find . -maxdepth 1 -type f -iname "*readme*" | sed "s:^:%%doc :" >> files.list
find . -maxdepth 1 -type f -iname "*license*" | sed "s:^:%%license :" >> files.list

%files -f files.list



%changelog
* Sun Nov 19 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.11.13-1
- Update to latest release
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.11.12-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.11.12-1
- Update auto-generated Spec file
