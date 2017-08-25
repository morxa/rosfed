Name:           ros-kinetic-ros_core
Version:        1.3.1
Release:        2%{?dist}
Summary:        ROS package ros_core

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/metapackages-release/archive/release/kinetic/ros_core/1.3.1-0.tar.gz#/ros-kinetic-ros_core-1.3.1-source0.tar.gz


BuildArch: noarch

BuildRequires:  ros-kinetic-catkin

Requires:       ros-kinetic-catkin
Requires:       ros-kinetic-cmake_modules
Requires:       ros-kinetic-common_msgs
Requires:       ros-kinetic-gencpp
Requires:       ros-kinetic-geneus
Requires:       ros-kinetic-genlisp
Requires:       ros-kinetic-genmsg
Requires:       ros-kinetic-gennodejs
Requires:       ros-kinetic-genpy
Requires:       ros-kinetic-message_generation
Requires:       ros-kinetic-message_runtime
Requires:       ros-kinetic-ros
Requires:       ros-kinetic-ros_comm
Requires:       ros-kinetic-rosbag_migration_rule
Requires:       ros-kinetic-rosconsole_bridge
Requires:       ros-kinetic-roscpp_core
Requires:       ros-kinetic-rosgraph_msgs
Requires:       ros-kinetic-roslisp
Requires:       ros-kinetic-rospack
Requires:       ros-kinetic-std_msgs
Requires:       ros-kinetic-std_srvs

%description
A metapackage to aggregate the packages required to use publish /
subscribe, services, launch files, and other core ROS concepts.


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
  --pkg ros_core

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
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.3.1-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.3.1-1
- Update auto-generated Spec file
