Name:           ros-kinetic-dwa_local_planner
Version:        1.14.3
Release:        1%{?dist}
Summary:        ROS package dwa_local_planner

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/navigation-release/archive/release/kinetic/dwa_local_planner/1.14.3-0.tar.gz#/ros-kinetic-dwa_local_planner-1.14.3-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  eigen3-devel
BuildRequires:  ros-kinetic-base_local_planner-devel
BuildRequires:  ros-kinetic-catkin-devel
BuildRequires:  ros-kinetic-cmake_modules-devel
BuildRequires:  ros-kinetic-costmap_2d-devel
BuildRequires:  ros-kinetic-dynamic_reconfigure-devel
BuildRequires:  ros-kinetic-nav_core-devel
BuildRequires:  ros-kinetic-nav_msgs-devel
BuildRequires:  ros-kinetic-pcl_conversions-devel
BuildRequires:  ros-kinetic-pluginlib-devel
BuildRequires:  ros-kinetic-roscpp-devel
BuildRequires:  ros-kinetic-tf-devel

Requires:       ros-kinetic-base_local_planner
Requires:       ros-kinetic-costmap_2d
Requires:       ros-kinetic-dynamic_reconfigure
Requires:       ros-kinetic-nav_core
Requires:       ros-kinetic-nav_msgs
Requires:       ros-kinetic-pluginlib
Requires:       ros-kinetic-roscpp
Requires:       ros-kinetic-tf


%description
This package provides an implementation of the Dynamic Window Approach
to local robot navigation on a plane. Given a global plan to follow
and a costmap, the local planner produces velocity commands to send to
a mobile base. This package supports any robot who's footprint can be
represented as a convex polygon or cicrle, and exposes its
configuration as ROS parameters that can be set in a launch file. The
parameters for this planner are also dynamically reconfigurable. This
package's ROS wrapper adheres to the BaseLocalPlanner interface
specified in the

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-kinetic-catkin-devel
Requires:       eigen3-devel
Requires:       ros-kinetic-base_local_planner-devel
Requires:       ros-kinetic-cmake_modules-devel
Requires:       ros-kinetic-costmap_2d-devel
Requires:       ros-kinetic-dynamic_reconfigure-devel
Requires:       ros-kinetic-nav_core-devel
Requires:       ros-kinetic-nav_msgs-devel
Requires:       ros-kinetic-pcl_conversions-devel
Requires:       ros-kinetic-pluginlib-devel
Requires:       ros-kinetic-roscpp-devel
Requires:       ros-kinetic-tf-devel

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
  --pkg dwa_local_planner




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
