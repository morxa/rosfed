Name:           ros-kinetic-base_local_planner
Version:        1.14.2
Release:        2%{?dist}
Summary:        ROS package base_local_planner

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/navigation-release/archive/release/kinetic/base_local_planner/1.14.2-0.tar.gz#/ros-kinetic-base_local_planner-1.14.2-source0.tar.gz



BuildRequires:  eigen3-devel
BuildRequires:  ros-kinetic-angles
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-cmake_modules
BuildRequires:  ros-kinetic-costmap_2d
BuildRequires:  ros-kinetic-dynamic_reconfigure
BuildRequires:  ros-kinetic-geometry_msgs
BuildRequires:  ros-kinetic-message_generation
BuildRequires:  ros-kinetic-nav_core
BuildRequires:  ros-kinetic-nav_msgs
BuildRequires:  ros-kinetic-pcl_conversions
BuildRequires:  ros-kinetic-pcl_ros
BuildRequires:  ros-kinetic-pluginlib
BuildRequires:  ros-kinetic-roscpp
BuildRequires:  ros-kinetic-rospy
BuildRequires:  ros-kinetic-rosunit
BuildRequires:  ros-kinetic-std_msgs
BuildRequires:  ros-kinetic-tf
BuildRequires:  ros-kinetic-voxel_grid

Requires:       ros-kinetic-angles
Requires:       ros-kinetic-costmap_2d
Requires:       ros-kinetic-dynamic_reconfigure
Requires:       ros-kinetic-geometry_msgs
Requires:       ros-kinetic-message_runtime
Requires:       ros-kinetic-nav_core
Requires:       ros-kinetic-nav_msgs
Requires:       ros-kinetic-pcl_ros
Requires:       ros-kinetic-pluginlib
Requires:       ros-kinetic-roscpp
Requires:       ros-kinetic-rospy
Requires:       ros-kinetic-std_msgs
Requires:       ros-kinetic-tf
Requires:       ros-kinetic-voxel_grid

%description
This package provides implementations of the Trajectory Rollout and
Dynamic Window approaches to local robot navigation on a plane. Given
a plan to follow and a costmap, the controller produces velocity
commands to send to a mobile base. This package supports both
holonomic and non-holonomic robots, any robot footprint that can be
represented as a convex polygon or circle, and exposes its
configuration as ROS parameters that can be set in a launch file. This
package's ROS wrapper adheres to the BaseLocalPlanner interface
specified in the


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
  --pkg base_local_planner

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
