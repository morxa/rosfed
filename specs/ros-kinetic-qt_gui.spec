Name:           ros-kinetic-qt_gui
Version:        0.3.4
Release:        2%{?dist}
Summary:        ROS package qt_gui

License:        BSD
URL:            http://ros.org/wiki/qt_gui

Source0:        https://github.com/ros-gbp/qt_gui_core-release/archive/release/kinetic/qt_gui/0.3.4-0.tar.gz#/ros-kinetic-qt_gui-0.3.4-source0.tar.gz


BuildArch: noarch

BuildRequires:  python-qt5 sip
BuildRequires:  qt5-qtbase-devel
BuildRequires:  ros-kinetic-catkin

Requires:       python-rospkg
Requires:       tango-icon-theme
Requires:       ros-kinetic-python_qt_binding

%description
qt_gui provides the infrastructure for an integrated graphical user
interface based on Qt. It is extensible with Python- and C++-based
plugins (implemented in separate packages) which can contribute
arbitrary widgets. It requires either PyQt or PySide bindings.


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
  --pkg qt_gui

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
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.3.4-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.3.4-1
- Update auto-generated Spec file
