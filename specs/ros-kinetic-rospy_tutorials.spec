Name:           ros-kinetic-rospy_tutorials
Version:        0.7.1
Release:        1%{?dist}
Summary:        ROS package rospy_tutorials

License:        BSD
URL:            http://www.ros.org/wiki/rospy_tutorials

Source0:        https://github.com/ros-gbp/ros_tutorials-release/archive/release/kinetic/rospy_tutorials/0.7.1-0.tar.gz#/ros-kinetic-rospy_tutorials-0.7.1-source0.tar.gz


BuildArch: noarch

BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-message_generation
BuildRequires:  ros-kinetic-rostest
BuildRequires:  ros-kinetic-std_msgs

Requires:       ros-kinetic-message_runtime
Requires:       ros-kinetic-rospy
Requires:       ros-kinetic-std_msgs

%description
This package attempts to show the features of ROS python API step-by-
step, including using messages, servers, parameters, etc. These
tutorials are compatible with the nodes in roscpp_tutorial.


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
  --pkg rospy_tutorials

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
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.7.1-1
- Update auto-generated Spec file