Name:           ros-move_base
Version:        noetic.1.17.2
Release:        1%{?dist}
Summary:        ROS package move_base

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/navigation-release/archive/release/noetic/move_base/1.17.2-1.tar.gz#/ros-noetic-move_base-1.17.2-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel
BuildRequires:  python-unversioned-command

BuildRequires:  libuuid-devel
BuildRequires:  lz4-devel
BuildRequires:  pcl-devel
BuildRequires:  poco-devel
BuildRequires:  tinyxml-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  ros-noetic-actionlib-devel
BuildRequires:  ros-noetic-base_local_planner-devel
BuildRequires:  ros-noetic-catkin-devel
BuildRequires:  ros-noetic-clear_costmap_recovery-devel
BuildRequires:  ros-noetic-cmake_modules-devel
BuildRequires:  ros-noetic-costmap_2d-devel
BuildRequires:  ros-noetic-dynamic_reconfigure-devel
BuildRequires:  ros-noetic-geometry_msgs-devel
BuildRequires:  ros-noetic-message_generation-devel
BuildRequires:  ros-noetic-move_base_msgs-devel
BuildRequires:  ros-noetic-nav_core-devel
BuildRequires:  ros-noetic-nav_msgs-devel
BuildRequires:  ros-noetic-navfn-devel
BuildRequires:  ros-noetic-pluginlib-devel
BuildRequires:  ros-noetic-roscpp-devel
BuildRequires:  ros-noetic-rospy-devel
BuildRequires:  ros-noetic-rotate_recovery-devel
BuildRequires:  ros-noetic-std_srvs-devel
BuildRequires:  ros-noetic-tf2_geometry_msgs-devel
BuildRequires:  ros-noetic-tf2_ros-devel
BuildRequires:  ros-noetic-visualization_msgs-devel

Requires:       ros-noetic-actionlib
Requires:       ros-noetic-base_local_planner
Requires:       ros-noetic-clear_costmap_recovery
Requires:       ros-noetic-costmap_2d
Requires:       ros-noetic-dynamic_reconfigure
Requires:       ros-noetic-geometry_msgs
Requires:       ros-noetic-message_runtime
Requires:       ros-noetic-move_base_msgs
Requires:       ros-noetic-nav_core
Requires:       ros-noetic-nav_msgs
Requires:       ros-noetic-navfn
Requires:       ros-noetic-pluginlib
Requires:       ros-noetic-roscpp
Requires:       ros-noetic-rospy
Requires:       ros-noetic-rotate_recovery
Requires:       ros-noetic-std_srvs
Requires:       ros-noetic-tf2_ros
Requires:       ros-noetic-visualization_msgs

Provides:  ros-noetic-move_base = 1.17.2-1
Obsoletes: ros-noetic-move_base < 1.17.2-1
Obsoletes: ros-kinetic-move_base < 1.17.2-1



%description
The move_base package provides an implementation of an action (see the

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-noetic-catkin-devel
Requires:       libuuid-devel
Requires:       lz4-devel
Requires:       pcl-devel
Requires:       poco-devel
Requires:       tinyxml-devel
Requires:       tinyxml2-devel
Requires:       ros-noetic-actionlib-devel
Requires:       ros-noetic-base_local_planner-devel
Requires:       ros-noetic-clear_costmap_recovery-devel
Requires:       ros-noetic-cmake_modules-devel
Requires:       ros-noetic-costmap_2d-devel
Requires:       ros-noetic-dynamic_reconfigure-devel
Requires:       ros-noetic-geometry_msgs-devel
Requires:       ros-noetic-message_generation-devel
Requires:       ros-noetic-move_base_msgs-devel
Requires:       ros-noetic-nav_core-devel
Requires:       ros-noetic-nav_msgs-devel
Requires:       ros-noetic-navfn-devel
Requires:       ros-noetic-pluginlib-devel
Requires:       ros-noetic-roscpp-devel
Requires:       ros-noetic-rospy-devel
Requires:       ros-noetic-rotate_recovery-devel
Requires:       ros-noetic-std_srvs-devel
Requires:       ros-noetic-tf2_geometry_msgs-devel
Requires:       ros-noetic-tf2_ros-devel
Requires:       ros-noetic-visualization_msgs-devel
Requires:       ros-noetic-message_runtime-devel

Provides: ros-noetic-move_base-devel = 1.17.2-1
Obsoletes: ros-noetic-move_base-devel < 1.17.2-1
Obsoletes: ros-kinetic-move_base-devel < 1.17.2-1


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
  --pkg move_base




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,local_setup*,setup*,env.sh}

touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig,share/move_base/cmake} \
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
* Tue Jun 28 2022 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.17.2-1
- Update to latest release
* Thu Oct 14 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.17.1-3
- Rebuild to pull in updated dependencies
* Tue Feb 23 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.17.1-2
- Modernize python shebang replacement
* Mon Nov 02 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.17.1-1
- Update to latest release
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.17.0-1
- Upgrade to noetic
* Fri Apr 17 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.16.6-1
- Update to latest release
* Thu Mar 05 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.16.4-1
- Update to latest release
* Tue Feb 04 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.16.3-1
- Update to latest release
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
