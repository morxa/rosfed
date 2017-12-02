Name:           ros-kinetic-costmap_2d
Version:        1.14.2
Release:        2%{?dist}
Summary:        ROS package costmap_2d

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/navigation-release/archive/release/kinetic/costmap_2d/1.14.2-0.tar.gz#/ros-kinetic-costmap_2d-1.14.2-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  eigen3-devel
BuildRequires:  libuuid-devel
BuildRequires:  lz4-devel
BuildRequires:  pcl-devel
BuildRequires:  poco-devel
BuildRequires:  tinyxml-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-cmake_modules
BuildRequires:  ros-kinetic-dynamic_reconfigure
BuildRequires:  ros-kinetic-geometry_msgs
BuildRequires:  ros-kinetic-laser_geometry
BuildRequires:  ros-kinetic-map_msgs
BuildRequires:  ros-kinetic-map_server
BuildRequires:  ros-kinetic-message_filters
BuildRequires:  ros-kinetic-message_generation
BuildRequires:  ros-kinetic-nav_msgs
BuildRequires:  ros-kinetic-pcl_conversions
BuildRequires:  ros-kinetic-pcl_ros
BuildRequires:  ros-kinetic-pluginlib
BuildRequires:  ros-kinetic-rosbag
BuildRequires:  ros-kinetic-roscpp
BuildRequires:  ros-kinetic-rostest
BuildRequires:  ros-kinetic-rosunit
BuildRequires:  ros-kinetic-sensor_msgs
BuildRequires:  ros-kinetic-std_msgs
BuildRequires:  ros-kinetic-tf
BuildRequires:  ros-kinetic-visualization_msgs
BuildRequires:  ros-kinetic-voxel_grid

Requires:       ros-kinetic-dynamic_reconfigure
Requires:       ros-kinetic-geometry_msgs
Requires:       ros-kinetic-laser_geometry
Requires:       ros-kinetic-map_msgs
Requires:       ros-kinetic-message_filters
Requires:       ros-kinetic-message_runtime
Requires:       ros-kinetic-nav_msgs
Requires:       ros-kinetic-pcl_conversions
Requires:       ros-kinetic-pcl_ros
Requires:       ros-kinetic-pluginlib
Requires:       ros-kinetic-rosconsole
Requires:       ros-kinetic-roscpp
Requires:       ros-kinetic-sensor_msgs
Requires:       ros-kinetic-std_msgs
Requires:       ros-kinetic-tf
Requires:       ros-kinetic-visualization_msgs
Requires:       ros-kinetic-voxel_grid

%description
This package provides an implementation of a 2D costmap that takes in
sensor data from the world, builds a 2D or 3D occupancy grid of the
data (depending on whether a voxel based implementation is used), and
inflates costs in a 2D costmap based on the occupancy grid and a user
specified inflation radius. This package also provides support for
map_server based initialization of a costmap, rolling window based
costmaps, and parameter based subscription to and configuration of
sensor topics.


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
  --pkg costmap_2d

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
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.14.2-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.14.2-1
- Update auto-generated Spec file
