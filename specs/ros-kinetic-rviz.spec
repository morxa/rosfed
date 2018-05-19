Name:           ros-kinetic-rviz
Version:        1.12.16
Release:        1%{?dist}
Summary:        ROS package rviz

License:        BSD
URL:            http://ros.org/wiki/rviz

Source0:        https://github.com/ros-gbp/rviz-release/archive/release/kinetic/rviz/1.12.16-0.tar.gz#/ros-kinetic-rviz-1.12.16-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  assimp-devel
BuildRequires:  eigen3-devel
BuildRequires:  lz4-devel
BuildRequires:  mesa-libGL-devel mesa-libGLU-devel
BuildRequires:  ogre-devel
BuildRequires:  poco-devel
BuildRequires:  python-qt5-devel
BuildRequires:  qt5-qtbase
BuildRequires:  qt5-qtbase-devel
BuildRequires:  sip-devel
BuildRequires:  tinyxml-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  urdfdom-devel
BuildRequires:  urdfdom-headers-devel
BuildRequires:  yaml-cpp-devel
BuildRequires:  ros-kinetic-catkin-devel
BuildRequires:  ros-kinetic-cmake_modules-devel
BuildRequires:  ros-kinetic-geometry_msgs-devel
BuildRequires:  ros-kinetic-image_transport-devel
BuildRequires:  ros-kinetic-interactive_markers-devel
BuildRequires:  ros-kinetic-laser_geometry-devel
BuildRequires:  ros-kinetic-map_msgs-devel
BuildRequires:  ros-kinetic-message_filters-devel
BuildRequires:  ros-kinetic-nav_msgs-devel
BuildRequires:  ros-kinetic-pluginlib-devel
BuildRequires:  ros-kinetic-python_qt_binding-devel
BuildRequires:  ros-kinetic-resource_retriever-devel
BuildRequires:  ros-kinetic-rosbag-devel
BuildRequires:  ros-kinetic-rosconsole-devel
BuildRequires:  ros-kinetic-roscpp-devel
BuildRequires:  ros-kinetic-roslib-devel
BuildRequires:  ros-kinetic-rospy-devel
BuildRequires:  ros-kinetic-sensor_msgs-devel
BuildRequires:  ros-kinetic-std_msgs-devel
BuildRequires:  ros-kinetic-std_srvs-devel
BuildRequires:  ros-kinetic-tf-devel
BuildRequires:  ros-kinetic-urdf-devel
BuildRequires:  ros-kinetic-visualization_msgs-devel

Requires:       assimp
Requires:       qt5-qtbase
Requires:       qt5-qtbase-gui
Requires:       ros-kinetic-geometry_msgs
Requires:       ros-kinetic-image_transport
Requires:       ros-kinetic-interactive_markers
Requires:       ros-kinetic-laser_geometry
Requires:       ros-kinetic-map_msgs
Requires:       ros-kinetic-media_export
Requires:       ros-kinetic-message_filters
Requires:       ros-kinetic-nav_msgs
Requires:       ros-kinetic-pluginlib
Requires:       ros-kinetic-python_qt_binding
Requires:       ros-kinetic-resource_retriever
Requires:       ros-kinetic-rosbag
Requires:       ros-kinetic-rosconsole
Requires:       ros-kinetic-roscpp
Requires:       ros-kinetic-roslib
Requires:       ros-kinetic-rospy
Requires:       ros-kinetic-sensor_msgs
Requires:       ros-kinetic-std_msgs
Requires:       ros-kinetic-std_srvs
Requires:       ros-kinetic-tf
Requires:       ros-kinetic-urdf
Requires:       ros-kinetic-visualization_msgs


%description
3D visualization tool for ROS.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-kinetic-catkin-devel
Requires:       assimp-devel
Requires:       eigen3-devel
Requires:       lz4-devel
Requires:       mesa-libGL-devel mesa-libGLU-devel
Requires:       ogre-devel
Requires:       poco-devel
Requires:       python-qt5-devel
Requires:       qt5-qtbase
Requires:       qt5-qtbase-devel
Requires:       sip-devel
Requires:       tinyxml-devel
Requires:       tinyxml2-devel
Requires:       urdfdom-devel
Requires:       urdfdom-headers-devel
Requires:       yaml-cpp-devel
Requires:       ros-kinetic-cmake_modules-devel
Requires:       ros-kinetic-geometry_msgs-devel
Requires:       ros-kinetic-image_transport-devel
Requires:       ros-kinetic-interactive_markers-devel
Requires:       ros-kinetic-laser_geometry-devel
Requires:       ros-kinetic-map_msgs-devel
Requires:       ros-kinetic-message_filters-devel
Requires:       ros-kinetic-nav_msgs-devel
Requires:       ros-kinetic-pluginlib-devel
Requires:       ros-kinetic-python_qt_binding-devel
Requires:       ros-kinetic-resource_retriever-devel
Requires:       ros-kinetic-rosbag-devel
Requires:       ros-kinetic-rosconsole-devel
Requires:       ros-kinetic-roscpp-devel
Requires:       ros-kinetic-roslib-devel
Requires:       ros-kinetic-rospy-devel
Requires:       ros-kinetic-sensor_msgs-devel
Requires:       ros-kinetic-std_msgs-devel
Requires:       ros-kinetic-std_srvs-devel
Requires:       ros-kinetic-tf-devel
Requires:       ros-kinetic-urdf-devel
Requires:       ros-kinetic-visualization_msgs-devel

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

DESTDIR=%{buildroot} ; export DESTDIR


catkin_make_isolated \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCATKIN_ENABLE_TESTING=OFF \
  --source . \
  --install \
  --install-space %{_libdir}/ros/ \
  --pkg rviz




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
