Name:           ros-kinetic-opencv3
Version:        3.2.0
Release:        2%{?dist}
Summary:        ROS package opencv3

License:        BSD
URL:            http://opencv.org

Source0:        https://github.com/ros-gbp/opencv3-release/archive/release/kinetic/opencv3/3.2.0-4.tar.gz#/ros-kinetic-opencv3-3.2.0-source0.tar.gz



BuildRequires:  cmake
BuildRequires:  jasper-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng12-devel
BuildRequires:  libtiff
BuildRequires:  libv4l-devel
BuildRequires:  numpy
BuildRequires:  protobuf-devel protobuf-compiler
BuildRequires:  python-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  vtk-qt
BuildRequires:  zlib-devel
BuildRequires:  ros-kinetic-catkin

Requires:       numpy
Requires:       protobuf
Requires:       vtk-qt
Requires:       ros-kinetic-catkin

%description
OpenCV 3.x


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
  --pkg opencv3 \
  --cmake-args -DENABLE_PRECOMPILED_HEADERS=OFF -DWITH_FFMPEG=OFF

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
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 3.2.0-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 3.2.0-1
- Update auto-generated Spec file
