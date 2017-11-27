Name:           ros-kinetic-stage
Version:        4.1.1
Release:        2%{?dist}
Summary:        ROS package stage

License:        GPL
URL:            http://rtv.github.com/Stage

Source0:        https://github.com/ros-gbp/stage-release/archive/release/kinetic/stage/4.1.1-1.tar.gz#/ros-kinetic-stage-4.1.1-source0.tar.gz

Patch0: ros-kinetic-stage.string-literal.patch
Patch1: ros-kinetic-stage.abs-ambiguity.patch


# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  cmake
BuildRequires:  fltk-devel
BuildRequires:  gtk2-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libtool libtool-ltdl-devel
BuildRequires:  mesa-libGL-devel mesa-libGLU-devel
BuildRequires:  pkgconfig
BuildRequires:  player-devel
BuildRequires:  ros-kinetic-catkin

Requires:       ros-kinetic-catkin

%description
Mobile robot simulator http://rtv.github.com/Stage


%prep

%setup -c -T
tar --strip-components=1 -xf %{SOURCE0}
%patch0 -p1
%patch1 -p1

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
  --pkg stage

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
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 4.1.1-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 4.1.1-1
- Update auto-generated Spec file
