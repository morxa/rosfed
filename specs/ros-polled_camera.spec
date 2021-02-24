Name:           ros-polled_camera
Version:        noetic.1.12.0
Release:        2%{?dist}
Summary:        ROS package polled_camera

License:        BSD
URL:            http://ros.org/wiki/polled_camera

Source0:        https://github.com/ros-gbp/image_common-release/archive/release/noetic/polled_camera/1.12.0-1.tar.gz#/ros-noetic-polled_camera-1.12.0-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel
BuildRequires:  python-unversioned-command

BuildRequires:  poco-devel
BuildRequires:  tinyxml-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  ros-noetic-catkin-devel
BuildRequires:  ros-noetic-image_transport-devel
BuildRequires:  ros-noetic-message_generation-devel
BuildRequires:  ros-noetic-roscpp-devel
BuildRequires:  ros-noetic-sensor_msgs-devel
BuildRequires:  ros-noetic-std_msgs-devel

Requires:       ros-noetic-image_transport
Requires:       ros-noetic-message_runtime
Requires:       ros-noetic-roscpp
Requires:       ros-noetic-sensor_msgs
Requires:       ros-noetic-std_msgs

Provides:  ros-noetic-polled_camera = 1.12.0-2
Obsoletes: ros-noetic-polled_camera < 1.12.0-2
Obsoletes: ros-kinetic-polled_camera < 1.12.0-2



%description
polled_camera contains a service and C++ helper classes for
implementing a polled camera driver node and requesting images from
it. The package is currently for internal use as the API is still
under development.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-noetic-catkin-devel
Requires:       poco-devel
Requires:       tinyxml-devel
Requires:       tinyxml2-devel
Requires:       ros-noetic-image_transport-devel
Requires:       ros-noetic-message_generation-devel
Requires:       ros-noetic-roscpp-devel
Requires:       ros-noetic-sensor_msgs-devel
Requires:       ros-noetic-std_msgs-devel
Requires:       ros-noetic-message_runtime-devel

Provides: ros-noetic-polled_camera-devel = 1.12.0-2
Obsoletes: ros-noetic-polled_camera-devel < 1.12.0-2
Obsoletes: ros-kinetic-polled_camera-devel < 1.12.0-2


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
  --pkg polled_camera




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,local_setup*,setup*,env.sh}

touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig,share/polled_camera/cmake} \
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
* Tue Feb 23 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.12.0-2
- Modernize python shebang replacement
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.12.0-1
- Upgrade to noetic
* Mon Jul 22 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.11.13-12
- Remove obsolete python2 dependencies
* Sun Jul 21 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.11.13-11
- Switch to python3
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.11.13-10
- Update to ROS melodic release
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
