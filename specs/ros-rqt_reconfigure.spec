Name:           ros-rqt_reconfigure
Version:        noetic.0.5.3
Release:        2%{?dist}
Summary:        ROS package rqt_reconfigure

License:        BSD
URL:            http://wiki.ros.org/rqt_reconfigure

Source0:        https://github.com/ros-gbp/rqt_reconfigure-release/archive/release/noetic/rqt_reconfigure/0.5.3-1.tar.gz#/ros-noetic-rqt_reconfigure-0.5.3-source0.tar.gz


BuildArch: noarch

# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel
BuildRequires:  python-unversioned-command

BuildRequires:  python3-setuptools
BuildRequires:  ros-noetic-catkin-devel
BuildRequires:  ros-noetic-roslint-devel
BuildRequires:  ros-noetic-rostest-devel

Requires:       python3-pyyaml
Requires:       python3dist(pyyaml)
Requires:       ros-noetic-dynamic_reconfigure
Requires:       ros-noetic-python_qt_binding
Requires:       ros-noetic-rospy
Requires:       ros-noetic-rqt_console
Requires:       ros-noetic-rqt_gui
Requires:       ros-noetic-rqt_gui_py
Requires:       ros-noetic-rqt_py_common

Provides:  ros-noetic-rqt_reconfigure = 0.5.3-2
Obsoletes: ros-noetic-rqt_reconfigure < 0.5.3-2
Obsoletes: ros-kinetic-rqt_reconfigure < 0.5.3-2



%description
This rqt plugin succeeds former dynamic_reconfigure's GUI
(reconfigure_gui), and provides the way to view and edit the
parameters that are accessible via dynamic_reconfigure.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       python3-setuptools
Requires:       ros-noetic-catkin-devel
Requires:       ros-noetic-roslint-devel
Requires:       ros-noetic-rostest-devel
Requires:       ros-noetic-dynamic_reconfigure-devel
Requires:       ros-noetic-python_qt_binding-devel
Requires:       ros-noetic-rospy-devel
Requires:       ros-noetic-rqt_console-devel
Requires:       ros-noetic-rqt_gui-devel
Requires:       ros-noetic-rqt_gui_py-devel
Requires:       ros-noetic-rqt_py_common-devel

Provides: ros-noetic-rqt_reconfigure-devel = 0.5.3-2
Obsoletes: ros-noetic-rqt_reconfigure-devel < 0.5.3-2
Obsoletes: ros-kinetic-rqt_reconfigure-devel < 0.5.3-2


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

# substitute shebang before install block because we run the local catkin script
%py3_shebang_fix .

DESTDIR=%{buildroot} ; export DESTDIR


catkin_make_isolated \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCATKIN_ENABLE_TESTING=OFF \
  -DPYTHON_VERSION=%{python3_version} \
  -DPYTHON_VERSION_NODOTS=%{python3_version_nodots} \
  --source . \
  --install \
  --install-space %{_libdir}/ros/ \
  --pkg rqt_reconfigure




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,local_setup*,setup*,env.sh}

touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig,share/rqt_reconfigure/cmake} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files_devel.list

find . -maxdepth 1 -type f -iname "*readme*" | sed "s:^:%%doc :" >> files.list
find . -maxdepth 1 -type f -iname "*license*" | sed "s:^:%%license :" >> files.list



# replace cmake python macro in shebang
for file in $(grep -rIl '^#!.*@PYTHON_EXECUTABLE@.*$' %{buildroot}) ; do
  sed -i.orig 's:^#!\s*@PYTHON_EXECUTABLE@\s*:%{__python3}:' $file
  touch -r $file.orig $file
  rm $file.orig
done


echo "This is a package automatically generated with rosfed." >> README_FEDORA
echo "See https://pagure.io/ros for more information." >> README_FEDORA
install -m 0644 -p -D -t %{buildroot}/%{_docdir}/%{name} README_FEDORA
echo %{_docdir}/%{name} >> files.list
install -m 0644 -p -D -t %{buildroot}/%{_docdir}/%{name}-devel README_FEDORA
echo %{_docdir}/%{name}-devel >> files_devel.list

%py3_shebang_fix %{buildroot}

# Also fix .py.in files
for pyfile in $(grep -rIl '^#!.*python.*$' %{buildroot}) ; do
  %py3_shebang_fix $pyfile
done


%files -f files.list
%files devel -f files_devel.list


%changelog
* Tue Feb 23 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.5.3-2
- Modernize python shebang replacement
* Mon Nov 02 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.5.3-1
- Update to latest release
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.5.2-1
- Upgrade to noetic
* Thu Mar 05 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.5.1-2
- Fix dependency on python3-pyyaml
* Tue Feb 04 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.5.1-1
- Update to latest release
* Mon Jul 22 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.4.10-3
- Remove obsolete python2 dependencies
* Sun Jul 21 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.4.10-2
- Switch to python3
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.4.10-1
- Update to ROS melodic release
* Fri Jul 12 2019 Till Hofmann <thofmann@fedoraproject.org> - 0.4.10-4
- Remove ROS distro from package name
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.10-3
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.10-2
- devel also requires: the devel package of each run dependency
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.10-1
- Also add upstream's exec_depend as Requires:
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.9-4
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.9-3
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.9-2
- Add Recommends: for all BRs to the devel subpackage
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.9-1
- Split devel package
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.4.8-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.4.8-1
- Update auto-generated Spec file
