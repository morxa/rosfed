Name:           ros-rviz
Version:        noetic.1.14.1
Release:        1%{?dist}
Summary:        ROS package rviz

License:        BSD
URL:            http://wiki.ros.org/rviz

Source0:        https://github.com/ros-gbp/rviz-release/archive/release/noetic/rviz/1.14.1-1.tar.gz#/ros-noetic-rviz-1.14.1-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel

BuildRequires:  assimp-devel
BuildRequires:  eigen3-devel
BuildRequires:  libXext-devel
BuildRequires:  lz4-devel
BuildRequires:  mesa-libGL-devel mesa-libGLU-devel
BuildRequires:  ogre-devel
BuildRequires:  poco-devel
BuildRequires:  python3-qt5-devel
BuildRequires:  python3-sip-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  urdfdom-devel
BuildRequires:  urdfdom-headers-devel
BuildRequires:  yaml-cpp-devel
BuildRequires:  ros-noetic-catkin-devel
BuildRequires:  ros-noetic-cmake_modules-devel
BuildRequires:  ros-noetic-geometry_msgs-devel
BuildRequires:  ros-noetic-image_transport-devel
BuildRequires:  ros-noetic-interactive_markers-devel
BuildRequires:  ros-noetic-laser_geometry-devel
BuildRequires:  ros-noetic-map_msgs-devel
BuildRequires:  ros-noetic-message_filters-devel
BuildRequires:  ros-noetic-message_generation-devel
BuildRequires:  ros-noetic-nav_msgs-devel
BuildRequires:  ros-noetic-pluginlib-devel
BuildRequires:  ros-noetic-python_qt_binding-devel
BuildRequires:  ros-noetic-resource_retriever-devel
BuildRequires:  ros-noetic-rosbag-devel
BuildRequires:  ros-noetic-rosconsole-devel
BuildRequires:  ros-noetic-roscpp-devel
BuildRequires:  ros-noetic-roslib-devel
BuildRequires:  ros-noetic-rospy-devel
BuildRequires:  ros-noetic-rostest-devel
BuildRequires:  ros-noetic-rosunit-devel
BuildRequires:  ros-noetic-sensor_msgs-devel
BuildRequires:  ros-noetic-std_msgs-devel
BuildRequires:  ros-noetic-std_srvs-devel
BuildRequires:  ros-noetic-tf2_geometry_msgs-devel
BuildRequires:  ros-noetic-tf2_ros-devel
BuildRequires:  ros-noetic-urdf-devel
BuildRequires:  ros-noetic-visualization_msgs-devel

Requires:       qt5-qtbase
Requires:       qt5-qtbase-gui
Requires:       ros-noetic-geometry_msgs
Requires:       ros-noetic-image_transport
Requires:       ros-noetic-interactive_markers
Requires:       ros-noetic-laser_geometry
Requires:       ros-noetic-map_msgs
Requires:       ros-noetic-media_export
Requires:       ros-noetic-message_filters
Requires:       ros-noetic-message_runtime
Requires:       ros-noetic-nav_msgs
Requires:       ros-noetic-pluginlib
Requires:       ros-noetic-python_qt_binding
Requires:       ros-noetic-resource_retriever
Requires:       ros-noetic-rosbag
Requires:       ros-noetic-rosconsole
Requires:       ros-noetic-roscpp
Requires:       ros-noetic-roslib
Requires:       ros-noetic-rospy
Requires:       ros-noetic-sensor_msgs
Requires:       ros-noetic-std_msgs
Requires:       ros-noetic-std_srvs
Requires:       ros-noetic-tf2_geometry_msgs
Requires:       ros-noetic-tf2_ros
Requires:       ros-noetic-urdf
Requires:       ros-noetic-visualization_msgs

Provides:  ros-noetic-rviz = 1.14.1-1
Obsoletes: ros-noetic-rviz < 1.14.1-1
Obsoletes: ros-kinetic-rviz < 1.14.1-1



%description
3D visualization tool for ROS.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ogre-devel
Requires:       ros-noetic-catkin-devel
Requires:       assimp-devel
Requires:       eigen3-devel
Requires:       libXext-devel
Requires:       lz4-devel
Requires:       mesa-libGL-devel mesa-libGLU-devel
Requires:       poco-devel
Requires:       python3-qt5-devel
Requires:       python3-sip-devel
Requires:       qt5-qtbase-devel
Requires:       tinyxml2-devel
Requires:       urdfdom-devel
Requires:       urdfdom-headers-devel
Requires:       yaml-cpp-devel
Requires:       ros-noetic-cmake_modules-devel
Requires:       ros-noetic-geometry_msgs-devel
Requires:       ros-noetic-image_transport-devel
Requires:       ros-noetic-interactive_markers-devel
Requires:       ros-noetic-laser_geometry-devel
Requires:       ros-noetic-map_msgs-devel
Requires:       ros-noetic-message_filters-devel
Requires:       ros-noetic-message_generation-devel
Requires:       ros-noetic-nav_msgs-devel
Requires:       ros-noetic-pluginlib-devel
Requires:       ros-noetic-python_qt_binding-devel
Requires:       ros-noetic-resource_retriever-devel
Requires:       ros-noetic-rosbag-devel
Requires:       ros-noetic-rosconsole-devel
Requires:       ros-noetic-roscpp-devel
Requires:       ros-noetic-roslib-devel
Requires:       ros-noetic-rospy-devel
Requires:       ros-noetic-rostest-devel
Requires:       ros-noetic-rosunit-devel
Requires:       ros-noetic-sensor_msgs-devel
Requires:       ros-noetic-std_msgs-devel
Requires:       ros-noetic-std_srvs-devel
Requires:       ros-noetic-tf2_geometry_msgs-devel
Requires:       ros-noetic-tf2_ros-devel
Requires:       ros-noetic-urdf-devel
Requires:       ros-noetic-visualization_msgs-devel
Requires:       ros-noetic-media_export-devel
Requires:       ros-noetic-message_runtime-devel

Provides: ros-noetic-rviz-devel = 1.14.1-1
Obsoletes: ros-noetic-rviz-devel < 1.14.1-1
Obsoletes: ros-kinetic-rviz-devel < 1.14.1-1


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

PATH="$PATH:%{_qt5_bindir}" ; export PATH
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
  --pkg rviz




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
* Thu Sep 10 2020 Nicolas Limpert <limpert@fh-aachen.de> - noetic.1.14.1-1
- Update to latest release
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.14.0-1
- Upgrade to noetic
* Wed Apr 29 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.13.11-2
- Add BR on libXext
* Wed Apr 29 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.13.11-1
- Update to latest release
* Fri Apr 17 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.13.9-1
- Update to latest release
* Tue Feb 04 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.13.7-1
- Update to latest release
* Mon Jul 22 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.13.3-3
- Remove obsolete python2 dependencies
* Sun Jul 21 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.13.3-2
- Switch to python3
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.13.3-1
- Update to ROS melodic release
* Fri Jul 12 2019 Till Hofmann <thofmann@fedoraproject.org> - 1.12.17-2
- Remove ROS distro from package name
* Thu Mar 14 2019 Till Hofmann <thofmann@fedoraproject.org> - 1.12.17-1
- Update to latest release
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.16-3
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.16-2
- devel also requires: the devel package of each run dependency
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.16-1
- Also add upstream's exec_depend as Requires:
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.15-5
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.15-4
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.15-3
- Add Recommends: for all BRs to the devel subpackage
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.15-2
- Split devel package
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.15-1
- Split devel package
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.12.13-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.12.11-1
- Update auto-generated Spec file
