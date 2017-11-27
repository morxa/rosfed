Name:           ros-kinetic-depth_image_proc
Version:        1.12.21
Release:        2%{?dist}
Summary:        ROS package depth_image_proc

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/image_pipeline-release/archive/release/kinetic/depth_image_proc/1.12.21-0.tar.gz#/ros-kinetic-depth_image_proc-1.12.21-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  boost-devel
BuildRequires:  eigen3-devel
BuildRequires:  libuuid-devel
BuildRequires:  opencv-devel
BuildRequires:  poco-devel
BuildRequires:  tinyxml-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-cmake_modules
BuildRequires:  ros-kinetic-cv_bridge
BuildRequires:  ros-kinetic-eigen_conversions
BuildRequires:  ros-kinetic-image_geometry
BuildRequires:  ros-kinetic-image_transport
BuildRequires:  ros-kinetic-message_filters
BuildRequires:  ros-kinetic-nodelet
BuildRequires:  ros-kinetic-rostest
BuildRequires:  ros-kinetic-sensor_msgs
BuildRequires:  ros-kinetic-stereo_msgs
BuildRequires:  ros-kinetic-tf2
BuildRequires:  ros-kinetic-tf2_ros

Requires:       ros-kinetic-cv_bridge
Requires:       ros-kinetic-eigen_conversions
Requires:       ros-kinetic-image_geometry
Requires:       ros-kinetic-image_transport
Requires:       ros-kinetic-nodelet
Requires:       ros-kinetic-tf2
Requires:       ros-kinetic-tf2_ros

%description
Contains nodelets for processing depth images such as those produced
by OpenNI camera. Functions include creating disparity images and
point clouds, as well as registering (reprojecting) a depth image into
another camera frame.


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
  --pkg depth_image_proc

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
* Thu Nov 23 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.12.21-2
- Build against system opencv3 instead of ros-kinetic-opencv
* Sun Nov 19 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.12.21-1
- Update to latest release
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.12.20-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.12.20-1
- Update auto-generated Spec file
