Name:           ros-kinetic-actionlib
Version:        1.11.9
Release:        1%{?dist}
Summary:        ROS package actionlib

License:        BSD
URL:            http://www.ros.org/wiki/actionlib

Source0:        https://github.com/ros-gbp/actionlib-release/archive/release/kinetic/actionlib/1.11.9-0.tar.gz#/ros-kinetic-actionlib-1.11.9-source0.tar.gz



BuildRequires:  boost-devel
BuildRequires:  ros-kinetic-actionlib_msgs
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-message_generation
BuildRequires:  ros-kinetic-roscpp
BuildRequires:  ros-kinetic-rosnode
BuildRequires:  ros-kinetic-rospy
BuildRequires:  ros-kinetic-rostest
BuildRequires:  ros-kinetic-std_msgs

Requires:       boost-devel
Requires:       ros-kinetic-actionlib_msgs
Requires:       ros-kinetic-message_runtime
Requires:       ros-kinetic-roscpp
Requires:       ros-kinetic-rospy
Requires:       ros-kinetic-rostest
Requires:       ros-kinetic-std_msgs

%description
The actionlib stack provides a standardized interface for interfacing
with preemptable tasks. Examples of this include moving the base to a
target location, performing a laser scan and returning the resulting
point cloud, detecting the handle of a door, etc.


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
  --pkg actionlib

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
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.11.9-1
- Update auto-generated Spec file
