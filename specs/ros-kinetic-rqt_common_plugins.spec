Name:           ros-kinetic-rqt_common_plugins
Version:        0.4.8
Release:        2%{?dist}
Summary:        ROS package rqt_common_plugins

License:        BSD
URL:            http://ros.org/wiki/rqt_common_plugins

Source0:        https://github.com/ros-gbp/rqt_common_plugins-release/archive/release/kinetic/rqt_common_plugins/0.4.8-0.tar.gz#/ros-kinetic-rqt_common_plugins-0.4.8-source0.tar.gz


BuildArch: noarch

BuildRequires:  ros-kinetic-catkin

Requires:       ros-kinetic-rqt_action
Requires:       ros-kinetic-rqt_bag
Requires:       ros-kinetic-rqt_bag_plugins
Requires:       ros-kinetic-rqt_console
Requires:       ros-kinetic-rqt_dep
Requires:       ros-kinetic-rqt_graph
Requires:       ros-kinetic-rqt_image_view
Requires:       ros-kinetic-rqt_launch
Requires:       ros-kinetic-rqt_logger_level
Requires:       ros-kinetic-rqt_msg
Requires:       ros-kinetic-rqt_plot
Requires:       ros-kinetic-rqt_publisher
Requires:       ros-kinetic-rqt_py_common
Requires:       ros-kinetic-rqt_py_console
Requires:       ros-kinetic-rqt_reconfigure
Requires:       ros-kinetic-rqt_service_caller
Requires:       ros-kinetic-rqt_shell
Requires:       ros-kinetic-rqt_srv
Requires:       ros-kinetic-rqt_top
Requires:       ros-kinetic-rqt_topic
Requires:       ros-kinetic-rqt_web

%description
rqt_common_plugins metapackage provides ROS backend graphical tools
suite that can be used on/off of robot runtime.


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
  --pkg rqt_common_plugins

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
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.4.8-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.4.8-1
- Update auto-generated Spec file
