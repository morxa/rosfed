Name:           ros-gazebo_ros_control
Version:        melodic.2.8.6
Release:        1%{?dist}
Summary:        ROS package gazebo_ros_control

License:        BSD
URL:            http://ros.org/wiki/gazebo_ros_control

Source0:        https://github.com/ros-gbp/gazebo_ros_pkgs-release/archive/release/melodic/gazebo_ros_control/2.8.6-1.tar.gz#/ros-melodic-gazebo_ros_control-2.8.6-source0.tar.gz



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
BuildRequires:  ros-melodic-catkin-devel
BuildRequires:  ros-melodic-control_toolbox-devel
BuildRequires:  ros-melodic-controller_manager-devel
BuildRequires:  ros-melodic-gazebo_dev-devel
BuildRequires:  ros-melodic-hardware_interface-devel
BuildRequires:  ros-melodic-joint_limits_interface-devel
BuildRequires:  ros-melodic-pluginlib-devel
BuildRequires:  ros-melodic-roscpp-devel
BuildRequires:  ros-melodic-std_msgs-devel
BuildRequires:  ros-melodic-transmission_interface-devel
BuildRequires:  ros-melodic-urdf-devel

Requires:       ros-melodic-angles
Requires:       ros-melodic-control_toolbox
Requires:       ros-melodic-controller_manager
Requires:       ros-melodic-gazebo_ros
Requires:       ros-melodic-hardware_interface
Requires:       ros-melodic-joint_limits_interface
Requires:       ros-melodic-pluginlib
Requires:       ros-melodic-roscpp
Requires:       ros-melodic-std_msgs
Requires:       ros-melodic-transmission_interface
Requires:       ros-melodic-urdf

Provides:  ros-melodic-gazebo_ros_control = 2.8.6-1
Obsoletes: ros-melodic-gazebo_ros_control < 2.8.6-1
Obsoletes: ros-kinetic-gazebo_ros_control < 2.8.6-1


%description
gazebo_ros_control

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
Requires:       ros-melodic-control_toolbox-devel
Requires:       ros-melodic-controller_manager-devel
Requires:       ros-melodic-gazebo_dev-devel
Requires:       ros-melodic-hardware_interface-devel
Requires:       ros-melodic-joint_limits_interface-devel
Requires:       ros-melodic-pluginlib-devel
Requires:       ros-melodic-roscpp-devel
Requires:       ros-melodic-std_msgs-devel
Requires:       ros-melodic-transmission_interface-devel
Requires:       ros-melodic-urdf-devel
Requires:       ros-melodic-gazebo_ros-devel

Provides: ros-melodic-gazebo_ros_control-devel = 2.8.6-1
Obsoletes: ros-melodic-gazebo_ros_control-devel < 2.8.6-1
Obsoletes: ros-kinetic-gazebo_ros_control-devel < 2.8.6-1

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
  --pkg gazebo_ros_control




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
* Fri Jan 19 2018 Tim Niemueller <tim@niemueller.de> - 2.5.14-1
- Initial package
