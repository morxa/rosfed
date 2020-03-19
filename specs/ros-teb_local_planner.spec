Name:           ros-teb_local_planner
Version:        melodic.0.8.4
Release:        1%{?dist}
Summary:        ROS package teb_local_planner

License:        BSD
URL:            http://wiki.ros.org/teb_local_planner

Source0:        https://github.com/rst-tu-dortmund/teb_local_planner-release/archive/release/melodic/teb_local_planner/0.8.4-1.tar.gz#/ros-melodic-teb_local_planner-0.8.4-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel

BuildRequires:  ros-melodic-base_local_planner-devel
BuildRequires:  ros-melodic-catkin-devel
BuildRequires:  ros-melodic-cmake_modules-devel
BuildRequires:  ros-melodic-costmap_2d-devel
BuildRequires:  ros-melodic-costmap_converter-devel
BuildRequires:  ros-melodic-dynamic_reconfigure-devel
BuildRequires:  ros-melodic-geometry_msgs-devel
BuildRequires:  ros-melodic-interactive_markers-devel
BuildRequires:  ros-melodic-libg2o-devel
BuildRequires:  ros-melodic-mbf_costmap_core-devel
BuildRequires:  ros-melodic-mbf_msgs-devel
BuildRequires:  ros-melodic-message_generation-devel
BuildRequires:  ros-melodic-message_runtime-devel
BuildRequires:  ros-melodic-nav_core-devel
BuildRequires:  ros-melodic-nav_msgs-devel
BuildRequires:  ros-melodic-pluginlib-devel
BuildRequires:  ros-melodic-roscpp-devel
BuildRequires:  ros-melodic-std_msgs-devel
BuildRequires:  ros-melodic-tf2-devel
BuildRequires:  ros-melodic-tf2_eigen-devel
BuildRequires:  ros-melodic-tf2_geometry_msgs-devel
BuildRequires:  ros-melodic-tf2_ros-devel
BuildRequires:  ros-melodic-visualization_msgs-devel

Requires:       ros-melodic-base_local_planner
Requires:       ros-melodic-costmap_2d
Requires:       ros-melodic-costmap_converter
Requires:       ros-melodic-dynamic_reconfigure
Requires:       ros-melodic-geometry_msgs
Requires:       ros-melodic-interactive_markers
Requires:       ros-melodic-libg2o
Requires:       ros-melodic-mbf_costmap_core
Requires:       ros-melodic-mbf_msgs
Requires:       ros-melodic-message_runtime
Requires:       ros-melodic-nav_core
Requires:       ros-melodic-nav_msgs
Requires:       ros-melodic-pluginlib
Requires:       ros-melodic-roscpp
Requires:       ros-melodic-std_msgs
Requires:       ros-melodic-tf2
Requires:       ros-melodic-tf2_ros
Requires:       ros-melodic-visualization_msgs

Provides:  ros-melodic-teb_local_planner = 0.8.4-1
Obsoletes: ros-melodic-teb_local_planner < 0.8.4-1
Obsoletes: ros-kinetic-teb_local_planner < 0.8.4-1


%description
The teb_local_planner package implements a plugin to the
base_local_planner of the 2D navigation stack. The underlying method
called Timed Elastic Band locally optimizes the robot's trajectory
with respect to trajectory execution time, separation from obstacles
and compliance with kinodynamic constraints at runtime.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-melodic-catkin-devel
Requires:       ros-melodic-message_runtime-devel
Requires:       ros-melodic-base_local_planner-devel
Requires:       ros-melodic-cmake_modules-devel
Requires:       ros-melodic-costmap_2d-devel
Requires:       ros-melodic-costmap_converter-devel
Requires:       ros-melodic-dynamic_reconfigure-devel
Requires:       ros-melodic-geometry_msgs-devel
Requires:       ros-melodic-interactive_markers-devel
Requires:       ros-melodic-libg2o-devel
Requires:       ros-melodic-mbf_costmap_core-devel
Requires:       ros-melodic-mbf_msgs-devel
Requires:       ros-melodic-message_generation-devel
Requires:       ros-melodic-nav_core-devel
Requires:       ros-melodic-nav_msgs-devel
Requires:       ros-melodic-pluginlib-devel
Requires:       ros-melodic-roscpp-devel
Requires:       ros-melodic-std_msgs-devel
Requires:       ros-melodic-tf2-devel
Requires:       ros-melodic-tf2_eigen-devel
Requires:       ros-melodic-tf2_geometry_msgs-devel
Requires:       ros-melodic-tf2_ros-devel
Requires:       ros-melodic-visualization_msgs-devel

Provides: ros-melodic-teb_local_planner-devel = 0.8.4-1
Obsoletes: ros-melodic-teb_local_planner-devel < 0.8.4-1
Obsoletes: ros-kinetic-teb_local_planner-devel < 0.8.4-1

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

# substitute shebang before install block because we run the local catkin script
for f in $(grep -rl python .) ; do
  sed -i.orig '/^#!.*python\s*$/ { s/python/python3/ }' $f
  touch -r $f.orig $f
  rm $f.orig
done

DESTDIR=%{buildroot} ; export DESTDIR


catkin_make_isolated \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCATKIN_ENABLE_TESTING=OFF \
  -DPYTHON_VERSION=%{python3_version} \
  -DPYTHON_VERSION_NODOTS=%{python3_version_nodots} \
  --source . \
  --install \
  --install-space %{_libdir}/ros/ \
  --pkg teb_local_planner




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,local_setup*,setup*,env.sh}

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



# replace cmake python macro in shebang
for file in $(grep -rIl '^#!.*@PYTHON_EXECUTABLE@*$' %{buildroot}) ; do
  sed -i.orig 's:^#!\s*@PYTHON_EXECUTABLE@\s*:%{__python3}:' $file
  touch -r $file.orig $file
  rm $file.orig
done

# replace unversioned python shebang
for file in $(grep -rIl '^#!.*python\s*$' %{buildroot}) ; do
  sed -i.orig '/^#!.*python\s*$/ { s/python/python3/ }' $file
  touch -r $file.orig $file
  rm $file.orig
done

# replace "/usr/bin/env $interpreter" with "/usr/bin/$interpreter"
for interpreter in bash sh python2 python3 ; do
  for file in $(grep -rIl "^#\!.*${interpreter}" %{buildroot}) ; do
    sed -i.orig "s:^#\!\s*/usr/bin/env\s\+${interpreter}.*:#!/usr/bin/${interpreter}:" $file
    touch -r $file.orig $file
    rm $file.orig
  done
done


echo "This is a package automatically generated with rosfed." >> README_FEDORA
echo "See https://pagure.io/ros for more information." >> README_FEDORA
install -m 0644 -p -D -t %{buildroot}/%{_docdir}/%{name} README_FEDORA
echo %{_docdir}/%{name} >> files.list
install -m 0644 -p -D -t %{buildroot}/%{_docdir}/%{name}-devel README_FEDORA
echo %{_docdir}/%{name}-devel >> files_devel.list


%files -f files.list
%files devel -f files_devel.list


%changelog
* Fri Mar 13 2020 Nicolas Limpert - melodic.0.8.4-1
- Initial package
