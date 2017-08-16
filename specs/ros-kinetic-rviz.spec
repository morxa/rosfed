Name:           ros-kinetic-rviz
Version:        1.12.11
Release:        1%{?dist}
Summary:        ROS package rviz

License:        BSD
URL:            http://ros.org/wiki/rviz

Source0:        https://github.com/ros-gbp/rviz-release/archive/release/kinetic/rviz/1.12.11-0.tar.gz#/ros-kinetic-rviz-1.12.11-source0.tar.gz



BuildRequires:  assimp-devel
BuildRequires:  eigen3-devel
BuildRequires:  mesa-libGL-devel mesa-libGLU-devel
BuildRequires:  ogre-devel
BuildRequires:  python-qt5-devel
BuildRequires:  qt5-qtbase
BuildRequires:  qt5-qtbase-devel
BuildRequires:  sip-devel
BuildRequires:  tinyxml-devel
BuildRequires:  urdfdom-headers-devel
BuildRequires:  yaml-cpp-devel
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-cmake_modules
BuildRequires:  ros-kinetic-geometry_msgs
BuildRequires:  ros-kinetic-image_transport
BuildRequires:  ros-kinetic-interactive_markers
BuildRequires:  ros-kinetic-laser_geometry
BuildRequires:  ros-kinetic-map_msgs
BuildRequires:  ros-kinetic-message_filters
BuildRequires:  ros-kinetic-nav_msgs
BuildRequires:  ros-kinetic-pluginlib
BuildRequires:  ros-kinetic-python_qt_binding
BuildRequires:  ros-kinetic-resource_retriever
BuildRequires:  ros-kinetic-rosbag
BuildRequires:  ros-kinetic-rosconsole
BuildRequires:  ros-kinetic-roscpp
BuildRequires:  ros-kinetic-roslib
BuildRequires:  ros-kinetic-rospy
BuildRequires:  ros-kinetic-sensor_msgs
BuildRequires:  ros-kinetic-std_msgs
BuildRequires:  ros-kinetic-std_srvs
BuildRequires:  ros-kinetic-tf
BuildRequires:  ros-kinetic-urdf
BuildRequires:  ros-kinetic-visualization_msgs

Requires:       assimp
Requires:       eigen3-devel
Requires:       mesa-libGL-devel mesa-libGLU-devel
Requires:       ogre-devel
Requires:       qt5-qtbase
Requires:       qt5-qtbase-gui
Requires:       tinyxml-devel
Requires:       urdfdom-headers-devel
Requires:       yaml-cpp-devel
Requires:       ros-kinetic-geometry_msgs
Requires:       ros-kinetic-image_transport
Requires:       ros-kinetic-interactive_markers
Requires:       ros-kinetic-laser_geometry
Requires:       ros-kinetic-map_msgs
Requires:       ros-kinetic-media_export
Requires:       ros-kinetic-message_filters
Requires:       ros-kinetic-nav_msgs
Requires:       ros-kinetic-pluginlib
Requires:       ros-kinetic-python_qt_binding
Requires:       ros-kinetic-resource_retriever
Requires:       ros-kinetic-rosbag
Requires:       ros-kinetic-rosconsole
Requires:       ros-kinetic-roscpp
Requires:       ros-kinetic-roslib
Requires:       ros-kinetic-rospy
Requires:       ros-kinetic-sensor_msgs
Requires:       ros-kinetic-std_msgs
Requires:       ros-kinetic-std_srvs
Requires:       ros-kinetic-tf
Requires:       ros-kinetic-urdf
Requires:       ros-kinetic-visualization_msgs

%description
3D visualization tool for ROS.


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

PATH="$PATH:%{_qt5_bindir}" ; export PATH

source %{_libdir}/ros/setup.bash

DESTDIR=%{buildroot} ; export DESTDIR

catkin_make_isolated \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  --source . \
  --install \
  --install-space %{_libdir}/ros/ \
  --pkg rviz

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
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.12.11-1
- Update auto-generated Spec file
