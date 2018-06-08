Name:           ros-kinetic-robot_pose_ekf
Version:        1.14.3
Release:        1%{?dist}
Summary:        ROS package robot_pose_ekf

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/navigation-release/archive/release/kinetic/robot_pose_ekf/1.14.3-0.tar.gz#/ros-kinetic-robot_pose_ekf-1.14.3-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  ros-kinetic-bfl-devel
BuildRequires:  ros-kinetic-catkin-devel
BuildRequires:  ros-kinetic-geometry_msgs-devel
BuildRequires:  ros-kinetic-message_generation-devel
BuildRequires:  ros-kinetic-nav_msgs-devel
BuildRequires:  ros-kinetic-rosbag-devel
BuildRequires:  ros-kinetic-roscpp-devel
BuildRequires:  ros-kinetic-rostest-devel
BuildRequires:  ros-kinetic-sensor_msgs-devel
BuildRequires:  ros-kinetic-std_msgs-devel
BuildRequires:  ros-kinetic-tf-devel

Requires:       ros-kinetic-bfl
Requires:       ros-kinetic-geometry_msgs
Requires:       ros-kinetic-message_runtime
Requires:       ros-kinetic-nav_msgs
Requires:       ros-kinetic-roscpp
Requires:       ros-kinetic-sensor_msgs
Requires:       ros-kinetic-std_msgs
Requires:       ros-kinetic-tf


%description
The Robot Pose EKF package is used to estimate the 3D pose of a robot,
based on (partial) pose measurements coming from different sources. It
uses an extended Kalman filter with a 6D model (3D position and 3D
orientation) to combine measurements from wheel odometry, IMU sensor
and visual odometry. The basic idea is to offer loosely coupled
integration with different sensors, where sensor signals are received
as ROS messages.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-kinetic-catkin-devel
Requires:       ros-kinetic-bfl-devel
Requires:       ros-kinetic-geometry_msgs-devel
Requires:       ros-kinetic-message_generation-devel
Requires:       ros-kinetic-nav_msgs-devel
Requires:       ros-kinetic-rosbag-devel
Requires:       ros-kinetic-roscpp-devel
Requires:       ros-kinetic-rostest-devel
Requires:       ros-kinetic-sensor_msgs-devel
Requires:       ros-kinetic-std_msgs-devel
Requires:       ros-kinetic-tf-devel
Requires:       ros-kinetic-message_runtime-devel

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.



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
  --pkg robot_pose_ekf




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,setup*,env.sh}

touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files_devel.list

find . -maxdepth 1 -type f -iname "*readme*" | sed "s:^:%%doc :" >> files.list
find . -maxdepth 1 -type f -iname "*license*" | sed "s:^:%%license :" >> files.list


echo "This is a package automatically generated with rosfed." >> README_FEDORA
echo "See https://pagure.io/ros for more information." >> README_FEDORA
install -p -D -t %{buildroot}/%{_docdir}/%{name} README_FEDORA
echo %{_docdir}/%{name} >> files.list
install -p -D -t %{buildroot}/%{_docdir}/%{name}-devel README_FEDORA
echo %{_docdir}/%{name}-devel >> files_devel.list


%files -f files.list
%files devel -f files_devel.list


%changelog
* Wed Jun 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.14.3-1
- Initial package
