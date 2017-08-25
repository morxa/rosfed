Name:           ros-kinetic-tf_conversions
Version:        1.11.9
Release:        2%{?dist}
Summary:        ROS package tf_conversions

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/geometry-release/archive/release/kinetic/tf_conversions/1.11.9-0.tar.gz#/ros-kinetic-tf_conversions-1.11.9-source0.tar.gz



BuildRequires:  eigen3-devel
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-cmake_modules
BuildRequires:  ros-kinetic-geometry_msgs
BuildRequires:  ros-kinetic-kdl_conversions
BuildRequires:  ros-kinetic-orocos_kdl
BuildRequires:  ros-kinetic-tf

Requires:       ros-kinetic-geometry_msgs
Requires:       ros-kinetic-kdl_conversions
Requires:       ros-kinetic-orocos_kdl
Requires:       ros-kinetic-python_orocos_kdl
Requires:       ros-kinetic-tf

%description
This package contains a set of conversion functions to convert common
tf datatypes (point, vector, pose, etc) into semantically identical
datatypes used by other libraries. The conversion functions make it
easier for users of the transform library (tf) to work with the
datatype of their choice. Currently this package has support for the
Kinematics and Dynamics Library (KDL) and the Eigen matrix library.
This package is stable, and will get integrated into tf in the next
major release cycle (see roadmap).


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
  --pkg tf_conversions

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
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.11.9-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.11.9-1
- Update auto-generated Spec file
