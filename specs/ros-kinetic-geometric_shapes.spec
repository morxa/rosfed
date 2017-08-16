Name:           ros-kinetic-geometric_shapes
Version:        0.5.2
Release:        1%{?dist}
Summary:        ROS package geometric_shapes

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/geometric_shapes-release/archive/release/kinetic/geometric_shapes/0.5.2-0.tar.gz#/ros-kinetic-geometric_shapes-0.5.2-source0.tar.gz



BuildRequires:  assimp-devel
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  eigen3-devel
BuildRequires:  pkgconfig
BuildRequires:  qhull-devel
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-eigen_stl_containers
BuildRequires:  ros-kinetic-octomap
BuildRequires:  ros-kinetic-random_numbers
BuildRequires:  ros-kinetic-resource_retriever
BuildRequires:  ros-kinetic-rosunit
BuildRequires:  ros-kinetic-shape_msgs
BuildRequires:  ros-kinetic-visualization_msgs

Requires:       assimp
Requires:       boost-devel
Requires:       console-bridge-devel
Requires:       eigen3-devel
Requires:       qhull-devel
Requires:       ros-kinetic-eigen_stl_containers
Requires:       ros-kinetic-octomap
Requires:       ros-kinetic-random_numbers
Requires:       ros-kinetic-resource_retriever
Requires:       ros-kinetic-shape_msgs
Requires:       ros-kinetic-visualization_msgs

%description
This package contains generic definitions of geometric shapes and
bodies.


%prep

%setup -c -T
tar --strip-components=1 -xf %{SOURCE0}

%build
# nothing to do here


%install
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
FFLAGS="${FFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FFLAGS ; \
FCFLAGS="${FCFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FCFLAGS ; \
%{?__global_ldflags:LDFLAGS="${LDFLAGS:-%__global_ldflags}" ; export LDFLAGS ;} \


source %{_libdir}/ros/setup.bash

DESTDIR=%{buildroot} ; export DESTDIR

catkin_make_isolated \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  --source . \
  --install \
  --install-space %{_libdir}/ros/ \
  --pkg geometric_shapes

rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,setup*,env.sh}

find %{buildroot}/%{_libdir}/ros/{bin,etc,include,lib/pkgconfig,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list


find . -maxdepth 1 -type f -iname "*readme*" | sed "s:^:%%doc :" >> files.list
find . -maxdepth 1 -type f -iname "*license*" | sed "s:^:%%license :" >> files.list

%files -f files.list



%changelog
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.5.2-1
- Update auto-generated Spec file
