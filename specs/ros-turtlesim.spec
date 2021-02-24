Name:           ros-turtlesim
Version:        noetic.0.10.2
Release:        2%{?dist}
Summary:        ROS package turtlesim

License:        BSD
URL:            http://www.ros.org/wiki/turtlesim

Source0:        https://github.com/ros-gbp/ros_tutorials-release/archive/release/noetic/turtlesim/0.10.2-1.tar.gz#/ros-noetic-turtlesim-0.10.2-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel
BuildRequires:  python-unversioned-command

BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  log4cxx-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  tinyxml-devel
BuildRequires:  ros-noetic-catkin-devel
BuildRequires:  ros-noetic-geometry_msgs-devel
BuildRequires:  ros-noetic-message_generation-devel
BuildRequires:  ros-noetic-rosconsole-devel
BuildRequires:  ros-noetic-roscpp-devel
BuildRequires:  ros-noetic-roscpp_serialization-devel
BuildRequires:  ros-noetic-roslib-devel
BuildRequires:  ros-noetic-rostime-devel
BuildRequires:  ros-noetic-std_msgs-devel
BuildRequires:  ros-noetic-std_srvs-devel

Requires:       qt5-qtbase
Requires:       qt5-qtbase-gui
Requires:       ros-noetic-geometry_msgs
Requires:       ros-noetic-message_runtime
Requires:       ros-noetic-rosconsole
Requires:       ros-noetic-roscpp
Requires:       ros-noetic-roscpp_serialization
Requires:       ros-noetic-roslib
Requires:       ros-noetic-rostime
Requires:       ros-noetic-std_msgs
Requires:       ros-noetic-std_srvs

Provides:  ros-noetic-turtlesim = 0.10.2-2
Obsoletes: ros-noetic-turtlesim < 0.10.2-2
Obsoletes: ros-kinetic-turtlesim < 0.10.2-2



%description
turtlesim is a tool made for teaching ROS and ROS packages.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-noetic-catkin-devel
Requires:       boost-devel
Requires:       console-bridge-devel
Requires:       log4cxx-devel
Requires:       qt5-qtbase-devel
Requires:       tinyxml-devel
Requires:       ros-noetic-geometry_msgs-devel
Requires:       ros-noetic-message_generation-devel
Requires:       ros-noetic-rosconsole-devel
Requires:       ros-noetic-roscpp-devel
Requires:       ros-noetic-roscpp_serialization-devel
Requires:       ros-noetic-roslib-devel
Requires:       ros-noetic-rostime-devel
Requires:       ros-noetic-std_msgs-devel
Requires:       ros-noetic-std_srvs-devel
Requires:       ros-noetic-message_runtime-devel

Provides: ros-noetic-turtlesim-devel = 0.10.2-2
Obsoletes: ros-noetic-turtlesim-devel < 0.10.2-2
Obsoletes: ros-kinetic-turtlesim-devel < 0.10.2-2


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
  --pkg turtlesim




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,local_setup*,setup*,env.sh}

touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig,share/turtlesim/cmake} \
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
* Tue Feb 23 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.10.2-2
- Modernize python shebang replacement
* Mon Nov 02 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.10.2-1
- Update to latest release
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.10.1-1
- Upgrade to noetic
* Wed Mar 04 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.9.2-1
- Update to latest release
* Mon Jul 22 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.9.1-3
- Remove obsolete python2 dependencies
* Sun Jul 21 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.9.1-2
- Switch to python3
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.9.1-1
- Update to ROS melodic release
* Fri Jul 12 2019 Till Hofmann <thofmann@fedoraproject.org> - 0.7.1-10
- Remove ROS distro from package name
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.7.1-9
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.7.1-8
- devel also requires: the devel package of each run dependency
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.7.1-7
- Also add upstream's exec_depend as Requires:
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.7.1-6
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.7.1-5
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.7.1-4
- Add Recommends: for all BRs to the devel subpackage
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.7.1-3
- Split devel package
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.7.1-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.7.1-1
- Update auto-generated Spec file
