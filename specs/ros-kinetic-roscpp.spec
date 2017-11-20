Name:           ros-kinetic-roscpp
Version:        1.12.12
Release:        3%{?dist}
Summary:        ROS package roscpp

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/ros_comm-release/archive/release/kinetic/roscpp/1.12.12-0.tar.gz#/ros-kinetic-roscpp-1.12.12-source0.tar.gz



BuildRequires:  boost-devel
BuildRequires:  log4cxx-devel
BuildRequires:  pkgconfig
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-cpp_common
BuildRequires:  ros-kinetic-message_generation
BuildRequires:  ros-kinetic-rosconsole
BuildRequires:  ros-kinetic-roscpp_serialization
BuildRequires:  ros-kinetic-roscpp_traits
BuildRequires:  ros-kinetic-rosgraph_msgs
BuildRequires:  ros-kinetic-roslang
BuildRequires:  ros-kinetic-rostime
BuildRequires:  ros-kinetic-std_msgs
BuildRequires:  ros-kinetic-xmlrpcpp

Requires:       ros-kinetic-cpp_common
Requires:       ros-kinetic-message_runtime
Requires:       ros-kinetic-rosconsole
Requires:       ros-kinetic-roscpp_serialization
Requires:       ros-kinetic-roscpp_traits
Requires:       ros-kinetic-rosgraph_msgs
Requires:       ros-kinetic-rostime
Requires:       ros-kinetic-std_msgs
Requires:       ros-kinetic-xmlrpcpp

%description
roscpp is a C++ implementation of ROS. It provides a


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
  --pkg roscpp

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
* Mon Nov 20 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.12.12-3
- Add missing BR on log4cxx-devel
* Mon Nov 20 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.12.12-2
- Add missing BR on boost-devel
* Sun Nov 19 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.12.12-1
- Update to latest release
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.12.7-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.12.7-1
- Update auto-generated Spec file
