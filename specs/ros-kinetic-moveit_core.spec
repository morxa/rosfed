Name:           ros-kinetic-moveit_core
Version:        0.9.15
Release:        1%{?dist}
Summary:        ROS package moveit_core

License:        BSD
URL:            http://moveit.ros.org

Source0:        https://github.com/ros-gbp/moveit-release/archive/release/kinetic/moveit_core/0.9.15-0.tar.gz#/ros-kinetic-moveit_core-0.9.15-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  assimp
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  eigen3-devel
BuildRequires:  fcl-devel
BuildRequires:  libccd-devel
BuildRequires:  pkgconfig
BuildRequires:  tinyxml-devel
BuildRequires:  urdfdom-devel
BuildRequires:  urdfdom-headers-devel
BuildRequires:  ros-kinetic-angles-devel
BuildRequires:  ros-kinetic-catkin-devel
BuildRequires:  ros-kinetic-eigen_conversions-devel
BuildRequires:  ros-kinetic-eigen_stl_containers-devel
BuildRequires:  ros-kinetic-geometric_shapes-devel
BuildRequires:  ros-kinetic-geometry_msgs-devel
BuildRequires:  ros-kinetic-kdl_parser-devel
BuildRequires:  ros-kinetic-moveit_msgs-devel
BuildRequires:  ros-kinetic-moveit_resources-devel
BuildRequires:  ros-kinetic-octomap-devel
BuildRequires:  ros-kinetic-octomap_msgs-devel
BuildRequires:  ros-kinetic-orocos_kdl-devel
BuildRequires:  ros-kinetic-random_numbers-devel
BuildRequires:  ros-kinetic-rosconsole-devel
BuildRequires:  ros-kinetic-roslib-devel
BuildRequires:  ros-kinetic-rostime-devel
BuildRequires:  ros-kinetic-rosunit-devel
BuildRequires:  ros-kinetic-sensor_msgs-devel
BuildRequires:  ros-kinetic-shape_msgs-devel
BuildRequires:  ros-kinetic-srdfdom-devel
BuildRequires:  ros-kinetic-std_msgs-devel
BuildRequires:  ros-kinetic-tf_conversions-devel
BuildRequires:  ros-kinetic-trajectory_msgs-devel
BuildRequires:  ros-kinetic-urdf-devel
BuildRequires:  ros-kinetic-visualization_msgs-devel

Requires:       assimp
Requires:       ros-kinetic-eigen_conversions
Requires:       ros-kinetic-eigen_stl_containers
Requires:       ros-kinetic-geometric_shapes
Requires:       ros-kinetic-geometry_msgs
Requires:       ros-kinetic-kdl_parser
Requires:       ros-kinetic-moveit_msgs
Requires:       ros-kinetic-octomap
Requires:       ros-kinetic-octomap_msgs
Requires:       ros-kinetic-random_numbers
Requires:       ros-kinetic-rosconsole
Requires:       ros-kinetic-rostime
Requires:       ros-kinetic-sensor_msgs
Requires:       ros-kinetic-srdfdom
Requires:       ros-kinetic-std_msgs
Requires:       ros-kinetic-trajectory_msgs
Requires:       ros-kinetic-urdf
Requires:       ros-kinetic-visualization_msgs


%description
Core libraries used by MoveIt!

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       ros-kinetic-catkin-devel
Requires:       assimp
Requires:       boost-devel
Requires:       console-bridge-devel
Requires:       eigen3-devel
Requires:       fcl-devel
Requires:       libccd-devel
Requires:       tinyxml-devel
Requires:       urdfdom-devel
Requires:       urdfdom-headers-devel
Requires:       ros-kinetic-angles-devel
Requires:       ros-kinetic-eigen_conversions-devel
Requires:       ros-kinetic-eigen_stl_containers-devel
Requires:       ros-kinetic-geometric_shapes-devel
Requires:       ros-kinetic-geometry_msgs-devel
Requires:       ros-kinetic-kdl_parser-devel
Requires:       ros-kinetic-moveit_msgs-devel
Requires:       ros-kinetic-moveit_resources-devel
Requires:       ros-kinetic-octomap-devel
Requires:       ros-kinetic-octomap_msgs-devel
Requires:       ros-kinetic-orocos_kdl-devel
Requires:       ros-kinetic-random_numbers-devel
Requires:       ros-kinetic-rosconsole-devel
Requires:       ros-kinetic-roslib-devel
Requires:       ros-kinetic-rostime-devel
Requires:       ros-kinetic-rosunit-devel
Requires:       ros-kinetic-sensor_msgs-devel
Requires:       ros-kinetic-shape_msgs-devel
Requires:       ros-kinetic-srdfdom-devel
Requires:       ros-kinetic-std_msgs-devel
Requires:       ros-kinetic-tf_conversions-devel
Requires:       ros-kinetic-trajectory_msgs-devel
Requires:       ros-kinetic-urdf-devel
Requires:       ros-kinetic-visualization_msgs-devel

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
  --pkg moveit_core




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



# replace unversioned python shebang
for file in $(grep -rIl '^#!.*python\s*$') ; do
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
* Wed Nov 07 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.9.15-1
- Update to latest release
* Wed May 30 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.9.12-1
- Update to latest release
* Thu Jan 18 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.9.11-1
- Initial package
