Name:           ros-rqt_tf_tree
Version:        kinetic.0.6.0
Release:        2%{?dist}
Summary:        ROS package rqt_tf_tree

License:        BSD
URL:            http://wiki.ros.org/rqt_tf_tree

Source0:        https://github.com/ros-gbp/rqt_tf_tree-release/archive/release/kinetic/rqt_tf_tree/0.6.0-0.tar.gz#/ros-kinetic-rqt_tf_tree-0.6.0-source0.tar.gz


BuildArch: noarch

# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  python-mock
BuildRequires:  ros-kinetic-catkin-devel

Requires:       python-rospkg
Requires:       ros-kinetic-geometry_msgs
Requires:       ros-kinetic-python_qt_binding
Requires:       ros-kinetic-qt_dotgraph
Requires:       ros-kinetic-rospy
Requires:       ros-kinetic-rqt_graph
Requires:       ros-kinetic-rqt_gui
Requires:       ros-kinetic-rqt_gui_py
Requires:       ros-kinetic-tf2
Requires:       ros-kinetic-tf2_msgs
Requires:       ros-kinetic-tf2_ros


%description
rqt_tf_tree provides a GUI plugin for visualizing the ROS TF frame
tree.

Provides:  ros-kinetic-rqt_tf_tree = %{version}-%{release}
Obsoletes: ros-kinetic-rqt_tf_tree < %{version}-%{release}

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       ros-kinetic-catkin-devel
Requires:       python-mock
Requires:       ros-kinetic-geometry_msgs-devel
Requires:       ros-kinetic-python_qt_binding-devel
Requires:       ros-kinetic-qt_dotgraph-devel
Requires:       ros-kinetic-rospy-devel
Requires:       ros-kinetic-rqt_graph-devel
Requires:       ros-kinetic-rqt_gui-devel
Requires:       ros-kinetic-rqt_gui_py-devel
Requires:       ros-kinetic-tf2-devel
Requires:       ros-kinetic-tf2_msgs-devel
Requires:       ros-kinetic-tf2_ros-devel

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

Provides: ros-kinetic-rqt_tf_tree-devel = %{version}-%{release}
Obsoletes: ros-kinetic-rqt_tf_tree-devel < %{version}-%{release}



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
  --pkg rqt_tf_tree




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
for file in $(grep -rIl '^#!.*python\s*$') ; do
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
* Fri Jul 12 2019 Till Hofmann <thofmann@fedoraproject.org> - 0.6.0-2
- Remove ROS distro from package name
* Thu Mar 14 2019 Till Hofmann <thofmann@fedoraproject.org> - 0.6.0-1
- Update to latest release
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.5.8-9
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.5.8-8
- devel also requires: the devel package of each run dependency
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.5.8-7
- Also add upstream's exec_depend as Requires:
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.5.8-6
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.5.8-5
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.5.8-4
- Add Recommends: for all BRs to the devel subpackage
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.5.8-3
- Split devel package
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.5.8-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.5.8-1
- Update auto-generated Spec file
