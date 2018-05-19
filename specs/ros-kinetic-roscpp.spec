Name:           ros-kinetic-roscpp
Version:        1.12.13
Release:        3%{?dist}
Summary:        ROS package roscpp

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/ros_comm-release/archive/release/kinetic/roscpp/1.12.13-0.tar.gz#/ros-kinetic-roscpp-1.12.13-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  log4cxx-devel
BuildRequires:  pkgconfig
BuildRequires:  ros-kinetic-catkin-devel
BuildRequires:  ros-kinetic-cpp_common-devel
BuildRequires:  ros-kinetic-message_generation-devel
BuildRequires:  ros-kinetic-rosconsole-devel
BuildRequires:  ros-kinetic-roscpp_serialization-devel
BuildRequires:  ros-kinetic-roscpp_traits-devel
BuildRequires:  ros-kinetic-rosgraph_msgs-devel
BuildRequires:  ros-kinetic-roslang-devel
BuildRequires:  ros-kinetic-rostime-devel
BuildRequires:  ros-kinetic-std_msgs-devel
BuildRequires:  ros-kinetic-xmlrpcpp-devel

Requires:       ros-kinetic-cpp_common
Requires:       ros-kinetic-message_runtime
Requires:       ros-kinetic-rosconsole
Requires:       ros-kinetic-roscpp_serialization
Requires:       ros-kinetic-roscpp_traits
Requires:       ros-kinetic-rosgraph_msgs
Requires:       ros-kinetic-rostime
Requires:       ros-kinetic-std_msgs
Requires:       ros-kinetic-xmlrpcpp


%description
roscpp is a C++ implementation of ROS. It provides a

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-kinetic-catkin-devel
Requires:       boost-devel
Requires:       console-bridge-devel
Requires:       log4cxx-devel
Requires:       pkgconfig
Requires:       ros-kinetic-cpp_common-devel
Requires:       ros-kinetic-message_generation-devel
Requires:       ros-kinetic-rosconsole-devel
Requires:       ros-kinetic-roscpp_serialization-devel
Requires:       ros-kinetic-roscpp_traits-devel
Requires:       ros-kinetic-rosgraph_msgs-devel
Requires:       ros-kinetic-roslang-devel
Requires:       ros-kinetic-rostime-devel
Requires:       ros-kinetic-std_msgs-devel
Requires:       ros-kinetic-xmlrpcpp-devel

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
  --pkg roscpp




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
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.13-3
- Also add upstream's exec_depend as Requires:
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.13-2
- Add corresponding devel Requires: for the package's BRs and Rs
* Mon May 14 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.13-1
- Update to latest release, rebuild for F28
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.12-7
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.12-6
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.12-5
- Add Recommends: for all BRs to the devel subpackage
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.12-4
- Split devel package
* Mon Nov 20 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.12.12-3
- Add missing BR on log4cxx-devel
* Mon Nov 20 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.12.12-2
- Add missing BR on boost-devel
* Sun Nov 19 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.12.12-1
- Update to latest release
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.12.7-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.12.7-1
- Update auto-generated Spec file
