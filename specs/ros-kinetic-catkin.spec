Name:           ros-kinetic-catkin
Version:        0.7.6
Release:        2%{?dist}
Summary:        ROS package catkin

License:        BSD
URL:            http://www.ros.org/wiki/catkin

Source0:        https://github.com/ros-gbp/catkin-release/archive/release/kinetic/catkin/0.7.6-0.tar.gz#/ros-kinetic-catkin-0.7.6-source0.tar.gz


BuildArch: noarch

BuildRequires:  cmake
BuildRequires:  gtest-devel
BuildRequires:  python
BuildRequires:  python-catkin_pkg
BuildRequires:  python-empy
BuildRequires:  python-mock
BuildRequires:  python-nose

Requires:       cmake
Requires:       python
Requires:       python-catkin_pkg
Requires:       python-empy
Requires:       python-nose

%description
Low-level build system macros and infrastructure for ROS.


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


mkdir -p %{buildroot}/%{_libdir}/ros/

DESTDIR=%{buildroot} ; export DESTDIR

./bin/catkin_make_isolated \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  --source . \
  --install \
  --install-space %{_libdir}/ros/ \
  --pkg catkin

find %{buildroot}/%{_libdir}/ros/{bin,etc,lib/pkgconfig,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list

find %{buildroot}/%{_libdir}/ros -maxdepth 1 \
  -name .catkin -o -name .rosinstall \
  -o -name "_setup*" -o -name "setup.*" -o -name env.sh \
  | sed -e "s:%{buildroot}/::" -e "s:.py$:.py{,o,c}:" >> files.list

find . -maxdepth 1 -type f -iname "*readme*" | sed "s:^:%%doc :" >> files.list
find . -maxdepth 1 -type f -iname "*license*" | sed "s:^:%%license :" >> files.list


%files -f files.list



%changelog
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.7.6-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.7.6-1
- Update auto-generated Spec file
