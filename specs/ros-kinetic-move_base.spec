Name:           ros-kinetic-move_base
Version:        1.14.2
Release:        2%{?dist}
Summary:        ROS package move_base

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/navigation-release/archive/release/kinetic/move_base/1.14.2-0.tar.gz#/ros-kinetic-move_base-1.14.2-source0.tar.gz



BuildRequires:  ros-kinetic-actionlib
BuildRequires:  ros-kinetic-base_local_planner
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-clear_costmap_recovery
BuildRequires:  ros-kinetic-cmake_modules
BuildRequires:  ros-kinetic-costmap_2d
BuildRequires:  ros-kinetic-dynamic_reconfigure
BuildRequires:  ros-kinetic-geometry_msgs
BuildRequires:  ros-kinetic-message_generation
BuildRequires:  ros-kinetic-move_base_msgs
BuildRequires:  ros-kinetic-nav_core
BuildRequires:  ros-kinetic-nav_msgs
BuildRequires:  ros-kinetic-navfn
BuildRequires:  ros-kinetic-pluginlib
BuildRequires:  ros-kinetic-roscpp
BuildRequires:  ros-kinetic-rospy
BuildRequires:  ros-kinetic-rotate_recovery
BuildRequires:  ros-kinetic-std_srvs
BuildRequires:  ros-kinetic-tf

Requires:       ros-kinetic-actionlib
Requires:       ros-kinetic-base_local_planner
Requires:       ros-kinetic-clear_costmap_recovery
Requires:       ros-kinetic-costmap_2d
Requires:       ros-kinetic-dynamic_reconfigure
Requires:       ros-kinetic-geometry_msgs
Requires:       ros-kinetic-message_runtime
Requires:       ros-kinetic-move_base_msgs
Requires:       ros-kinetic-nav_core
Requires:       ros-kinetic-nav_msgs
Requires:       ros-kinetic-navfn
Requires:       ros-kinetic-pluginlib
Requires:       ros-kinetic-roscpp
Requires:       ros-kinetic-rospy
Requires:       ros-kinetic-rotate_recovery
Requires:       ros-kinetic-std_srvs
Requires:       ros-kinetic-tf

%description
The move_base package provides an implementation of an action (see the


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
  --pkg move_base

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
