Name:           ros-kinetic-image_geometry
Version:        1.12.7
Release:        2%{?dist}
Summary:        ROS package image_geometry

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/vision_opencv-release/archive/release/kinetic/image_geometry/1.12.7-0.tar.gz#/ros-kinetic-image_geometry-1.12.7-source0.tar.gz

Patch0: ros-kinetic-image_geometry.catkin-fix-order.patch


# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  boost-devel
BuildRequires:  gtest-devel
BuildRequires:  opencv-devel
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-sensor_msgs

Requires:       ros-kinetic-sensor_msgs

%description
`image_geometry` contains C++ and Python libraries for interpreting
images geometrically. It interfaces the calibration parameters in
sensor_msgs/CameraInfo messages with OpenCV functions such as image
rectification, much as cv_bridge interfaces ROS sensor_msgs/Image with
OpenCV data types.


%prep

%setup -c -T
tar --strip-components=1 -xf %{SOURCE0}
%patch0 -p1

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
  --pkg image_geometry

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
* Thu Nov 23 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.12.7-2
- Build against system opencv3 instead of ros-kinetic-opencv
* Sun Nov 19 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.12.7-1
- Update to latest release
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.12.4-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.12.4-1
- Update auto-generated Spec file
