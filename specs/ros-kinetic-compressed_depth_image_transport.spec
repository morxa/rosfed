Name:           ros-kinetic-compressed_depth_image_transport
Version:        1.9.5
Release:        3%{?dist}
Summary:        ROS package compressed_depth_image_transport

License:        BSD
URL:            http://www.ros.org/wiki/image_transport_plugins

Source0:        https://github.com/ros-gbp/image_transport_plugins-release/archive/release/kinetic/compressed_depth_image_transport/1.9.5-0.tar.gz#/ros-kinetic-compressed_depth_image_transport-1.9.5-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  opencv-devel
BuildRequires:  poco-devel
BuildRequires:  tinyxml-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-cv_bridge
BuildRequires:  ros-kinetic-dynamic_reconfigure
BuildRequires:  ros-kinetic-image_transport

Requires:       ros-kinetic-cv_bridge
Requires:       ros-kinetic-dynamic_reconfigure
Requires:       ros-kinetic-image_transport

%description
Compressed_depth_image_transport provides a plugin to image_transport
for transparently sending depth images (raw, floating-point) using PNG
compression.


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
  --pkg compressed_depth_image_transport

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
* Thu Nov 23 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.9.5-3
- Build against system opencv3 instead of ros-kinetic-opencv
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.9.5-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.9.5-1
- Update auto-generated Spec file
