Name:           ros-kinetic-navfn
Version:        1.14.2
Release:        1%{?dist}
Summary:        ROS package navfn

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/navigation-release/archive/release/kinetic/navfn/1.14.2-0.tar.gz#/ros-kinetic-navfn-1.14.2-source0.tar.gz



BuildRequires:  netpbm-devel
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-cmake_modules
BuildRequires:  ros-kinetic-costmap_2d
BuildRequires:  ros-kinetic-geometry_msgs
BuildRequires:  ros-kinetic-message_generation
BuildRequires:  ros-kinetic-nav_core
BuildRequires:  ros-kinetic-nav_msgs
BuildRequires:  ros-kinetic-pcl_conversions
BuildRequires:  ros-kinetic-pcl_ros
BuildRequires:  ros-kinetic-pluginlib
BuildRequires:  ros-kinetic-rosconsole
BuildRequires:  ros-kinetic-roscpp
BuildRequires:  ros-kinetic-rosunit
BuildRequires:  ros-kinetic-tf
BuildRequires:  ros-kinetic-visualization_msgs

Requires:       ros-kinetic-costmap_2d
Requires:       ros-kinetic-geometry_msgs
Requires:       ros-kinetic-message_runtime
Requires:       ros-kinetic-nav_core
Requires:       ros-kinetic-nav_msgs
Requires:       ros-kinetic-pcl_conversions
Requires:       ros-kinetic-pcl_ros
Requires:       ros-kinetic-pluginlib
Requires:       ros-kinetic-rosconsole
Requires:       ros-kinetic-roscpp
Requires:       ros-kinetic-tf
Requires:       ros-kinetic-visualization_msgs

%description
navfn provides a fast interpolated navigation function that can be
used to create plans for a mobile base. The planner assumes a circular
robot and operates on a costmap to find a minimum cost plan from a
start point to an end point in a grid. The navigation function is
computed with Dijkstra's algorithm, but support for an A* heuristic
may also be added in the near future. navfn also provides a ROS
wrapper for the navfn planner that adheres to the
nav_core::BaseGlobalPlanner interface specified in


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
  --pkg navfn

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
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.14.2-1
- Update auto-generated Spec file
