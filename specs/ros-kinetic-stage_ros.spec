Name:           ros-kinetic-stage_ros
Version:        1.7.5
Release:        2%{?dist}
Summary:        ROS package stage_ros

License:        BSD
URL:            http://ros.org/wiki/stage_ros

Source0:        https://github.com/ros-gbp/stage_ros-release/archive/release/kinetic/stage_ros/1.7.5-0.tar.gz#/ros-kinetic-stage_ros-1.7.5-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  boost-devel
BuildRequires:  fltk-devel
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-geometry_msgs
BuildRequires:  ros-kinetic-nav_msgs
BuildRequires:  ros-kinetic-roscpp
BuildRequires:  ros-kinetic-rostest
BuildRequires:  ros-kinetic-sensor_msgs
BuildRequires:  ros-kinetic-stage
BuildRequires:  ros-kinetic-std_msgs
BuildRequires:  ros-kinetic-std_srvs
BuildRequires:  ros-kinetic-tf

Requires:       ros-kinetic-geometry_msgs
Requires:       ros-kinetic-nav_msgs
Requires:       ros-kinetic-roscpp
Requires:       ros-kinetic-sensor_msgs
Requires:       ros-kinetic-stage
Requires:       ros-kinetic-std_msgs
Requires:       ros-kinetic-std_srvs
Requires:       ros-kinetic-tf

%description
This package provides ROS specific hooks for stage


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
  --pkg stage_ros

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
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.7.5-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.7.5-1
- Update auto-generated Spec file
