Name:           ros-kinetic-common_msgs
Version:        1.12.5
Release:        1%{?dist}
Summary:        ROS package common_msgs

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/common_msgs-release/archive/release/kinetic/common_msgs/1.12.5-0.tar.gz#/ros-kinetic-common_msgs-1.12.5-source0.tar.gz


BuildArch: noarch

BuildRequires:  ros-kinetic-catkin

Requires:       ros-kinetic-actionlib_msgs
Requires:       ros-kinetic-diagnostic_msgs
Requires:       ros-kinetic-geometry_msgs
Requires:       ros-kinetic-nav_msgs
Requires:       ros-kinetic-sensor_msgs
Requires:       ros-kinetic-shape_msgs
Requires:       ros-kinetic-stereo_msgs
Requires:       ros-kinetic-trajectory_msgs
Requires:       ros-kinetic-visualization_msgs

%description
common_msgs contains messages that are widely used by other ROS
packages. These includes messages for actions (


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
  --pkg common_msgs

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
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.12.5-1
- Update auto-generated Spec file