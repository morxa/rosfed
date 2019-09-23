%global pkg_version 1.16.2
Name:           ros-move_base
Version:        melodic.1.16.2
Release:        1%{?dist}
Summary:        ROS package move_base

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/navigation-release/archive/release/melodic/move_base/1.16.2-0.tar.gz#/ros-melodic-move_base-1.16.2-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel

BuildRequires:  libuuid-devel
BuildRequires:  lz4-devel
BuildRequires:  pcl-devel
BuildRequires:  poco-devel
BuildRequires:  tinyxml-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  ros-melodic-actionlib-devel
BuildRequires:  ros-melodic-base_local_planner-devel
BuildRequires:  ros-melodic-catkin-devel
BuildRequires:  ros-melodic-clear_costmap_recovery-devel
BuildRequires:  ros-melodic-cmake_modules-devel
BuildRequires:  ros-melodic-costmap_2d-devel
BuildRequires:  ros-melodic-dynamic_reconfigure-devel
BuildRequires:  ros-melodic-geometry_msgs-devel
BuildRequires:  ros-melodic-message_generation-devel
BuildRequires:  ros-melodic-move_base_msgs-devel
BuildRequires:  ros-melodic-nav_core-devel
BuildRequires:  ros-melodic-nav_msgs-devel
BuildRequires:  ros-melodic-navfn-devel
BuildRequires:  ros-melodic-pluginlib-devel
BuildRequires:  ros-melodic-roscpp-devel
BuildRequires:  ros-melodic-rospy-devel
BuildRequires:  ros-melodic-rotate_recovery-devel
BuildRequires:  ros-melodic-std_srvs-devel
BuildRequires:  ros-melodic-tf2_geometry_msgs-devel
BuildRequires:  ros-melodic-tf2_ros-devel
BuildRequires:  ros-melodic-visualization_msgs-devel

Requires:       ros-melodic-actionlib
Requires:       ros-melodic-base_local_planner
Requires:       ros-melodic-clear_costmap_recovery
Requires:       ros-melodic-costmap_2d
Requires:       ros-melodic-dynamic_reconfigure
Requires:       ros-melodic-geometry_msgs
Requires:       ros-melodic-message_runtime
Requires:       ros-melodic-move_base_msgs
Requires:       ros-melodic-nav_core
Requires:       ros-melodic-nav_msgs
Requires:       ros-melodic-navfn
Requires:       ros-melodic-pluginlib
Requires:       ros-melodic-roscpp
Requires:       ros-melodic-rospy
Requires:       ros-melodic-rotate_recovery
Requires:       ros-melodic-std_srvs
Requires:       ros-melodic-tf2_ros
Requires:       ros-melodic-visualization_msgs

Provides:  ros-melodic-move_base = 1.16.2-1
Obsoletes: ros-melodic-move_base < 1.16.2-1


%description
The move_base package provides an implementation of an action (see the

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-melodic-catkin-devel
Requires:       libuuid-devel
Requires:       lz4-devel
Requires:       pcl-devel
Requires:       poco-devel
Requires:       tinyxml-devel
Requires:       tinyxml2-devel
Requires:       ros-melodic-actionlib-devel
Requires:       ros-melodic-base_local_planner-devel
Requires:       ros-melodic-clear_costmap_recovery-devel
Requires:       ros-melodic-cmake_modules-devel
Requires:       ros-melodic-costmap_2d-devel
Requires:       ros-melodic-dynamic_reconfigure-devel
Requires:       ros-melodic-geometry_msgs-devel
Requires:       ros-melodic-message_generation-devel
Requires:       ros-melodic-move_base_msgs-devel
Requires:       ros-melodic-nav_core-devel
Requires:       ros-melodic-nav_msgs-devel
Requires:       ros-melodic-navfn-devel
Requires:       ros-melodic-pluginlib-devel
Requires:       ros-melodic-roscpp-devel
Requires:       ros-melodic-rospy-devel
Requires:       ros-melodic-rotate_recovery-devel
Requires:       ros-melodic-std_srvs-devel
Requires:       ros-melodic-tf2_geometry_msgs-devel
Requires:       ros-melodic-tf2_ros-devel
Requires:       ros-melodic-visualization_msgs-devel
Requires:       ros-melodic-message_runtime-devel

Provides: ros-melodic-move_base-devel = 1.16.2-1
Obsoletes: ros-melodic-move_base-devel < 1.16.2-1

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
  --pkg move_base




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
* Wed Jul 24 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.16.2-1
- Update to latest release
* Tue Jun 26 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.14.4-1
- Update to latest release
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.14.3-5
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.14.3-4
- devel also requires: the devel package of each run dependency
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.14.3-3
- Also add upstream's exec_depend as Requires:
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.14.3-2
- Add corresponding devel Requires: for the package's BRs and Rs
* Mon May 14 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.14.3-1
- Update to latest release, rebuild for F28
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.14.2-5
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.14.2-4
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.14.2-3
- Add Recommends: for all BRs to the devel subpackage
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.14.2-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.14.2-1
- Update auto-generated Spec file
