Name:           ros-kinetic-geometric_shapes
Version:        0.5.4
Release:        1%{?dist}
Summary:        ROS package geometric_shapes

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/geometric_shapes-release/archive/release/kinetic/geometric_shapes/0.5.4-1.tar.gz#/ros-kinetic-geometric_shapes-0.5.4-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  assimp-devel
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  eigen3-devel
BuildRequires:  gtest-devel
BuildRequires:  pkgconfig
BuildRequires:  qhull-devel
BuildRequires:  ros-kinetic-catkin-devel
BuildRequires:  ros-kinetic-eigen_stl_containers-devel
BuildRequires:  ros-kinetic-octomap-devel
BuildRequires:  ros-kinetic-random_numbers-devel
BuildRequires:  ros-kinetic-resource_retriever-devel
BuildRequires:  ros-kinetic-roscpp_serialization-devel
BuildRequires:  ros-kinetic-rosunit-devel
BuildRequires:  ros-kinetic-shape_msgs-devel
BuildRequires:  ros-kinetic-visualization_msgs-devel

Requires:       assimp
Requires:       ros-kinetic-eigen_stl_containers
Requires:       ros-kinetic-octomap
Requires:       ros-kinetic-random_numbers
Requires:       ros-kinetic-resource_retriever
Requires:       ros-kinetic-shape_msgs
Requires:       ros-kinetic-visualization_msgs


%description
This package contains generic definitions of geometric shapes and
bodies.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-kinetic-catkin-devel
Requires:       assimp-devel
Requires:       boost-devel
Requires:       console-bridge-devel
Requires:       eigen3-devel
Requires:       gtest-devel
Requires:       pkgconfig
Requires:       qhull-devel
Requires:       ros-kinetic-eigen_stl_containers-devel
Requires:       ros-kinetic-octomap-devel
Requires:       ros-kinetic-random_numbers-devel
Requires:       ros-kinetic-resource_retriever-devel
Requires:       ros-kinetic-roscpp_serialization-devel
Requires:       ros-kinetic-rosunit-devel
Requires:       ros-kinetic-shape_msgs-devel
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
  --pkg geometric_shapes




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
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.5.4-1
- Also add upstream's exec_depend as Requires:
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.5.3-4
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.5.3-3
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.5.3-2
- Add Recommends: for all BRs to the devel subpackage
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.5.3-1
- Split devel package
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.5.2-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.5.2-1
- Update auto-generated Spec file
