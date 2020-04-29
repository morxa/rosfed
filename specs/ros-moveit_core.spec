Name:           ros-moveit_core
Version:        melodic.1.0.3
Release:        1%{?dist}
Summary:        ROS package moveit_core

License:        BSD
URL:            http://moveit.ros.org

Source0:        https://github.com/ros-gbp/moveit-release/archive/release/melodic/moveit_core/1.0.3-1.tar.gz#/ros-melodic-moveit_core-1.0.3-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel

BuildRequires:  assimp
BuildRequires:  boost-devel boost-python3-devel boost-python3-devel
BuildRequires:  console-bridge-devel
BuildRequires:  eigen3-devel
BuildRequires:  fcl-devel
BuildRequires:  libccd-devel
BuildRequires:  pkgconfig
BuildRequires:  tinyxml-devel
BuildRequires:  urdfdom-devel
BuildRequires:  urdfdom-headers-devel
BuildRequires:  ros-melodic-angles-devel
BuildRequires:  ros-melodic-catkin-devel
BuildRequires:  ros-melodic-code_coverage-devel
BuildRequires:  ros-melodic-eigen_stl_containers-devel
BuildRequires:  ros-melodic-geometric_shapes-devel
BuildRequires:  ros-melodic-geometry_msgs-devel
BuildRequires:  ros-melodic-kdl_parser-devel
BuildRequires:  ros-melodic-moveit_msgs-devel
BuildRequires:  ros-melodic-moveit_resources-devel
BuildRequires:  ros-melodic-octomap-devel
BuildRequires:  ros-melodic-octomap_msgs-devel
BuildRequires:  ros-melodic-orocos_kdl-devel
BuildRequires:  ros-melodic-random_numbers-devel
BuildRequires:  ros-melodic-rosconsole-devel
BuildRequires:  ros-melodic-roslib-devel
BuildRequires:  ros-melodic-rostime-devel
BuildRequires:  ros-melodic-rosunit-devel
BuildRequires:  ros-melodic-sensor_msgs-devel
BuildRequires:  ros-melodic-shape_msgs-devel
BuildRequires:  ros-melodic-srdfdom-devel
BuildRequires:  ros-melodic-std_msgs-devel
BuildRequires:  ros-melodic-tf2_eigen-devel
BuildRequires:  ros-melodic-tf2_geometry_msgs-devel
BuildRequires:  ros-melodic-tf2_kdl-devel
BuildRequires:  ros-melodic-trajectory_msgs-devel
BuildRequires:  ros-melodic-urdf-devel
BuildRequires:  ros-melodic-visualization_msgs-devel
BuildRequires:  ros-melodic-xmlrpcpp-devel

Requires:       assimp
Requires:       ros-melodic-eigen_stl_containers
Requires:       ros-melodic-geometric_shapes
Requires:       ros-melodic-geometry_msgs
Requires:       ros-melodic-kdl_parser
Requires:       ros-melodic-moveit_msgs
Requires:       ros-melodic-octomap
Requires:       ros-melodic-octomap_msgs
Requires:       ros-melodic-random_numbers
Requires:       ros-melodic-rosconsole
Requires:       ros-melodic-roslib
Requires:       ros-melodic-rostime
Requires:       ros-melodic-sensor_msgs
Requires:       ros-melodic-shape_msgs
Requires:       ros-melodic-srdfdom
Requires:       ros-melodic-std_msgs
Requires:       ros-melodic-tf2_eigen
Requires:       ros-melodic-tf2_geometry_msgs
Requires:       ros-melodic-trajectory_msgs
Requires:       ros-melodic-urdf
Requires:       ros-melodic-visualization_msgs
Requires:       ros-melodic-xmlrpcpp

Provides:  ros-melodic-moveit_core = 1.0.3-1
Obsoletes: ros-melodic-moveit_core < 1.0.3-1
Obsoletes: ros-kinetic-moveit_core < 1.0.3-1


%description
Core libraries used by MoveIt!

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       ros-melodic-catkin-devel
Requires:       assimp
Requires:       boost-devel boost-python3-devel boost-python3-devel
Requires:       console-bridge-devel
Requires:       eigen3-devel
Requires:       fcl-devel
Requires:       libccd-devel
Requires:       tinyxml-devel
Requires:       urdfdom-devel
Requires:       urdfdom-headers-devel
Requires:       ros-melodic-angles-devel
Requires:       ros-melodic-code_coverage-devel
Requires:       ros-melodic-eigen_stl_containers-devel
Requires:       ros-melodic-geometric_shapes-devel
Requires:       ros-melodic-geometry_msgs-devel
Requires:       ros-melodic-kdl_parser-devel
Requires:       ros-melodic-moveit_msgs-devel
Requires:       ros-melodic-moveit_resources-devel
Requires:       ros-melodic-octomap-devel
Requires:       ros-melodic-octomap_msgs-devel
Requires:       ros-melodic-orocos_kdl-devel
Requires:       ros-melodic-random_numbers-devel
Requires:       ros-melodic-rosconsole-devel
Requires:       ros-melodic-roslib-devel
Requires:       ros-melodic-rostime-devel
Requires:       ros-melodic-rosunit-devel
Requires:       ros-melodic-sensor_msgs-devel
Requires:       ros-melodic-shape_msgs-devel
Requires:       ros-melodic-srdfdom-devel
Requires:       ros-melodic-std_msgs-devel
Requires:       ros-melodic-tf2_eigen-devel
Requires:       ros-melodic-tf2_geometry_msgs-devel
Requires:       ros-melodic-tf2_kdl-devel
Requires:       ros-melodic-trajectory_msgs-devel
Requires:       ros-melodic-urdf-devel
Requires:       ros-melodic-visualization_msgs-devel
Requires:       ros-melodic-xmlrpcpp-devel

Provides: ros-melodic-moveit_core-devel = 1.0.3-1
Obsoletes: ros-melodic-moveit_core-devel < 1.0.3-1
Obsoletes: ros-kinetic-moveit_core-devel < 1.0.3-1

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
  --pkg moveit_core




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
* Wed Apr 29 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.0.3-1
- Update to latest release
* Wed Jul 24 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.0.2-1
- Update to latest release
* Wed Nov 07 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.9.15-1
- Update to latest release
* Wed May 30 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.9.12-1
- Update to latest release
* Thu Jan 18 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.9.11-1
- Initial package
