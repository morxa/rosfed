Name:           ros-kinetic-navigation
Version:        1.14.3
Release:        1%{?dist}
Summary:        ROS package navigation

License:        BSD,LGPL,LGPL (amcl)
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/navigation-release/archive/release/kinetic/navigation/1.14.3-0.tar.gz#/ros-kinetic-navigation-1.14.3-source0.tar.gz


BuildArch: noarch

# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  ros-kinetic-catkin-devel

Requires:       ros-kinetic-amcl
Requires:       ros-kinetic-base_local_planner
Requires:       ros-kinetic-carrot_planner
Requires:       ros-kinetic-clear_costmap_recovery
Requires:       ros-kinetic-costmap_2d
Requires:       ros-kinetic-dwa_local_planner
Requires:       ros-kinetic-fake_localization
Requires:       ros-kinetic-global_planner
Requires:       ros-kinetic-map_server
Requires:       ros-kinetic-move_base
Requires:       ros-kinetic-move_base_msgs
Requires:       ros-kinetic-move_slow_and_clear
Requires:       ros-kinetic-nav_core
Requires:       ros-kinetic-navfn
Requires:       ros-kinetic-robot_pose_ekf
Requires:       ros-kinetic-rotate_recovery
Requires:       ros-kinetic-voxel_grid


%description
A 2D navigation stack that takes in information from odometry, sensor
streams, and a goal pose and outputs safe velocity commands that are
sent to a mobile base.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       ros-kinetic-catkin-devel
Requires:       ros-kinetic-amcl-devel
Requires:       ros-kinetic-base_local_planner-devel
Requires:       ros-kinetic-carrot_planner-devel
Requires:       ros-kinetic-clear_costmap_recovery-devel
Requires:       ros-kinetic-costmap_2d-devel
Requires:       ros-kinetic-dwa_local_planner-devel
Requires:       ros-kinetic-fake_localization-devel
Requires:       ros-kinetic-global_planner-devel
Requires:       ros-kinetic-map_server-devel
Requires:       ros-kinetic-move_base-devel
Requires:       ros-kinetic-move_base_msgs-devel
Requires:       ros-kinetic-move_slow_and_clear-devel
Requires:       ros-kinetic-nav_core-devel
Requires:       ros-kinetic-navfn-devel
Requires:       ros-kinetic-robot_pose_ekf-devel
Requires:       ros-kinetic-rotate_recovery-devel
Requires:       ros-kinetic-voxel_grid-devel

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
  --pkg navigation




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
