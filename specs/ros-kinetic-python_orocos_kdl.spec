Name:           ros-kinetic-python_orocos_kdl
Version:        1.3.1
Release:        1%{?dist}
Summary:        ROS package python_orocos_kdl

License:        LGPL
URL:            http://www.ros.org/

Source0:        https://github.com/smits/orocos-kdl-release/archive/release/kinetic/python_orocos_kdl/1.3.1-0.tar.gz#/ros-kinetic-python_orocos_kdl-1.3.1-source0.tar.gz



BuildRequires:  cmake
BuildRequires:  sip-devel
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-orocos_kdl

Requires:       sip-devel
Requires:       ros-kinetic-catkin
Requires:       ros-kinetic-orocos_kdl

%description
This package contains the python bindings PyKDL for the Kinematics and
Dynamics Library (KDL), distributed by the Orocos Project.


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
  --pkg python_orocos_kdl

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
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.3.1-1
- Update auto-generated Spec file
