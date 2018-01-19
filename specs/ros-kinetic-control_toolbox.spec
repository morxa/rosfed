Name:           ros-kinetic-control_toolbox
Version:        1.16.0
Release:        1%{?dist}
Summary:        ROS package control_toolbox

License:        BSD
URL:            http://ros.org/wiki/control_toolbox

Source0:        https://github.com/ros-gbp/control_toolbox-release/archive/release/kinetic/control_toolbox/1.16.0-0.tar.gz#/ros-kinetic-control_toolbox-1.16.0-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  tinyxml-devel
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-cmake_modules
BuildRequires:  ros-kinetic-control_msgs
BuildRequires:  ros-kinetic-dynamic_reconfigure
BuildRequires:  ros-kinetic-message_generation
BuildRequires:  ros-kinetic-realtime_tools
BuildRequires:  ros-kinetic-roscpp
BuildRequires:  ros-kinetic-std_msgs

Requires:       ros-kinetic-cmake_modules
Requires:       ros-kinetic-control_msgs
Requires:       ros-kinetic-dynamic_reconfigure
Requires:       ros-kinetic-message_runtime
Requires:       ros-kinetic-realtime_tools
Requires:       ros-kinetic-roscpp
Requires:       ros-kinetic-std_msgs

%description
The control toolbox contains modules that are useful across all
controllers.


%prep

%setup -c -T
tar --strip-components=1 -xf %{SOURCE0}

%build
# nothing to do here


%install

PYTHONUNBUFFERED=1 ; export PYTHONUNBUFFERED

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
FFLAGS="${FFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FFLAGS ; \
FCFLAGS="${FCFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FCFLAGS ; \
%{?__global_ldflags:LDFLAGS="${LDFLAGS:-%__global_ldflags}" ; export LDFLAGS ;} \


source %{_libdir}/ros/setup.bash

DESTDIR=%{buildroot} ; export DESTDIR

catkin_make_isolated \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCATKIN_ENABLE_TESTING=OFF \
  --source . \
  --install \
  --install-space %{_libdir}/ros/ \
  --pkg control_toolbox

rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,setup*,env.sh}

find %{buildroot}/%{_libdir}/ros/{bin,etc,include,lib*/pkgconfig,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list


find . -maxdepth 1 -type f -iname "*readme*" | sed "s:^:%%doc :" >> files.list
find . -maxdepth 1 -type f -iname "*license*" | sed "s:^:%%license :" >> files.list

%files -f files.list



%changelog
* Fri Jan 19 2018 Tim Niemueller <tim@niemueller.de> - 1.16.0-1
- Initial package
