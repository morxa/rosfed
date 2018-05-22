Name:           ros-kinetic-ros_core
Version:        1.3.2
Release:        3%{?dist}
Summary:        ROS package ros_core

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/metapackages-release/archive/release/kinetic/ros_core/1.3.2-0.tar.gz#/ros-kinetic-ros_core-1.3.2-source0.tar.gz


BuildArch: noarch

# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  ros-kinetic-catkin-devel

Requires:       ros-kinetic-catkin
Requires:       ros-kinetic-cmake_modules
Requires:       ros-kinetic-common_msgs
Requires:       ros-kinetic-gencpp
Requires:       ros-kinetic-geneus
Requires:       ros-kinetic-genlisp
Requires:       ros-kinetic-genmsg
Requires:       ros-kinetic-gennodejs
Requires:       ros-kinetic-genpy
Requires:       ros-kinetic-message_generation
Requires:       ros-kinetic-message_runtime
Requires:       ros-kinetic-ros
Requires:       ros-kinetic-ros_comm
Requires:       ros-kinetic-rosbag_migration_rule
Requires:       ros-kinetic-rosconsole_bridge
Requires:       ros-kinetic-roscpp_core
Requires:       ros-kinetic-rosgraph_msgs
Requires:       ros-kinetic-roslisp
Requires:       ros-kinetic-rospack
Requires:       ros-kinetic-std_msgs
Requires:       ros-kinetic-std_srvs


%description
A metapackage to aggregate the packages required to use publish /
subscribe, services, launch files, and other core ROS concepts.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       ros-kinetic-catkin-devel
Requires:       ros-kinetic-cmake_modules-devel
Requires:       ros-kinetic-common_msgs-devel
Requires:       ros-kinetic-gencpp-devel
Requires:       ros-kinetic-geneus-devel
Requires:       ros-kinetic-genlisp-devel
Requires:       ros-kinetic-genmsg-devel
Requires:       ros-kinetic-gennodejs-devel
Requires:       ros-kinetic-genpy-devel
Requires:       ros-kinetic-message_generation-devel
Requires:       ros-kinetic-message_runtime-devel
Requires:       ros-kinetic-ros-devel
Requires:       ros-kinetic-ros_comm-devel
Requires:       ros-kinetic-rosbag_migration_rule-devel
Requires:       ros-kinetic-rosconsole_bridge-devel
Requires:       ros-kinetic-roscpp_core-devel
Requires:       ros-kinetic-rosgraph_msgs-devel
Requires:       ros-kinetic-roslisp-devel
Requires:       ros-kinetic-rospack-devel
Requires:       ros-kinetic-std_msgs-devel
Requires:       ros-kinetic-std_srvs-devel

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




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,setup*,env.sh}

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


echo "This is a package automatically generated with rosfed." >> README_FEDORA
echo "See https://pagure.io/ros for more information." >> README_FEDORA
install -p -D -t %{buildroot}/%{_docdir}/%{name} README_FEDORA
echo %{_docdir}/%{name} >> files.list
install -p -D -t %{buildroot}/%{_docdir}/%{name}-devel README_FEDORA
echo %{_docdir}/%{name}-devel >> files_devel.list


%files -f files.list
%files devel -f files_devel.list


%changelog
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
