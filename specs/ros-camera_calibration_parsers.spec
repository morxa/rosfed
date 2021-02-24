Name:           ros-camera_calibration_parsers
Version:        noetic.1.12.0
Release:        4%{?dist}
Summary:        ROS package camera_calibration_parsers

License:        BSD
URL:            http://ros.org/wiki/camera_calibration_parsers

Source0:        https://github.com/ros-gbp/image_common-release/archive/release/noetic/camera_calibration_parsers/1.12.0-1.tar.gz#/ros-noetic-camera_calibration_parsers-1.12.0-source0.tar.gz

Patch0: ros-camera_calibration_parsers.boost-python3.patch


# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel
BuildRequires:  python-unversioned-command

BuildRequires:  boost-devel boost-python3-devel
BuildRequires:  boost-python3-devel
BuildRequires:  console-bridge-devel
BuildRequires:  log4cxx-devel
BuildRequires:  pkgconfig
BuildRequires:  python3-devel
BuildRequires:  yaml-cpp-devel
BuildRequires:  ros-noetic-catkin-devel
BuildRequires:  ros-noetic-rosbash-devel
BuildRequires:  ros-noetic-rosconsole-devel
BuildRequires:  ros-noetic-roscpp-devel
BuildRequires:  ros-noetic-roscpp_serialization-devel
BuildRequires:  ros-noetic-rosunit-devel
BuildRequires:  ros-noetic-sensor_msgs-devel

Requires:       ros-noetic-roscpp
Requires:       ros-noetic-roscpp_serialization
Requires:       ros-noetic-sensor_msgs

Provides:  ros-noetic-camera_calibration_parsers = 1.12.0-4
Obsoletes: ros-noetic-camera_calibration_parsers < 1.12.0-4
Obsoletes: ros-kinetic-camera_calibration_parsers < 1.12.0-4



%description
camera_calibration_parsers contains routines for reading and writing
camera calibration parameters.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-noetic-catkin-devel
Requires:       boost-devel boost-python3-devel
Requires:       boost-python3-devel
Requires:       console-bridge-devel
Requires:       log4cxx-devel
Requires:       pkgconfig
Requires:       python3-devel
Requires:       yaml-cpp-devel
Requires:       ros-noetic-rosbash-devel
Requires:       ros-noetic-rosconsole-devel
Requires:       ros-noetic-roscpp-devel
Requires:       ros-noetic-roscpp_serialization-devel
Requires:       ros-noetic-rosunit-devel
Requires:       ros-noetic-sensor_msgs-devel

Provides: ros-noetic-camera_calibration_parsers-devel = 1.12.0-4
Obsoletes: ros-noetic-camera_calibration_parsers-devel < 1.12.0-4
Obsoletes: ros-kinetic-camera_calibration_parsers-devel < 1.12.0-4


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
  --pkg camera_calibration_parsers




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,local_setup*,setup*,env.sh}

touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig,share/camera_calibration_parsers/cmake} \
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
* Tue Feb 23 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.12.0-4
- Modernize python shebang replacement
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.12.0-3
- Update patch to properly detect boost-python
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.12.0-1
- Upgrade to noetic
* Mon Jul 22 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.11.13-13
- Remove obsolete python2 dependencies
* Sun Jul 21 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.11.13-12
- Switch to python3
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.11.13-11
- Update to ROS melodic release
* Thu Nov 08 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.13-10
- Add missing BR boost-python2-devel
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.13-9
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.13-8
- devel also requires: the devel package of each run dependency
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.13-7
- Also add upstream's exec_depend as Requires:
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.13-6
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.13-5
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.13-4
- Add Recommends: for all BRs to the devel subpackage
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.13-3
- Split devel package
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.13-2
- Split devel package
* Sun Nov 19 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.11.13-1
- Update to latest release
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.11.12-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.11.12-1
- Update auto-generated Spec file
