Name:           ros-cv_bridge
Version:        noetic.1.16.2
Release:        1%{?dist}
Summary:        ROS package cv_bridge

License:        BSD
URL:            http://www.ros.org/wiki/cv_bridge

Source0:        https://github.com/ros-gbp/vision_opencv-release/archive/release/noetic/cv_bridge/1.16.2-1.tar.gz#/ros-noetic-cv_bridge-1.16.2-source0.tar.gz

Patch0: ros-cv_bridge.boost-python3.patch


# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel
BuildRequires:  python-unversioned-command

BuildRequires:  boost-devel
BuildRequires:  boost-python3-devel
BuildRequires:  opencv-devel
BuildRequires:  python3-devel
BuildRequires:  python3-numpy
BuildRequires:  python3-opencv
BuildRequires:  ros-noetic-catkin-devel
BuildRequires:  ros-noetic-rosconsole-devel
BuildRequires:  ros-noetic-roscpp_serialization-devel
BuildRequires:  ros-noetic-rostest-devel
BuildRequires:  ros-noetic-sensor_msgs-devel

Requires:       python3-opencv
Requires:       ros-noetic-rosconsole

Provides:  ros-noetic-cv_bridge = 1.16.2-1
Obsoletes: ros-noetic-cv_bridge < 1.16.2-1
Obsoletes: ros-kinetic-cv_bridge < 1.16.2-1



%description
This contains CvBridge, which converts between ROS Image messages and
OpenCV images.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       opencv-devel
Requires:       ros-noetic-catkin-devel
Requires:       ros-noetic-sensor_msgs-devel
Requires:       boost-devel
Requires:       boost-python3-devel
Requires:       python3-devel
Requires:       python3-numpy
Requires:       python3-opencv
Requires:       ros-noetic-rosconsole-devel
Requires:       ros-noetic-roscpp_serialization-devel
Requires:       ros-noetic-rostest-devel

Provides: ros-noetic-cv_bridge-devel = 1.16.2-1
Obsoletes: ros-noetic-cv_bridge-devel < 1.16.2-1
Obsoletes: ros-kinetic-cv_bridge-devel < 1.16.2-1


%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.



%prep

%setup -c -T
tar --strip-components=1 -xf %{SOURCE0}
%patch0 -p1

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
  --pkg cv_bridge




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,local_setup*,setup*,env.sh}

touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig,share/cv_bridge/cmake} \
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
* Mon Dec 26 2022 Tarik Viehmann <viehmann@kbsg.rwth-aachen.de> - noetic.1.16.2-1
- Update to latest release
* Wed Nov 24 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.16.0-1
- Update to latest release
* Thu Oct 14 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.15.0-5
- Rebuild to pull in updated dependencies
* Tue Feb 23 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.15.0-4
- Modernize python shebang replacement
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.15.0-3
- Add patch to properly detect boost-python
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.15.0-2
- Remove upstreamed patch
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.15.0-1
- Upgrade to noetic
* Wed Apr 29 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.13.0-4
- Add patch for OpenCV4 compatitibility
* Mon Jul 22 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.13.0-3
- Remove obsolete python2 dependencies
* Sun Jul 21 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.13.0-2
- Switch to python3
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.13.0-1
- Update to ROS melodic release
* Fri Jul 12 2019 Till Hofmann <thofmann@fedoraproject.org> - 1.12.8-5
- Remove ROS distro from package name
* Thu Nov 08 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.8-4
- Add missing BR boost-python2-devel
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.8-3
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.8-2
- devel also requires: the devel package of each run dependency
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.8-1
- Also add upstream's exec_depend as Requires:
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.7-6
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.7-5
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.7-4
- Add Recommends: for all BRs to the devel subpackage
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.7-3
- Split devel package
* Thu Nov 23 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.12.7-2
- Build against system opencv3 instead of ros-kinetic-opencv
* Sun Nov 19 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.12.7-1
- Update to latest release
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.12.4-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.12.4-1
- Update auto-generated Spec file
