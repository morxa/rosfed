Name:           ros-kinetic-pluginlib
Version:        1.11.2
Release:        2%{?dist}
Summary:        ROS package pluginlib

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/pluginlib-release/archive/release/kinetic/pluginlib/1.11.2-0.tar.gz#/ros-kinetic-pluginlib-1.11.2-source0.tar.gz



BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  poco-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-class_loader
BuildRequires:  ros-kinetic-cmake_modules
BuildRequires:  ros-kinetic-rosconsole
BuildRequires:  ros-kinetic-roslib

Requires:       ros-kinetic-class_loader
Requires:       ros-kinetic-rosconsole
Requires:       ros-kinetic-roslib

%description
The pluginlib package provides tools for writing and dynamically
loading plugins using the ROS build infrastructure. To work, these
tools require plugin providers to register their plugins in the
package.xml of their package.


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
  --pkg pluginlib

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
* Mon Nov 20 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.11.2-2
- Add missing BR on console-bridge-devel and poco-devel
* Sun Nov 19 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.11.2-1
- Update to latest release
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.10.5-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.10.5-1
- Update auto-generated Spec file
