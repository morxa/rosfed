%global pkg_version 0.15.1
Name:           ros-ros_control
Version:        melodic.0.15.1
Release:        1%{?dist}
Summary:        ROS package ros_control

License:        BSD
URL:            http://ros.org/wiki/ros_control

Source0:        https://github.com/ros-gbp/ros_control-release/archive/release/melodic/ros_control/0.15.1-0.tar.gz#/ros-melodic-ros_control-0.15.1-source0.tar.gz


BuildArch: noarch

# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel

BuildRequires:  ros-melodic-catkin-devel

Requires:       ros-melodic-combined_robot_hw
Requires:       ros-melodic-combined_robot_hw_tests
Requires:       ros-melodic-controller_interface
Requires:       ros-melodic-controller_manager
Requires:       ros-melodic-controller_manager_msgs
Requires:       ros-melodic-controller_manager_tests
Requires:       ros-melodic-hardware_interface
Requires:       ros-melodic-joint_limits_interface
Requires:       ros-melodic-realtime_tools
Requires:       ros-melodic-transmission_interface

Provides:  ros-melodic-ros_control = 0.15.1-1
Obsoletes: ros-melodic-ros_control < 0.15.1-1


%description
A set of packages that include controller interfaces, controller
managers, transmissions and hardware_interfaces.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       ros-melodic-catkin-devel
Requires:       ros-melodic-combined_robot_hw-devel
Requires:       ros-melodic-combined_robot_hw_tests-devel
Requires:       ros-melodic-controller_interface-devel
Requires:       ros-melodic-controller_manager-devel
Requires:       ros-melodic-controller_manager_msgs-devel
Requires:       ros-melodic-controller_manager_tests-devel
Requires:       ros-melodic-hardware_interface-devel
Requires:       ros-melodic-joint_limits_interface-devel
Requires:       ros-melodic-realtime_tools-devel
Requires:       ros-melodic-transmission_interface-devel

Provides: ros-melodic-ros_control-devel = 0.15.1-1
Obsoletes: ros-melodic-ros_control-devel < 0.15.1-1

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
  --pkg ros_control




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
install -p -D -t %{buildroot}/%{_docdir}/%{name} README_FEDORA
echo %{_docdir}/%{name} >> files.list
install -p -D -t %{buildroot}/%{_docdir}/%{name}-devel README_FEDORA
echo %{_docdir}/%{name}-devel >> files_devel.list


%files -f files.list
%files devel -f files_devel.list


%changelog
* Wed Jul 24 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.15.1-1
- Update to latest release
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.13.3-1
- Update to latest release
* Thu Jan 18 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.13.0-1
- Initial package
