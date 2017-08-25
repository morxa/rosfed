Name:           ros-kinetic-tf2_ros
Version:        0.5.16
Release:        2%{?dist}
Summary:        ROS package tf2_ros

License:        BSD
URL:            http://www.ros.org/wiki/tf2_ros

Source0:        https://github.com/ros-gbp/geometry2-release/archive/release/kinetic/tf2_ros/0.5.16-0.tar.gz#/ros-kinetic-tf2_ros-0.5.16-source0.tar.gz



BuildRequires:  ros-kinetic-actionlib
BuildRequires:  ros-kinetic-actionlib_msgs
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-geometry_msgs
BuildRequires:  ros-kinetic-message_filters
BuildRequires:  ros-kinetic-roscpp
BuildRequires:  ros-kinetic-rosgraph
BuildRequires:  ros-kinetic-rospy
BuildRequires:  ros-kinetic-rostest
BuildRequires:  ros-kinetic-std_msgs
BuildRequires:  ros-kinetic-tf2
BuildRequires:  ros-kinetic-tf2_msgs
BuildRequires:  ros-kinetic-tf2_py
BuildRequires:  ros-kinetic-xmlrpcpp

Requires:       ros-kinetic-actionlib
Requires:       ros-kinetic-actionlib_msgs
Requires:       ros-kinetic-geometry_msgs
Requires:       ros-kinetic-message_filters
Requires:       ros-kinetic-roscpp
Requires:       ros-kinetic-rosgraph
Requires:       ros-kinetic-rospy
Requires:       ros-kinetic-std_msgs
Requires:       ros-kinetic-tf2
Requires:       ros-kinetic-tf2_msgs
Requires:       ros-kinetic-tf2_py
Requires:       ros-kinetic-xmlrpcpp

%description
This package contains the ROS bindings for the tf2 library, for both
Python and C++.


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
  --pkg tf2_ros

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
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.5.16-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.5.16-1
- Update auto-generated Spec file
