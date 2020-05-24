Name:           ros-ros_core
Version:        noetic.1.5.0
Release:        1%{?dist}
Summary:        ROS package ros_core

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/metapackages-release/archive/release/noetic/ros_core/1.5.0-1.tar.gz#/ros-noetic-ros_core-1.5.0-source0.tar.gz


BuildArch: noarch

# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel

BuildRequires:  ros-noetic-catkin-devel

Requires:       ros-noetic-catkin
Requires:       ros-noetic-class_loader
Requires:       ros-noetic-cmake_modules
Requires:       ros-noetic-common_msgs
Requires:       ros-noetic-gencpp
Requires:       ros-noetic-geneus
Requires:       ros-noetic-genlisp
Requires:       ros-noetic-genmsg
Requires:       ros-noetic-gennodejs
Requires:       ros-noetic-genpy
Requires:       ros-noetic-message_generation
Requires:       ros-noetic-message_runtime
Requires:       ros-noetic-pluginlib
Requires:       ros-noetic-ros
Requires:       ros-noetic-ros_comm
Requires:       ros-noetic-rosbag_migration_rule
Requires:       ros-noetic-rosconsole
Requires:       ros-noetic-rosconsole_bridge
Requires:       ros-noetic-roscpp_core
Requires:       ros-noetic-rosgraph_msgs
Requires:       ros-noetic-roslisp
Requires:       ros-noetic-rospack
Requires:       ros-noetic-std_msgs
Requires:       ros-noetic-std_srvs

Provides:  ros-noetic-ros_core = 1.5.0-1
Obsoletes: ros-noetic-ros_core < 1.5.0-1
Obsoletes: ros-kinetic-ros_core < 1.5.0-1


%description
A metapackage to aggregate the packages required to use publish /
subscribe, services, launch files, and other core ROS concepts.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       ros-noetic-catkin-devel
Requires:       ros-noetic-class_loader-devel
Requires:       ros-noetic-cmake_modules-devel
Requires:       ros-noetic-common_msgs-devel
Requires:       ros-noetic-gencpp-devel
Requires:       ros-noetic-geneus-devel
Requires:       ros-noetic-genlisp-devel
Requires:       ros-noetic-genmsg-devel
Requires:       ros-noetic-gennodejs-devel
Requires:       ros-noetic-genpy-devel
Requires:       ros-noetic-message_generation-devel
Requires:       ros-noetic-message_runtime-devel
Requires:       ros-noetic-pluginlib-devel
Requires:       ros-noetic-ros-devel
Requires:       ros-noetic-ros_comm-devel
Requires:       ros-noetic-rosbag_migration_rule-devel
Requires:       ros-noetic-rosconsole-devel
Requires:       ros-noetic-rosconsole_bridge-devel
Requires:       ros-noetic-roscpp_core-devel
Requires:       ros-noetic-rosgraph_msgs-devel
Requires:       ros-noetic-roslisp-devel
Requires:       ros-noetic-rospack-devel
Requires:       ros-noetic-std_msgs-devel
Requires:       ros-noetic-std_srvs-devel

Provides: ros-noetic-ros_core-devel = 1.5.0-1
Obsoletes: ros-noetic-ros_core-devel < 1.5.0-1
Obsoletes: ros-kinetic-ros_core-devel < 1.5.0-1

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
  --pkg ros_core




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
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.5.0-1
- Upgrade to noetic
* Mon Jul 22 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.4.1-3
- Remove obsolete python2 dependencies
* Sun Jul 21 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.4.1-2
- Switch to python3
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.4.1-1
- Update to ROS melodic release
* Fri Jul 12 2019 Till Hofmann <thofmann@fedoraproject.org> - 1.3.2-4
- Remove ROS distro from package name
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.3.2-3
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.3.2-2
- devel also requires: the devel package of each run dependency
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.3.2-1
- Also add upstream's exec_depend as Requires:
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.3.1-6
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.3.1-5
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.3.1-4
- Add Recommends: for all BRs to the devel subpackage
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.3.1-3
- Split devel package
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.3.1-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.3.1-1
- Update auto-generated Spec file
