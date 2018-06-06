Name:           ros-kinetic-moveit_commander
Version:        0.9.12
Release:        1%{?dist}
Summary:        ROS package moveit_commander

License:        BSD
URL:            http://moveit.ros.org

Source0:        https://github.com/ros-gbp/moveit-release/archive/release/kinetic/moveit_commander/0.9.12-1.tar.gz#/ros-kinetic-moveit_commander-0.9.12-source0.tar.gz


BuildArch: noarch

# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  python-catkin_pkg
BuildRequires:  python-devel
BuildRequires:  ros-kinetic-catkin-devel
BuildRequires:  ros-kinetic-moveit_resources-devel
BuildRequires:  ros-kinetic-rostest-devel

Requires:       assimp-python
Requires:       ros-kinetic-geometry_msgs
Requires:       ros-kinetic-moveit_msgs
Requires:       ros-kinetic-moveit_ros_planning_interface
Requires:       ros-kinetic-rospy
Requires:       ros-kinetic-sensor_msgs
Requires:       ros-kinetic-shape_msgs
Requires:       ros-kinetic-tf


%description
Python interfaces to MoveIt

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       python-catkin_pkg
Requires:       ros-kinetic-catkin-devel
Requires:       python-devel
Requires:       ros-kinetic-moveit_resources-devel
Requires:       ros-kinetic-rostest-devel
Requires:       ros-kinetic-geometry_msgs-devel
Requires:       ros-kinetic-moveit_msgs-devel
Requires:       ros-kinetic-moveit_ros_planning_interface-devel
Requires:       ros-kinetic-rospy-devel
Requires:       ros-kinetic-sensor_msgs-devel
Requires:       ros-kinetic-shape_msgs-devel
Requires:       ros-kinetic-tf-devel

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
  --pkg moveit_commander




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
* Wed May 30 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.9.12-1
- Update to latest release
* Thu Jan 18 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.9.11-1
- Initial package
