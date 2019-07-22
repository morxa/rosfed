Name:           ros-ros_core
Version:        melodic.1.4.1
Release:        1%{?dist}
Summary:        ROS package ros_core

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/metapackages-release/archive/release/melodic/ros_core/1.4.1-0.tar.gz#/ros-melodic-ros_core-1.4.1-source0.tar.gz


BuildArch: noarch

# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  ros-melodic-catkin-devel

Requires:       ros-melodic-catkin
Requires:       ros-melodic-class_loader
Requires:       ros-melodic-cmake_modules
Requires:       ros-melodic-common_msgs
Requires:       ros-melodic-gencpp
Requires:       ros-melodic-geneus
Requires:       ros-melodic-genlisp
Requires:       ros-melodic-genmsg
Requires:       ros-melodic-gennodejs
Requires:       ros-melodic-genpy
Requires:       ros-melodic-message_generation
Requires:       ros-melodic-message_runtime
Requires:       ros-melodic-pluginlib
Requires:       ros-melodic-ros
Requires:       ros-melodic-ros_comm
Requires:       ros-melodic-rosbag_migration_rule
Requires:       ros-melodic-rosconsole
Requires:       ros-melodic-rosconsole_bridge
Requires:       ros-melodic-roscpp_core
Requires:       ros-melodic-rosgraph_msgs
Requires:       ros-melodic-roslisp
Requires:       ros-melodic-rospack
Requires:       ros-melodic-std_msgs
Requires:       ros-melodic-std_srvs

Provides:  ros-melodic-ros_core = 1.4.1-1
Obsoletes: ros-melodic-ros_core < 1.4.1-1


%description
A metapackage to aggregate the packages required to use publish /
subscribe, services, launch files, and other core ROS concepts.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       ros-melodic-catkin-devel
Requires:       ros-melodic-class_loader-devel
Requires:       ros-melodic-cmake_modules-devel
Requires:       ros-melodic-common_msgs-devel
Requires:       ros-melodic-gencpp-devel
Requires:       ros-melodic-geneus-devel
Requires:       ros-melodic-genlisp-devel
Requires:       ros-melodic-genmsg-devel
Requires:       ros-melodic-gennodejs-devel
Requires:       ros-melodic-genpy-devel
Requires:       ros-melodic-message_generation-devel
Requires:       ros-melodic-message_runtime-devel
Requires:       ros-melodic-pluginlib-devel
Requires:       ros-melodic-ros-devel
Requires:       ros-melodic-ros_comm-devel
Requires:       ros-melodic-rosbag_migration_rule-devel
Requires:       ros-melodic-rosconsole-devel
Requires:       ros-melodic-rosconsole_bridge-devel
Requires:       ros-melodic-roscpp_core-devel
Requires:       ros-melodic-rosgraph_msgs-devel
Requires:       ros-melodic-roslisp-devel
Requires:       ros-melodic-rospack-devel
Requires:       ros-melodic-std_msgs-devel
Requires:       ros-melodic-std_srvs-devel

Provides: ros-melodic-ros_core-devel = 1.4.1-1
Obsoletes: ros-melodic-ros_core-devel < 1.4.1-1

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

DESTDIR=%{buildroot} ; export DESTDIR


catkin_make_isolated \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCATKIN_ENABLE_TESTING=OFF \
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



# replace unversioned python shebang
for file in $(grep -rIl '^#!.*python\s*$' %{buildroot}) ; do
  sed -i.orig '/^#!.*python\s*$/ { s/python/python2/ }' $file
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