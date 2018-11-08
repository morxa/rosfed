Name:           ros-kinetic-qt_gui_cpp
Version:        0.3.11
Release:        1%{?dist}
Summary:        ROS package qt_gui_cpp

License:        BSD
URL:            http://ros.org/wiki/qt_gui_cpp

Source0:        https://github.com/ros-gbp/qt_gui_core-release/archive/release/kinetic/qt_gui_cpp/0.3.11-0.tar.gz#/ros-kinetic-qt_gui_cpp-0.3.11-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  pkgconfig
BuildRequires:  poco-devel
BuildRequires:  python-qt5-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qtermwidget-qt5-devel
BuildRequires:  shiboken-devel
BuildRequires:  sip-devel
BuildRequires:  tinyxml-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  ros-kinetic-catkin-devel
BuildRequires:  ros-kinetic-cmake_modules-devel
BuildRequires:  ros-kinetic-pluginlib-devel
BuildRequires:  ros-kinetic-python_qt_binding-devel

Requires:       ros-kinetic-pluginlib
Requires:       ros-kinetic-qt_gui


%description
qt_gui_cpp provides the foundation for C++-bindings for qt_gui and
creates bindings for every generator available. At least one specific
binding must be available in order to use C++-plugins.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-kinetic-catkin-devel
Requires:       boost-devel
Requires:       console-bridge-devel
Requires:       pkgconfig
Requires:       poco-devel
Requires:       python-qt5-devel
Requires:       qt5-qtbase-devel
Requires:       qtermwidget-qt5-devel
Requires:       shiboken-devel
Requires:       sip-devel
Requires:       tinyxml-devel
Requires:       tinyxml2-devel
Requires:       ros-kinetic-cmake_modules-devel
Requires:       ros-kinetic-pluginlib-devel
Requires:       ros-kinetic-python_qt_binding-devel
Requires:       ros-kinetic-qt_gui-devel

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

PATH="$PATH:%{_qt5_bindir}" ; export PATH
source %{_libdir}/ros/setup.bash

DESTDIR=%{buildroot} ; export DESTDIR


catkin_make_isolated \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCATKIN_ENABLE_TESTING=OFF \
  --source . \
  --install \
  --install-space %{_libdir}/ros/ \
  --pkg qt_gui_cpp




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
* Wed Nov 07 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.3.11-1
- Update to latest release
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.3.8-8
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.3.8-7
- devel also requires: the devel package of each run dependency
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.3.8-6
- Also add upstream's exec_depend as Requires:
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.3.8-5
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.3.8-4
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.3.8-3
- Add Recommends: for all BRs to the devel subpackage
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.3.8-2
- Split devel package
* Sun Nov 19 2017 Till Hofmann <thofmann@fedoraproject.org> - 0.3.8-1
- Update to latest release
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.3.4-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.3.4-1
- Update auto-generated Spec file
