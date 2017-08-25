Name:           ros-kinetic-rqt_dep
Version:        0.4.8
Release:        1%{?dist}
Summary:        ROS package rqt_dep

License:        BSD
URL:            http://wiki.ros.org/rqt_dep

Source0:        https://github.com/ros-gbp/rqt_dep-release/archive/release/kinetic/rqt_dep/0.4.8-0.tar.gz#/ros-kinetic-rqt_dep-0.4.8-source0.tar.gz


BuildArch: noarch

BuildRequires:  python-mock
BuildRequires:  ros-kinetic-catkin

Requires:       python-rospkg
Requires:       ros-kinetic-python_qt_binding
Requires:       ros-kinetic-qt_dotgraph
Requires:       ros-kinetic-qt_gui
Requires:       ros-kinetic-qt_gui_py_common
Requires:       ros-kinetic-rqt_graph
Requires:       ros-kinetic-rqt_gui_py

%description
rqt_dep provides a GUI plugin for visualizing the ROS dependency
graph.


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
  --pkg rqt_dep

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
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.4.8-1
- Update auto-generated Spec file