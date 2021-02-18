Name:           ros-diff_drive_controller
Version:        noetic.0.18.1
Release:        1%{?dist}
Summary:        ROS package diff_drive_controller

License:        BSD
URL:            https://github.com/ros-controls/ros_controllers/wiki

Source0:        https://github.com/ros-gbp/ros_controllers-release/archive/release/noetic/diff_drive_controller/0.18.1-1.tar.gz#/ros-noetic-diff_drive_controller-0.18.1-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel

BuildRequires:  boost-devel boost-python3-devel
BuildRequires:  ros-noetic-catkin-devel
BuildRequires:  ros-noetic-control_msgs-devel
BuildRequires:  ros-noetic-controller_interface-devel
BuildRequires:  ros-noetic-controller_manager-devel
BuildRequires:  ros-noetic-dynamic_reconfigure-devel
BuildRequires:  ros-noetic-geometry_msgs-devel
BuildRequires:  ros-noetic-hardware_interface-devel
BuildRequires:  ros-noetic-nav_msgs-devel
BuildRequires:  ros-noetic-pluginlib-devel
BuildRequires:  ros-noetic-realtime_tools-devel
BuildRequires:  ros-noetic-rosgraph_msgs-devel
BuildRequires:  ros-noetic-rostest-devel
BuildRequires:  ros-noetic-rostopic-devel
BuildRequires:  ros-noetic-std_srvs-devel
BuildRequires:  ros-noetic-tf-devel
BuildRequires:  ros-noetic-urdf-devel
BuildRequires:  ros-noetic-xacro-devel

Requires:       ros-noetic-control_msgs
Requires:       ros-noetic-controller_interface
Requires:       ros-noetic-dynamic_reconfigure
Requires:       ros-noetic-geometry_msgs
Requires:       ros-noetic-hardware_interface
Requires:       ros-noetic-nav_msgs
Requires:       ros-noetic-pluginlib
Requires:       ros-noetic-realtime_tools
Requires:       ros-noetic-tf
Requires:       ros-noetic-urdf

Provides:  ros-noetic-diff_drive_controller = 0.18.1-1
Obsoletes: ros-noetic-diff_drive_controller < 0.18.1-1
Obsoletes: ros-kinetic-diff_drive_controller < 0.18.1-1



%description
Controller for a differential drive mobile base.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       boost-devel boost-python3-devel
Requires:       ros-noetic-catkin-devel
Requires:       ros-noetic-control_msgs-devel
Requires:       ros-noetic-controller_interface-devel
Requires:       ros-noetic-controller_manager-devel
Requires:       ros-noetic-dynamic_reconfigure-devel
Requires:       ros-noetic-geometry_msgs-devel
Requires:       ros-noetic-hardware_interface-devel
Requires:       ros-noetic-nav_msgs-devel
Requires:       ros-noetic-pluginlib-devel
Requires:       ros-noetic-realtime_tools-devel
Requires:       ros-noetic-rosgraph_msgs-devel
Requires:       ros-noetic-rostest-devel
Requires:       ros-noetic-rostopic-devel
Requires:       ros-noetic-std_srvs-devel
Requires:       ros-noetic-tf-devel
Requires:       ros-noetic-urdf-devel
Requires:       ros-noetic-xacro-devel

Provides: ros-noetic-diff_drive_controller-devel = 0.18.1-1
Obsoletes: ros-noetic-diff_drive_controller-devel < 0.18.1-1
Obsoletes: ros-kinetic-diff_drive_controller-devel < 0.18.1-1


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
  --pkg diff_drive_controller




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
* Wed Feb 17 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.18.1-1
- Update to latest release
* Mon Nov 02 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.18.0-1
- Update to latest release
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.17.0-1
- Upgrade to noetic
* Wed Apr 29 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.16.1-1
- Update to latest release
* Fri Apr 17 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.15.1-1
- Update to latest release
* Mon Jul 22 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.15.0-3
- Remove obsolete python2 dependencies
* Sun Jul 21 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.15.0-2
- Switch to python3
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.15.0-1
- Update to ROS melodic release
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.15.0-1
- Update to ROS melodic release
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.15.0-1
- Update to ROS melodic release
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.15.0-1
- Update to ROS melodic release
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.15.0-1
- Update to ROS melodic release
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.15.0-1
- Update to ROS melodic release
