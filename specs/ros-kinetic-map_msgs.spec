Name:           ros-kinetic-map_msgs
Version:        1.13.0
Release:        2%{?dist}
Summary:        ROS package map_msgs

License:        BSD
URL:            http://ros.org/wiki/map_msgs

Source0:        https://github.com/ros-gbp/navigation_msgs-release/archive/release/kinetic/map_msgs/1.13.0-0.tar.gz#/ros-kinetic-map_msgs-1.13.0-source0.tar.gz


BuildArch: noarch

BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-message_generation
BuildRequires:  ros-kinetic-nav_msgs
BuildRequires:  ros-kinetic-sensor_msgs
BuildRequires:  ros-kinetic-std_msgs

Requires:       ros-kinetic-message_runtime
Requires:       ros-kinetic-nav_msgs
Requires:       ros-kinetic-sensor_msgs
Requires:       ros-kinetic-std_msgs

%description
This package defines messages commonly used in mapping packages.


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
  --pkg map_msgs

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
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.13.0-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.13.0-1
- Update auto-generated Spec file
