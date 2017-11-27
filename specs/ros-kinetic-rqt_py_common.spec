Name:           ros-kinetic-rqt_py_common
Version:        0.5.0
Release:        2%{?dist}
Summary:        ROS package rqt_py_common

License:        BSD
URL:            http://ros.org/wiki/rqt_py_common

Source0:        https://github.com/ros-gbp/rqt-release/archive/release/kinetic/rqt_py_common/0.5.0-0.tar.gz#/ros-kinetic-rqt_py_common-0.5.0-source0.tar.gz


BuildArch: noarch

# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-genmsg
BuildRequires:  ros-kinetic-std_msgs

Requires:       ros-kinetic-actionlib
Requires:       ros-kinetic-genpy
Requires:       ros-kinetic-python_qt_binding
Requires:       ros-kinetic-qt_gui
Requires:       ros-kinetic-rosbag
Requires:       ros-kinetic-roslib
Requires:       ros-kinetic-rospy
Requires:       ros-kinetic-rostopic

%description
rqt_py_common provides common functionality for rqt plugins written in
Python. Despite no plugin is provided, this package is part of the
rqt_common_plugins repository to keep refactoring generic
functionality from these common plugins into this package as easy as
possible. Functionality included in this package should cover generic
ROS concepts and should not introduce any special dependencies beside
"ros_base".


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
  --pkg rqt_py_common

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
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.5.0-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.5.0-1
- Update auto-generated Spec file
