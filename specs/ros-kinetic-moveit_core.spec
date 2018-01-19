Name:           ros-kinetic-moveit_core
Version:        0.9.11
Release:        1%{?dist}
Summary:        ROS package moveit_core

License:        BSD
URL:            http://moveit.ros.org

Source0:        https://github.com/ros-gbp/moveit-release/archive/release/kinetic/moveit_core/0.9.11-0.tar.gz#/ros-kinetic-moveit_core-0.9.11-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  assimp
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  eigen3-devel
BuildRequires:  fcl-devel
BuildRequires:  libccd-devel
BuildRequires:  pkgconfig
BuildRequires:  tinyxml-devel
BuildRequires:  urdfdom-devel
BuildRequires:  urdfdom-headers-devel
BuildRequires:  ros-kinetic-angles
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-eigen_conversions
BuildRequires:  ros-kinetic-eigen_stl_containers
BuildRequires:  ros-kinetic-geometric_shapes
BuildRequires:  ros-kinetic-geometry_msgs
BuildRequires:  ros-kinetic-kdl_parser
BuildRequires:  ros-kinetic-moveit_msgs
BuildRequires:  ros-kinetic-moveit_resources
BuildRequires:  ros-kinetic-octomap
BuildRequires:  ros-kinetic-octomap_msgs
BuildRequires:  ros-kinetic-orocos_kdl
BuildRequires:  ros-kinetic-random_numbers
BuildRequires:  ros-kinetic-roslib
BuildRequires:  ros-kinetic-rostime
BuildRequires:  ros-kinetic-rosunit
BuildRequires:  ros-kinetic-sensor_msgs
BuildRequires:  ros-kinetic-shape_msgs
BuildRequires:  ros-kinetic-srdfdom
BuildRequires:  ros-kinetic-std_msgs
BuildRequires:  ros-kinetic-tf_conversions
BuildRequires:  ros-kinetic-trajectory_msgs
BuildRequires:  ros-kinetic-urdf
BuildRequires:  ros-kinetic-visualization_msgs

Requires:       assimp
Requires:       ros-kinetic-eigen_conversions
Requires:       ros-kinetic-eigen_stl_containers
Requires:       ros-kinetic-geometric_shapes
Requires:       ros-kinetic-geometry_msgs
Requires:       ros-kinetic-kdl_parser
Requires:       ros-kinetic-moveit_msgs
Requires:       ros-kinetic-octomap
Requires:       ros-kinetic-octomap_msgs
Requires:       ros-kinetic-random_numbers
Requires:       ros-kinetic-rostime
Requires:       ros-kinetic-sensor_msgs
Requires:       ros-kinetic-srdfdom
Requires:       ros-kinetic-std_msgs
Requires:       ros-kinetic-trajectory_msgs
Requires:       ros-kinetic-urdf
Requires:       ros-kinetic-visualization_msgs

%description
Core libraries used by MoveIt!


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
  --pkg moveit_core

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
* Thu Jan 18 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.9.11-1
- Initial package
