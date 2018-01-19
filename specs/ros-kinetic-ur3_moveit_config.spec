Name:           ros-kinetic-ur3_moveit_config
Version:        1.2.1
Release:        1%{?dist}
Summary:        ROS package ur3_moveit_config

License:        BSD
URL:            http://moveit.ros.org/

Source0:        https://github.com/ros-industrial-release/universal_robot-release/archive/release/kinetic/ur3_moveit_config/1.2.1-0.tar.gz#/ros-kinetic-ur3_moveit_config-1.2.1-source0.tar.gz


BuildArch: noarch

# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-ur_description

Requires:       ros-kinetic-joint_state_publisher
Requires:       ros-kinetic-moveit_fake_controller_manager
Requires:       ros-kinetic-moveit_planners_ompl
Requires:       ros-kinetic-moveit_ros_move_group
Requires:       ros-kinetic-moveit_ros_visualization
Requires:       ros-kinetic-moveit_simple_controller_manager
Requires:       ros-kinetic-robot_state_publisher
Requires:       ros-kinetic-ur_description
Requires:       ros-kinetic-xacro

%description
An automatically generated package with all the configuration and
launch files for using the ur3 with the MoveIt Motion Planning
Framework


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
  --pkg ur3_moveit_config

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
* Fri Jan 19 2018 Tim Niemueller <tim@niemueller.de> - 1.2.1-1
- Initial package
