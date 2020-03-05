Name:           ros-gazebo_plugins
Version:        melodic.2.8.6
Release:        1%{?dist}
Summary:        ROS package gazebo_plugins

License:        BSD, Apache 2.0
URL:            http://gazebosim.org/tutorials?cat=connect_ros

Source0:        https://github.com/ros-gbp/gazebo_ros_pkgs-release/archive/release/melodic/gazebo_plugins/2.8.6-1.tar.gz#/ros-melodic-gazebo_plugins-2.8.6-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel

BuildRequires:  bullet-devel
BuildRequires:  gazebo-devel
BuildRequires:  libuuid-devel
BuildRequires:  opencv-devel
BuildRequires:  poco-devel
BuildRequires:  tinyxml-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  urdfdom-devel
BuildRequires:  ros-melodic-angles-devel
BuildRequires:  ros-melodic-camera_info_manager-devel
BuildRequires:  ros-melodic-catkin-devel
BuildRequires:  ros-melodic-cv_bridge-devel
BuildRequires:  ros-melodic-diagnostic_updater-devel
BuildRequires:  ros-melodic-dynamic_reconfigure-devel
BuildRequires:  ros-melodic-gazebo_dev-devel
BuildRequires:  ros-melodic-gazebo_msgs-devel
BuildRequires:  ros-melodic-gazebo_ros-devel
BuildRequires:  ros-melodic-geometry_msgs-devel
BuildRequires:  ros-melodic-image_transport-devel
BuildRequires:  ros-melodic-message_generation-devel
BuildRequires:  ros-melodic-nav_msgs-devel
BuildRequires:  ros-melodic-nodelet-devel
BuildRequires:  ros-melodic-polled_camera-devel
BuildRequires:  ros-melodic-rosconsole-devel
BuildRequires:  ros-melodic-roscpp-devel
BuildRequires:  ros-melodic-rosgraph_msgs-devel
BuildRequires:  ros-melodic-rospy-devel
BuildRequires:  ros-melodic-rostest-devel
BuildRequires:  ros-melodic-sensor_msgs-devel
BuildRequires:  ros-melodic-std_msgs-devel
BuildRequires:  ros-melodic-std_srvs-devel
BuildRequires:  ros-melodic-tf-devel
BuildRequires:  ros-melodic-tf2_ros-devel
BuildRequires:  ros-melodic-trajectory_msgs-devel
BuildRequires:  ros-melodic-urdf-devel

Requires:       ros-melodic-angles
Requires:       ros-melodic-camera_info_manager
Requires:       ros-melodic-cv_bridge
Requires:       ros-melodic-diagnostic_updater
Requires:       ros-melodic-dynamic_reconfigure
Requires:       ros-melodic-gazebo_dev
Requires:       ros-melodic-gazebo_msgs
Requires:       ros-melodic-gazebo_ros
Requires:       ros-melodic-geometry_msgs
Requires:       ros-melodic-image_transport
Requires:       ros-melodic-message_runtime
Requires:       ros-melodic-nav_msgs
Requires:       ros-melodic-nodelet
Requires:       ros-melodic-polled_camera
Requires:       ros-melodic-rosconsole
Requires:       ros-melodic-roscpp
Requires:       ros-melodic-rosgraph_msgs
Requires:       ros-melodic-rospy
Requires:       ros-melodic-sensor_msgs
Requires:       ros-melodic-std_msgs
Requires:       ros-melodic-std_srvs
Requires:       ros-melodic-tf
Requires:       ros-melodic-tf2_ros
Requires:       ros-melodic-trajectory_msgs
Requires:       ros-melodic-urdf

Provides:  ros-melodic-gazebo_plugins = 2.8.6-1
Obsoletes: ros-melodic-gazebo_plugins < 2.8.6-1
Obsoletes: ros-kinetic-gazebo_plugins < 2.8.6-1


%description
Robot-independent Gazebo plugins for sensors, motors and dynamic
reconfigurable components.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-melodic-catkin-devel
Requires:       bullet-devel
Requires:       gazebo-devel
Requires:       libuuid-devel
Requires:       opencv-devel
Requires:       poco-devel
Requires:       tinyxml-devel
Requires:       tinyxml2-devel
Requires:       urdfdom-devel
Requires:       ros-melodic-angles-devel
Requires:       ros-melodic-camera_info_manager-devel
Requires:       ros-melodic-cv_bridge-devel
Requires:       ros-melodic-diagnostic_updater-devel
Requires:       ros-melodic-dynamic_reconfigure-devel
Requires:       ros-melodic-gazebo_dev-devel
Requires:       ros-melodic-gazebo_msgs-devel
Requires:       ros-melodic-gazebo_ros-devel
Requires:       ros-melodic-geometry_msgs-devel
Requires:       ros-melodic-image_transport-devel
Requires:       ros-melodic-message_generation-devel
Requires:       ros-melodic-nav_msgs-devel
Requires:       ros-melodic-nodelet-devel
Requires:       ros-melodic-polled_camera-devel
Requires:       ros-melodic-rosconsole-devel
Requires:       ros-melodic-roscpp-devel
Requires:       ros-melodic-rosgraph_msgs-devel
Requires:       ros-melodic-rospy-devel
Requires:       ros-melodic-rostest-devel
Requires:       ros-melodic-sensor_msgs-devel
Requires:       ros-melodic-std_msgs-devel
Requires:       ros-melodic-std_srvs-devel
Requires:       ros-melodic-tf-devel
Requires:       ros-melodic-tf2_ros-devel
Requires:       ros-melodic-trajectory_msgs-devel
Requires:       ros-melodic-urdf-devel
Requires:       ros-melodic-message_runtime-devel

Provides: ros-melodic-gazebo_plugins-devel = 2.8.6-1
Obsoletes: ros-melodic-gazebo_plugins-devel < 2.8.6-1
Obsoletes: ros-kinetic-gazebo_plugins-devel < 2.8.6-1

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
  --pkg gazebo_plugins




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
* Tue Feb 04 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.2.8.6-1
- Update to latest release
* Mon Jul 22 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.2.8.4-3
- Remove obsolete python2 dependencies
* Sun Jul 21 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.2.8.4-2
- Switch to python3
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.2.8.4-1
- Update to ROS melodic release
* Thu Mar 14 2019 Till Hofmann <thofmann@fedoraproject.org> - 2.5.18-1
- Update to latest release
* Tue Jun 26 2018 Till Hofmann <thofmann@fedoraproject.org> - 2.5.17-1
- Update to latest release
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 2.5.14-4
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 2.5.14-3
- devel also requires: the devel package of each run dependency
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 2.5.14-2
- Also add upstream's exec_depend as Requires:
* Thu Jan 18 2018 Till Hofmann <thofmann@fedoraproject.org> - 2.5.14-1
- Initial package
