Name:           ros-moveit_ros_visualization
Version:        melodic.1.0.2
Release:        1%{?dist}
Summary:        ROS package moveit_ros_visualization

License:        BSD
URL:            http://moveit.ros.org

Source0:        https://github.com/ros-gbp/moveit-release/archive/release/melodic/moveit_ros_visualization/1.0.2-1.tar.gz#/ros-melodic-moveit_ros_visualization-1.0.2-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel

BuildRequires:  eigen3-devel
BuildRequires:  fcl-devel
BuildRequires:  ogre-devel
BuildRequires:  pkgconfig
BuildRequires:  poco-devel
BuildRequires:  qt5-qtbase
BuildRequires:  qt5-qtbase-devel
BuildRequires:  tinyxml-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  urdfdom-devel
BuildRequires:  ros-melodic-catkin-devel
BuildRequires:  ros-melodic-class_loader-devel
BuildRequires:  ros-melodic-geometric_shapes-devel
BuildRequires:  ros-melodic-interactive_markers-devel
BuildRequires:  ros-melodic-moveit_ros_perception-devel
BuildRequires:  ros-melodic-moveit_ros_planning_interface-devel
BuildRequires:  ros-melodic-moveit_ros_robot_interaction-devel
BuildRequires:  ros-melodic-moveit_ros_warehouse-devel
BuildRequires:  ros-melodic-object_recognition_msgs-devel
BuildRequires:  ros-melodic-pluginlib-devel
BuildRequires:  ros-melodic-rosconsole-devel
BuildRequires:  ros-melodic-roscpp-devel
BuildRequires:  ros-melodic-rospy-devel
BuildRequires:  ros-melodic-rostest-devel
BuildRequires:  ros-melodic-rviz-devel
BuildRequires:  ros-melodic-tf2_eigen-devel

Requires:       ros-melodic-geometric_shapes
Requires:       ros-melodic-interactive_markers
Requires:       ros-melodic-moveit_ros_perception
Requires:       ros-melodic-moveit_ros_planning_interface
Requires:       ros-melodic-moveit_ros_robot_interaction
Requires:       ros-melodic-moveit_ros_warehouse
Requires:       ros-melodic-object_recognition_msgs
Requires:       ros-melodic-pluginlib
Requires:       ros-melodic-rosconsole
Requires:       ros-melodic-roscpp
Requires:       ros-melodic-rospy
Requires:       ros-melodic-rviz
Requires:       ros-melodic-tf2_eigen

Provides:  ros-melodic-moveit_ros_visualization = 1.0.2-1
Obsoletes: ros-melodic-moveit_ros_visualization < 1.0.2-1
Obsoletes: ros-kinetic-moveit_ros_visualization


%description
Components of MoveIt! that offer visualization

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       ros-melodic-catkin-devel
Requires:       eigen3-devel
Requires:       fcl-devel
Requires:       ogre-devel
Requires:       poco-devel
Requires:       qt5-qtbase
Requires:       qt5-qtbase-devel
Requires:       tinyxml-devel
Requires:       tinyxml2-devel
Requires:       urdfdom-devel
Requires:       ros-melodic-class_loader-devel
Requires:       ros-melodic-geometric_shapes-devel
Requires:       ros-melodic-interactive_markers-devel
Requires:       ros-melodic-moveit_ros_perception-devel
Requires:       ros-melodic-moveit_ros_planning_interface-devel
Requires:       ros-melodic-moveit_ros_robot_interaction-devel
Requires:       ros-melodic-moveit_ros_warehouse-devel
Requires:       ros-melodic-object_recognition_msgs-devel
Requires:       ros-melodic-pluginlib-devel
Requires:       ros-melodic-rosconsole-devel
Requires:       ros-melodic-roscpp-devel
Requires:       ros-melodic-rospy-devel
Requires:       ros-melodic-rostest-devel
Requires:       ros-melodic-rviz-devel
Requires:       ros-melodic-tf2_eigen-devel

Provides: ros-melodic-moveit_ros_visualization-devel = 1.0.2-1
Obsoletes: ros-melodic-moveit_ros_visualization-devel < 1.0.2-1
Obsoletes: ros-kinetic-moveit_ros_visualization-devel

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
  --pkg moveit_ros_visualization




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
* Wed Jul 24 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.0.2-1
- Update to latest release
* Wed Nov 07 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.9.15-1
- Update to latest release
* Wed May 30 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.9.12-1
- Update to latest release
* Thu Jan 18 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.9.11-1
- Initial package
