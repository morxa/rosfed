Name:           ros-gazebo_ros_control
Version:        noetic.2.9.2
Release:        3%{?dist}
Summary:        ROS package gazebo_ros_control

License:        BSD
URL:            http://ros.org/wiki/gazebo_ros_control

Source0:        https://github.com/ros-gbp/gazebo_ros_pkgs-release/archive/release/noetic/gazebo_ros_control/2.9.2-1.tar.gz#/ros-noetic-gazebo_ros_control-2.9.2-source0.tar.gz

Patch0: ros-gazebo_ros_control.build-with-cpp17.patch


# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel
BuildRequires:  python-unversioned-command

BuildRequires:  bullet-devel
BuildRequires:  gazebo-devel
BuildRequires:  libuuid-devel
BuildRequires:  opencv-devel
BuildRequires:  poco-devel
BuildRequires:  tinyxml-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  urdfdom-devel
BuildRequires:  ros-noetic-angles-devel
BuildRequires:  ros-noetic-catkin-devel
BuildRequires:  ros-noetic-control_toolbox-devel
BuildRequires:  ros-noetic-controller_manager-devel
BuildRequires:  ros-noetic-gazebo_dev-devel
BuildRequires:  ros-noetic-hardware_interface-devel
BuildRequires:  ros-noetic-joint_limits_interface-devel
BuildRequires:  ros-noetic-pluginlib-devel
BuildRequires:  ros-noetic-roscpp-devel
BuildRequires:  ros-noetic-std_msgs-devel
BuildRequires:  ros-noetic-transmission_interface-devel
BuildRequires:  ros-noetic-urdf-devel

Requires:       ros-noetic-angles
Requires:       ros-noetic-control_toolbox
Requires:       ros-noetic-controller_manager
Requires:       ros-noetic-gazebo_ros
Requires:       ros-noetic-hardware_interface
Requires:       ros-noetic-joint_limits_interface
Requires:       ros-noetic-pluginlib
Requires:       ros-noetic-roscpp
Requires:       ros-noetic-std_msgs
Requires:       ros-noetic-transmission_interface
Requires:       ros-noetic-urdf

Provides:  ros-noetic-gazebo_ros_control = 2.9.2-3
Obsoletes: ros-noetic-gazebo_ros_control < 2.9.2-3
Obsoletes: ros-kinetic-gazebo_ros_control < 2.9.2-3



%description
gazebo_ros_control

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
Requires:       ros-noetic-control_toolbox-devel
Requires:       ros-noetic-controller_manager-devel
Requires:       ros-noetic-gazebo_dev-devel
Requires:       ros-noetic-hardware_interface-devel
Requires:       ros-noetic-joint_limits_interface-devel
Requires:       ros-noetic-pluginlib-devel
Requires:       ros-noetic-roscpp-devel
Requires:       ros-noetic-std_msgs-devel
Requires:       ros-noetic-transmission_interface-devel
Requires:       ros-noetic-urdf-devel
Requires:       ros-noetic-gazebo_ros-devel

Provides: ros-noetic-gazebo_ros_control-devel = 2.9.2-3
Obsoletes: ros-noetic-gazebo_ros_control-devel < 2.9.2-3
Obsoletes: ros-kinetic-gazebo_ros_control-devel < 2.9.2-3


%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.



%prep

%setup -c -T
tar --strip-components=1 -xf %{SOURCE0}
%patch0 -p1

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
  --pkg gazebo_ros_control




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,local_setup*,setup*,env.sh}

touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig,share/gazebo_ros_control/cmake} \
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
* Mon Dec 26 2022 Tarik Viehmann <viehmann@kbsg.rwth-aachen.de> - noetic.2.9.2-3
- Build with c++17 for log4cxx 0.13
* Thu Oct 14 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.2.9.2-2
- Rebuild to pull in updated dependencies
* Mon May 17 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.2.9.2-1
- Update to latest release
* Tue Feb 23 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.2.9.1-2
- Modernize python shebang replacement
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
* Fri Jan 19 2018 Tim Niemueller <tim@niemueller.de> - 2.5.14-1
- Initial package
