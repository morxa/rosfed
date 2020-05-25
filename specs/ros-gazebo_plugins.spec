Name:           ros-gazebo_plugins
Version:        noetic.2.9.1
Release:        1%{?dist}
Summary:        ROS package gazebo_plugins

License:        BSD, Apache 2.0
URL:            http://gazebosim.org/tutorials?cat=connect_ros

Source0:        https://github.com/ros-gbp/gazebo_ros_pkgs-release/archive/release/noetic/gazebo_plugins/2.9.1-1.tar.gz#/ros-noetic-gazebo_plugins-2.9.1-source0.tar.gz



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
BuildRequires:  ros-noetic-angles-devel
BuildRequires:  ros-noetic-camera_info_manager-devel
BuildRequires:  ros-noetic-catkin-devel
BuildRequires:  ros-noetic-cv_bridge-devel
BuildRequires:  ros-noetic-diagnostic_updater-devel
BuildRequires:  ros-noetic-dynamic_reconfigure-devel
BuildRequires:  ros-noetic-gazebo_dev-devel
BuildRequires:  ros-noetic-gazebo_msgs-devel
BuildRequires:  ros-noetic-gazebo_ros-devel
BuildRequires:  ros-noetic-geometry_msgs-devel
BuildRequires:  ros-noetic-image_transport-devel
BuildRequires:  ros-noetic-message_generation-devel
BuildRequires:  ros-noetic-nav_msgs-devel
BuildRequires:  ros-noetic-nodelet-devel
BuildRequires:  ros-noetic-polled_camera-devel
BuildRequires:  ros-noetic-rosconsole-devel
BuildRequires:  ros-noetic-roscpp-devel
BuildRequires:  ros-noetic-rosgraph_msgs-devel
BuildRequires:  ros-noetic-rospy-devel
BuildRequires:  ros-noetic-rostest-devel
BuildRequires:  ros-noetic-sensor_msgs-devel
BuildRequires:  ros-noetic-std_msgs-devel
BuildRequires:  ros-noetic-std_srvs-devel
BuildRequires:  ros-noetic-tf-devel
BuildRequires:  ros-noetic-tf2_ros-devel
BuildRequires:  ros-noetic-trajectory_msgs-devel
BuildRequires:  ros-noetic-urdf-devel
BuildRequires:  ros-noetic-visualization_msgs-devel

Requires:       ros-noetic-angles
Requires:       ros-noetic-camera_info_manager
Requires:       ros-noetic-cv_bridge
Requires:       ros-noetic-diagnostic_updater
Requires:       ros-noetic-dynamic_reconfigure
Requires:       ros-noetic-gazebo_dev
Requires:       ros-noetic-gazebo_msgs
Requires:       ros-noetic-gazebo_ros
Requires:       ros-noetic-geometry_msgs
Requires:       ros-noetic-image_transport
Requires:       ros-noetic-message_runtime
Requires:       ros-noetic-nav_msgs
Requires:       ros-noetic-nodelet
Requires:       ros-noetic-polled_camera
Requires:       ros-noetic-rosconsole
Requires:       ros-noetic-roscpp
Requires:       ros-noetic-rosgraph_msgs
Requires:       ros-noetic-rospy
Requires:       ros-noetic-sensor_msgs
Requires:       ros-noetic-std_msgs
Requires:       ros-noetic-std_srvs
Requires:       ros-noetic-tf
Requires:       ros-noetic-tf2_ros
Requires:       ros-noetic-trajectory_msgs
Requires:       ros-noetic-urdf
Requires:       ros-noetic-visualization_msgs

Provides:  ros-noetic-gazebo_plugins = 2.9.1-1
Obsoletes: ros-noetic-gazebo_plugins < 2.9.1-1
Obsoletes: ros-kinetic-gazebo_plugins < 2.9.1-1



%description
Robot-independent Gazebo plugins for sensors, motors and dynamic
reconfigurable components.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-noetic-catkin-devel
Requires:       bullet-devel
Requires:       gazebo-devel
Requires:       libuuid-devel
Requires:       opencv-devel
Requires:       poco-devel
Requires:       tinyxml-devel
Requires:       tinyxml2-devel
Requires:       urdfdom-devel
Requires:       ros-noetic-angles-devel
Requires:       ros-noetic-camera_info_manager-devel
Requires:       ros-noetic-cv_bridge-devel
Requires:       ros-noetic-diagnostic_updater-devel
Requires:       ros-noetic-dynamic_reconfigure-devel
Requires:       ros-noetic-gazebo_dev-devel
Requires:       ros-noetic-gazebo_msgs-devel
Requires:       ros-noetic-gazebo_ros-devel
Requires:       ros-noetic-geometry_msgs-devel
Requires:       ros-noetic-image_transport-devel
Requires:       ros-noetic-message_generation-devel
Requires:       ros-noetic-nav_msgs-devel
Requires:       ros-noetic-nodelet-devel
Requires:       ros-noetic-polled_camera-devel
Requires:       ros-noetic-rosconsole-devel
Requires:       ros-noetic-roscpp-devel
Requires:       ros-noetic-rosgraph_msgs-devel
Requires:       ros-noetic-rospy-devel
Requires:       ros-noetic-rostest-devel
Requires:       ros-noetic-sensor_msgs-devel
Requires:       ros-noetic-std_msgs-devel
Requires:       ros-noetic-std_srvs-devel
Requires:       ros-noetic-tf-devel
Requires:       ros-noetic-tf2_ros-devel
Requires:       ros-noetic-trajectory_msgs-devel
Requires:       ros-noetic-urdf-devel
Requires:       ros-noetic-visualization_msgs-devel
Requires:       ros-noetic-message_runtime-devel

Provides: ros-noetic-gazebo_plugins-devel = 2.9.1-1
Obsoletes: ros-noetic-gazebo_plugins-devel < 2.9.1-1
Obsoletes: ros-kinetic-gazebo_plugins-devel < 2.9.1-1


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
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.2.9.1-1
- Upgrade to noetic
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
