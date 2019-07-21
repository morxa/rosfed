Name:           ros-kinetic-effort_controllers
Version:        0.13.2
Release:        1%{?dist}
Summary:        ROS package effort_controllers

License:        BSD
URL:            https://github.com/ros-controls/ros_controllers/wiki

Source0:        https://github.com/ros-gbp/ros_controllers-release/archive/release/kinetic/effort_controllers/0.13.2-0.tar.gz#/ros-kinetic-effort_controllers-0.13.2-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  poco-devel
BuildRequires:  tinyxml-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  urdfdom-devel
BuildRequires:  ros-kinetic-angles
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-control_msgs
BuildRequires:  ros-kinetic-control_toolbox
BuildRequires:  ros-kinetic-controller_interface
BuildRequires:  ros-kinetic-forward_command_controller
BuildRequires:  ros-kinetic-realtime_tools
BuildRequires:  ros-kinetic-urdf

Requires:       ros-kinetic-angles
Requires:       ros-kinetic-control_msgs
Requires:       ros-kinetic-control_toolbox
Requires:       ros-kinetic-controller_interface
Requires:       ros-kinetic-forward_command_controller
Requires:       ros-kinetic-realtime_tools
Requires:       ros-kinetic-urdf

%description
effort_controllers


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
  --pkg effort_controllers

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
* Fri Jan 19 2018 Tim Niemueller <tim@niemueller.de> - 0.13.2-1
- Initial package
