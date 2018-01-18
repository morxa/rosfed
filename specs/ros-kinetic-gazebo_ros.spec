Name:           ros-kinetic-gazebo_ros
Version:        2.5.14
Release:        1%{?dist}
Summary:        ROS package gazebo_ros

License:        Apache 2.0
URL:            http://gazebosim.org/tutorials?cat=connect_ros

Source0:        https://github.com/ros-gbp/gazebo_ros_pkgs-release/archive/release/kinetic/gazebo_ros/2.5.14-1.tar.gz#/ros-kinetic-gazebo_ros-2.5.14-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  bullet-devel
BuildRequires:  gazebo-devel
BuildRequires:  libuuid-devel
BuildRequires:  tinyxml-devel
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-cmake_modules
BuildRequires:  ros-kinetic-dynamic_reconfigure
BuildRequires:  ros-kinetic-gazebo_dev
BuildRequires:  ros-kinetic-gazebo_msgs
BuildRequires:  ros-kinetic-geometry_msgs
BuildRequires:  ros-kinetic-roscpp
BuildRequires:  ros-kinetic-rosgraph_msgs
BuildRequires:  ros-kinetic-roslib
BuildRequires:  ros-kinetic-std_msgs
BuildRequires:  ros-kinetic-std_srvs
BuildRequires:  ros-kinetic-tf
BuildRequires:  ros-kinetic-trajectory_msgs

Requires:       ros-kinetic-dynamic_reconfigure
Requires:       ros-kinetic-gazebo_msgs
Requires:       ros-kinetic-geometry_msgs
Requires:       ros-kinetic-roscpp
Requires:       ros-kinetic-rosgraph_msgs
Requires:       ros-kinetic-roslib
Requires:       ros-kinetic-std_msgs
Requires:       ros-kinetic-std_srvs
Requires:       ros-kinetic-tf

%description
Provides ROS plugins that offer message and service publishers for
interfacing with


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
  --pkg gazebo_ros

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
* Thu Jan 18 2018 Till Hofmann <thofmann@fedoraproject.org> - 2.5.14-1
- Initial package
