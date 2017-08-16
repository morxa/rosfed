Name:           ros-kinetic-rqt_gui_cpp
Version:        0.5.0
Release:        1%{?dist}
Summary:        ROS package rqt_gui_cpp

License:        BSD
URL:            http://ros.org/wiki/rqt_gui_cpp

Source0:        https://github.com/ros-gbp/rqt-release/archive/release/kinetic/rqt_gui_cpp/0.5.0-0.tar.gz#/ros-kinetic-rqt_gui_cpp-0.5.0-source0.tar.gz



BuildRequires:  qt5-qtbase-devel
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-nodelet
BuildRequires:  ros-kinetic-qt_gui
BuildRequires:  ros-kinetic-qt_gui_cpp
BuildRequires:  ros-kinetic-roscpp

Requires:       ros-kinetic-nodelet
Requires:       ros-kinetic-qt_gui
Requires:       ros-kinetic-qt_gui_cpp
Requires:       ros-kinetic-roscpp

%description
rqt_gui_cpp enables GUI plugins to use the C++ client library for ROS.


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
  --pkg rqt_gui_cpp

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
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.5.0-1
- Update auto-generated Spec file
