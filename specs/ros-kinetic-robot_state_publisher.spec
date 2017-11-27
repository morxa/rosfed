Name:           ros-kinetic-robot_state_publisher
Version:        1.13.4
Release:        2%{?dist}
Summary:        ROS package robot_state_publisher

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/robot_state_publisher-release/archive/release/kinetic/robot_state_publisher/1.13.4-0.tar.gz#/ros-kinetic-robot_state_publisher-1.13.4-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  eigen3-devel
BuildRequires:  tinyxml-devel
BuildRequires:  urdfdom-devel
BuildRequires:  urdfdom-headers-devel
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-kdl_parser
BuildRequires:  ros-kinetic-orocos_kdl
BuildRequires:  ros-kinetic-rosconsole
BuildRequires:  ros-kinetic-roscpp
BuildRequires:  ros-kinetic-rostest
BuildRequires:  ros-kinetic-rostime
BuildRequires:  ros-kinetic-sensor_msgs
BuildRequires:  ros-kinetic-tf
BuildRequires:  ros-kinetic-tf2_kdl
BuildRequires:  ros-kinetic-tf2_ros

Requires:       ros-kinetic-catkin
Requires:       ros-kinetic-kdl_parser
Requires:       ros-kinetic-orocos_kdl
Requires:       ros-kinetic-rosconsole
Requires:       ros-kinetic-roscpp
Requires:       ros-kinetic-rostime
Requires:       ros-kinetic-sensor_msgs
Requires:       ros-kinetic-tf
Requires:       ros-kinetic-tf2_kdl
Requires:       ros-kinetic-tf2_ros

%description
This package allows you to publish the state of a robot to


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
  --pkg robot_state_publisher

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
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.13.4-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.13.4-1
- Update auto-generated Spec file
