Name:           ros-teb_local_planner
Version:        noetic.0.9.1
Release:        2%{?dist}
Summary:        ROS package teb_local_planner

License:        BSD
URL:            http://wiki.ros.org/teb_local_planner

Source0:        https://github.com/rst-tu-dortmund/teb_local_planner-release/archive/release/noetic/teb_local_planner/0.9.1-1.tar.gz#/ros-noetic-teb_local_planner-0.9.1-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel
BuildRequires:  python-unversioned-command

BuildRequires:  ros-noetic-base_local_planner-devel
BuildRequires:  ros-noetic-catkin-devel
BuildRequires:  ros-noetic-cmake_modules-devel
BuildRequires:  ros-noetic-costmap_2d-devel
BuildRequires:  ros-noetic-costmap_converter-devel
BuildRequires:  ros-noetic-dynamic_reconfigure-devel
BuildRequires:  ros-noetic-geometry_msgs-devel
BuildRequires:  ros-noetic-interactive_markers-devel
BuildRequires:  ros-noetic-libg2o-devel
BuildRequires:  ros-noetic-mbf_costmap_core-devel
BuildRequires:  ros-noetic-mbf_msgs-devel
BuildRequires:  ros-noetic-message_generation-devel
BuildRequires:  ros-noetic-message_runtime-devel
BuildRequires:  ros-noetic-nav_core-devel
BuildRequires:  ros-noetic-nav_msgs-devel
BuildRequires:  ros-noetic-pluginlib-devel
BuildRequires:  ros-noetic-roscpp-devel
BuildRequires:  ros-noetic-std_msgs-devel
BuildRequires:  ros-noetic-tf2-devel
BuildRequires:  ros-noetic-tf2_eigen-devel
BuildRequires:  ros-noetic-tf2_geometry_msgs-devel
BuildRequires:  ros-noetic-tf2_ros-devel
BuildRequires:  ros-noetic-visualization_msgs-devel

Requires:       ros-noetic-base_local_planner
Requires:       ros-noetic-costmap_2d
Requires:       ros-noetic-costmap_converter
Requires:       ros-noetic-dynamic_reconfigure
Requires:       ros-noetic-geometry_msgs
Requires:       ros-noetic-interactive_markers
Requires:       ros-noetic-libg2o
Requires:       ros-noetic-mbf_costmap_core
Requires:       ros-noetic-mbf_msgs
Requires:       ros-noetic-message_runtime
Requires:       ros-noetic-nav_core
Requires:       ros-noetic-nav_msgs
Requires:       ros-noetic-pluginlib
Requires:       ros-noetic-roscpp
Requires:       ros-noetic-std_msgs
Requires:       ros-noetic-tf2
Requires:       ros-noetic-tf2_ros
Requires:       ros-noetic-visualization_msgs

Provides:  ros-noetic-teb_local_planner = 0.9.1-2
Obsoletes: ros-noetic-teb_local_planner < 0.9.1-2
Obsoletes: ros-kinetic-teb_local_planner < 0.9.1-2



%description
The teb_local_planner package implements a plugin to the
base_local_planner of the 2D navigation stack. The underlying method
called Timed Elastic Band locally optimizes the robot's trajectory
with respect to trajectory execution time, separation from obstacles
and compliance with kinodynamic constraints at runtime.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-noetic-catkin-devel
Requires:       ros-noetic-message_runtime-devel
Requires:       ros-noetic-base_local_planner-devel
Requires:       ros-noetic-cmake_modules-devel
Requires:       ros-noetic-costmap_2d-devel
Requires:       ros-noetic-costmap_converter-devel
Requires:       ros-noetic-dynamic_reconfigure-devel
Requires:       ros-noetic-geometry_msgs-devel
Requires:       ros-noetic-interactive_markers-devel
Requires:       ros-noetic-libg2o-devel
Requires:       ros-noetic-mbf_costmap_core-devel
Requires:       ros-noetic-mbf_msgs-devel
Requires:       ros-noetic-message_generation-devel
Requires:       ros-noetic-nav_core-devel
Requires:       ros-noetic-nav_msgs-devel
Requires:       ros-noetic-pluginlib-devel
Requires:       ros-noetic-roscpp-devel
Requires:       ros-noetic-std_msgs-devel
Requires:       ros-noetic-tf2-devel
Requires:       ros-noetic-tf2_eigen-devel
Requires:       ros-noetic-tf2_geometry_msgs-devel
Requires:       ros-noetic-tf2_ros-devel
Requires:       ros-noetic-visualization_msgs-devel

Provides: ros-noetic-teb_local_planner-devel = 0.9.1-2
Obsoletes: ros-noetic-teb_local_planner-devel < 0.9.1-2
Obsoletes: ros-kinetic-teb_local_planner-devel < 0.9.1-2


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
%py3_shebang_fix .

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
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig,share/teb_local_planner/cmake} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files_devel.list

find . -maxdepth 1 -type f -iname "*readme*" | sed "s:^:%%doc :" >> files.list
find . -maxdepth 1 -type f -iname "*license*" | sed "s:^:%%license :" >> files.list



# replace cmake python macro in shebang
for file in $(grep -rIl '^#!.*@PYTHON_EXECUTABLE@.*$' %{buildroot}) ; do
  sed -i.orig 's:^#!\s*@PYTHON_EXECUTABLE@\s*:%{__python3}:' $file
  touch -r $file.orig $file
  rm $file.orig
done


echo "This is a package automatically generated with rosfed." >> README_FEDORA
echo "See https://pagure.io/ros for more information." >> README_FEDORA
install -m 0644 -p -D -t %{buildroot}/%{_docdir}/%{name} README_FEDORA
echo %{_docdir}/%{name} >> files.list
install -m 0644 -p -D -t %{buildroot}/%{_docdir}/%{name}-devel README_FEDORA
echo %{_docdir}/%{name}-devel >> files_devel.list

%py3_shebang_fix %{buildroot}

# Also fix .py.in files
for pyfile in $(grep -rIl '^#!.*python.*$' %{buildroot}) ; do
  %py3_shebang_fix $pyfile
done


%files -f files.list
%files devel -f files_devel.list


%changelog
* Tue Feb 23 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.9.1-2
- Modernize python shebang replacement
* Thu Jun 11 2020 Nicolas Limpert - noetic.0.9.1-1
- Update to noetic
* Fri Mar 13 2020 Nicolas Limpert - melodic.0.8.4-1
- Initial package
