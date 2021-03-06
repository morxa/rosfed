Name:           ros-moveit_ros_perception
Version:        melodic.1.0.3
Release:        1%{?dist}
Summary:        ROS package moveit_ros_perception

License:        BSD
URL:            http://moveit.ros.org

Source0:        https://github.com/ros-gbp/moveit-release/archive/release/melodic/moveit_ros_perception/1.0.3-1.tar.gz#/ros-melodic-moveit_ros_perception-1.0.3-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel

BuildRequires:  eigen3-devel
BuildRequires:  fcl-devel
BuildRequires:  freeglut-devel
BuildRequires:  glew-devel
BuildRequires:  mesa-libGL-devel mesa-libGLU-devel
BuildRequires:  opencv-devel
BuildRequires:  poco-devel
BuildRequires:  tinyxml-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  urdfdom-devel
BuildRequires:  ros-melodic-catkin-devel
BuildRequires:  ros-melodic-cv_bridge-devel
BuildRequires:  ros-melodic-image_transport-devel
BuildRequires:  ros-melodic-message_filters-devel
BuildRequires:  ros-melodic-moveit_core-devel
BuildRequires:  ros-melodic-moveit_msgs-devel
BuildRequires:  ros-melodic-moveit_ros_occupancy_map_monitor-devel
BuildRequires:  ros-melodic-object_recognition_msgs-devel
BuildRequires:  ros-melodic-pluginlib-devel
BuildRequires:  ros-melodic-rosconsole-devel
BuildRequires:  ros-melodic-roscpp-devel
BuildRequires:  ros-melodic-rosunit-devel
BuildRequires:  ros-melodic-sensor_msgs-devel
BuildRequires:  ros-melodic-tf2-devel
BuildRequires:  ros-melodic-tf2_eigen-devel
BuildRequires:  ros-melodic-tf2_geometry_msgs-devel
BuildRequires:  ros-melodic-tf2_ros-devel
BuildRequires:  ros-melodic-urdf-devel

Requires:       ros-melodic-cv_bridge
Requires:       ros-melodic-image_transport
Requires:       ros-melodic-message_filters
Requires:       ros-melodic-moveit_core
Requires:       ros-melodic-moveit_msgs
Requires:       ros-melodic-moveit_ros_occupancy_map_monitor
Requires:       ros-melodic-object_recognition_msgs
Requires:       ros-melodic-pluginlib
Requires:       ros-melodic-rosconsole
Requires:       ros-melodic-roscpp
Requires:       ros-melodic-sensor_msgs
Requires:       ros-melodic-tf2
Requires:       ros-melodic-tf2_eigen
Requires:       ros-melodic-tf2_geometry_msgs
Requires:       ros-melodic-tf2_ros
Requires:       ros-melodic-urdf

Provides:  ros-melodic-moveit_ros_perception = 1.0.3-1
Obsoletes: ros-melodic-moveit_ros_perception < 1.0.3-1
Obsoletes: ros-kinetic-moveit_ros_perception < 1.0.3-1


%description
Components of MoveIt! connecting to perception

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-melodic-catkin-devel
Requires:       eigen3-devel
Requires:       fcl-devel
Requires:       freeglut-devel
Requires:       glew-devel
Requires:       mesa-libGL-devel mesa-libGLU-devel
Requires:       opencv-devel
Requires:       poco-devel
Requires:       tinyxml-devel
Requires:       tinyxml2-devel
Requires:       urdfdom-devel
Requires:       ros-melodic-cv_bridge-devel
Requires:       ros-melodic-image_transport-devel
Requires:       ros-melodic-message_filters-devel
Requires:       ros-melodic-moveit_core-devel
Requires:       ros-melodic-moveit_msgs-devel
Requires:       ros-melodic-moveit_ros_occupancy_map_monitor-devel
Requires:       ros-melodic-object_recognition_msgs-devel
Requires:       ros-melodic-pluginlib-devel
Requires:       ros-melodic-rosconsole-devel
Requires:       ros-melodic-roscpp-devel
Requires:       ros-melodic-rosunit-devel
Requires:       ros-melodic-sensor_msgs-devel
Requires:       ros-melodic-tf2-devel
Requires:       ros-melodic-tf2_eigen-devel
Requires:       ros-melodic-tf2_geometry_msgs-devel
Requires:       ros-melodic-tf2_ros-devel
Requires:       ros-melodic-urdf-devel

Provides: ros-melodic-moveit_ros_perception-devel = 1.0.3-1
Obsoletes: ros-melodic-moveit_ros_perception-devel < 1.0.3-1
Obsoletes: ros-kinetic-moveit_ros_perception-devel < 1.0.3-1

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
  --pkg moveit_ros_perception




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
* Wed Jul 24 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.0.2-1
- Update to latest release
* Wed Nov 07 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.9.15-1
- Update to latest release
* Wed May 30 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.9.12-1
- Update to latest release
* Thu Jan 18 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.9.11-1
- Initial package
