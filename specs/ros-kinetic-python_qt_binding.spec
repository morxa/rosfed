Name:           ros-kinetic-python_qt_binding
Version:        0.3.3
Release:        1%{?dist}
Summary:        ROS package python_qt_binding

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/python_qt_binding-release/archive/release/kinetic/python_qt_binding/0.3.3-0.tar.gz#/ros-kinetic-python_qt_binding-0.3.3-source0.tar.gz


BuildArch: noarch

BuildRequires:  python-qt5 sip
BuildRequires:  qt5-qtbase-devel
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-rosbuild

Requires:       python-qt5 sip

%description
This stack provides Python bindings for Qt. There are two providers:
pyside and pyqt. PySide is released under the LGPL. PyQt is released
under the GPL. Both the bindings and tools to build bindings are
included from each available provider. For PySide, it is called
"Shiboken". For PyQt, this is called "SIP". Also provided is adapter
code to make the user's Python code independent of which binding
provider was actually used which makes it very easy to switch between
these.


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
  --pkg python_qt_binding

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
* Sun Nov 19 2017 Till Hofmann <thofmann@fedoraproject.org> - 0.3.3-1
- Update to latest release
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.3.2-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.3.2-1
- Update auto-generated Spec file
