Name:           ros-moveit_ros_occupancy_map_monitor
Version:        melodic.1.0.3
Release:        1%{?dist}
Summary:        ROS package moveit_ros_occupancy_map_monitor

License:        BSD
URL:            http://moveit.ros.org

Source0:        https://github.com/ros-gbp/moveit-release/archive/release/melodic/moveit_ros_occupancy_map_monitor/1.0.3-1.tar.gz#/ros-melodic-moveit_ros_occupancy_map_monitor-1.0.3-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel

BuildRequires:  eigen3-devel
BuildRequires:  ros-melodic-catkin-devel
BuildRequires:  ros-melodic-geometric_shapes-devel
BuildRequires:  ros-melodic-moveit_core-devel
BuildRequires:  ros-melodic-moveit_msgs-devel
BuildRequires:  ros-melodic-octomap-devel
BuildRequires:  ros-melodic-pluginlib-devel
BuildRequires:  ros-melodic-rosunit-devel
BuildRequires:  ros-melodic-tf2_ros-devel

Requires:       ros-melodic-geometric_shapes
Requires:       ros-melodic-moveit_core
Requires:       ros-melodic-moveit_msgs
Requires:       ros-melodic-octomap
Requires:       ros-melodic-pluginlib
Requires:       ros-melodic-tf2_ros

Provides:  ros-melodic-moveit_ros_occupancy_map_monitor = 1.0.3-1
Obsoletes: ros-melodic-moveit_ros_occupancy_map_monitor < 1.0.3-1
Obsoletes: ros-kinetic-moveit_ros_occupancy_map_monitor < 1.0.3-1


%description
Components of MoveIt! connecting to occupancy map

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-melodic-catkin-devel
Requires:       eigen3-devel
Requires:       ros-melodic-geometric_shapes-devel
Requires:       ros-melodic-moveit_core-devel
Requires:       ros-melodic-moveit_msgs-devel
Requires:       ros-melodic-octomap-devel
Requires:       ros-melodic-pluginlib-devel
Requires:       ros-melodic-rosunit-devel
Requires:       ros-melodic-tf2_ros-devel

Provides: ros-melodic-moveit_ros_occupancy_map_monitor-devel = 1.0.3-1
Obsoletes: ros-melodic-moveit_ros_occupancy_map_monitor-devel < 1.0.3-1
Obsoletes: ros-kinetic-moveit_ros_occupancy_map_monitor-devel < 1.0.3-1

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
  --pkg moveit_ros_occupancy_map_monitor




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
* Wed Apr 29 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.0.3-1
- Update to latest release
