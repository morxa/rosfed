Name:           ros-rqt_common_plugins
Version:        melodic.0.4.8
Release:        1%{?dist}
Summary:        ROS package rqt_common_plugins

License:        BSD
URL:            http://ros.org/wiki/rqt_common_plugins

Source0:        https://github.com/ros-gbp/rqt_common_plugins-release/archive/release/melodic/rqt_common_plugins/0.4.8-0.tar.gz#/ros-melodic-rqt_common_plugins-0.4.8-source0.tar.gz


BuildArch: noarch

# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  ros-melodic-catkin-devel

Requires:       ros-melodic-rqt_action
Requires:       ros-melodic-rqt_bag
Requires:       ros-melodic-rqt_bag_plugins
Requires:       ros-melodic-rqt_console
Requires:       ros-melodic-rqt_dep
Requires:       ros-melodic-rqt_graph
Requires:       ros-melodic-rqt_image_view
Requires:       ros-melodic-rqt_launch
Requires:       ros-melodic-rqt_logger_level
Requires:       ros-melodic-rqt_msg
Requires:       ros-melodic-rqt_plot
Requires:       ros-melodic-rqt_publisher
Requires:       ros-melodic-rqt_py_common
Requires:       ros-melodic-rqt_py_console
Requires:       ros-melodic-rqt_reconfigure
Requires:       ros-melodic-rqt_service_caller
Requires:       ros-melodic-rqt_shell
Requires:       ros-melodic-rqt_srv
Requires:       ros-melodic-rqt_top
Requires:       ros-melodic-rqt_topic
Requires:       ros-melodic-rqt_web

Provides:  ros-melodic-rqt_common_plugins = 0.4.8-1
Obsoletes: ros-melodic-rqt_common_plugins < 0.4.8-1


%description
rqt_common_plugins metapackage provides ROS backend graphical tools
suite that can be used on/off of robot runtime.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       ros-melodic-catkin-devel
Requires:       ros-melodic-rqt_action-devel
Requires:       ros-melodic-rqt_bag-devel
Requires:       ros-melodic-rqt_bag_plugins-devel
Requires:       ros-melodic-rqt_console-devel
Requires:       ros-melodic-rqt_dep-devel
Requires:       ros-melodic-rqt_graph-devel
Requires:       ros-melodic-rqt_image_view-devel
Requires:       ros-melodic-rqt_launch-devel
Requires:       ros-melodic-rqt_logger_level-devel
Requires:       ros-melodic-rqt_msg-devel
Requires:       ros-melodic-rqt_plot-devel
Requires:       ros-melodic-rqt_publisher-devel
Requires:       ros-melodic-rqt_py_common-devel
Requires:       ros-melodic-rqt_py_console-devel
Requires:       ros-melodic-rqt_reconfigure-devel
Requires:       ros-melodic-rqt_service_caller-devel
Requires:       ros-melodic-rqt_shell-devel
Requires:       ros-melodic-rqt_srv-devel
Requires:       ros-melodic-rqt_top-devel
Requires:       ros-melodic-rqt_topic-devel
Requires:       ros-melodic-rqt_web-devel

Provides: ros-melodic-rqt_common_plugins-devel = 0.4.8-1
Obsoletes: ros-melodic-rqt_common_plugins-devel < 0.4.8-1

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
  --pkg rqt_common_plugins




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,local_setup*,setup*,env.sh}

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



# replace unversioned python shebang
for file in $(grep -rIl '^#!.*python\s*$' %{buildroot}) ; do
  sed -i.orig '/^#!.*python\s*$/ { s/python/python2/ }' $file
  touch -r $file.orig $file
  rm $file.orig
done

# replace "/usr/bin/env $interpreter" with "/usr/bin/$interpreter"
for interpreter in bash sh python2 python3 ; do
  for file in $(grep -rIl "^#\!.*${interpreter}" %{buildroot}) ; do
    sed -i.orig "s:^#\!\s*/usr/bin/env\s\+${interpreter}.*:#!/usr/bin/${interpreter}:" $file
    touch -r $file.orig $file
    rm $file.orig
  done
done


echo "This is a package automatically generated with rosfed." >> README_FEDORA
echo "See https://pagure.io/ros for more information." >> README_FEDORA
install -p -D -t %{buildroot}/%{_docdir}/%{name} README_FEDORA
echo %{_docdir}/%{name} >> files.list
install -p -D -t %{buildroot}/%{_docdir}/%{name}-devel README_FEDORA
echo %{_docdir}/%{name}-devel >> files_devel.list


%files -f files.list
%files devel -f files_devel.list


%changelog
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.4.8-1
- Update to ROS melodic release
* Fri Jul 12 2019 Till Hofmann <thofmann@fedoraproject.org> - 0.4.8-11
- Remove ROS distro from package name
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.8-10
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.8-9
- devel also requires: the devel package of each run dependency
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.8-8
- Also add upstream's exec_depend as Requires:
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.8-7
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.8-6
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.8-5
- Add Recommends: for all BRs to the devel subpackage
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.8-4
- Split devel package
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.8-3
- Split devel package
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.4.8-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.4.8-1
- Update auto-generated Spec file
