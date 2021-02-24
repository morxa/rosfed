Name:           ros-image_rotate
Version:        noetic.1.15.3
Release:        2%{?dist}
Summary:        ROS package image_rotate

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/image_pipeline-release/archive/release/noetic/image_rotate/1.15.3-1.tar.gz#/ros-noetic-image_rotate-1.15.3-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel
BuildRequires:  python-unversioned-command

BuildRequires:  eigen3-devel
BuildRequires:  libuuid-devel
BuildRequires:  opencv-devel
BuildRequires:  poco-devel
BuildRequires:  tinyxml-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  ros-noetic-catkin-devel
BuildRequires:  ros-noetic-cmake_modules-devel
BuildRequires:  ros-noetic-cv_bridge-devel
BuildRequires:  ros-noetic-dynamic_reconfigure-devel
BuildRequires:  ros-noetic-geometry_msgs-devel
BuildRequires:  ros-noetic-image_transport-devel
BuildRequires:  ros-noetic-nodelet-devel
BuildRequires:  ros-noetic-roscpp-devel
BuildRequires:  ros-noetic-rostest-devel
BuildRequires:  ros-noetic-tf2-devel
BuildRequires:  ros-noetic-tf2_geometry_msgs-devel
BuildRequires:  ros-noetic-tf2_ros-devel

Requires:       ros-noetic-cv_bridge
Requires:       ros-noetic-dynamic_reconfigure
Requires:       ros-noetic-image_transport
Requires:       ros-noetic-nodelet
Requires:       ros-noetic-roscpp
Requires:       ros-noetic-tf2
Requires:       ros-noetic-tf2_geometry_msgs
Requires:       ros-noetic-tf2_ros

Provides:  ros-noetic-image_rotate = 1.15.3-2
Obsoletes: ros-noetic-image_rotate < 1.15.3-2
Obsoletes: ros-kinetic-image_rotate < 1.15.3-2



%description
ROS noetic package image_rotate.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-noetic-catkin-devel
Requires:       eigen3-devel
Requires:       libuuid-devel
Requires:       opencv-devel
Requires:       poco-devel
Requires:       tinyxml-devel
Requires:       tinyxml2-devel
Requires:       ros-noetic-cmake_modules-devel
Requires:       ros-noetic-cv_bridge-devel
Requires:       ros-noetic-dynamic_reconfigure-devel
Requires:       ros-noetic-geometry_msgs-devel
Requires:       ros-noetic-image_transport-devel
Requires:       ros-noetic-nodelet-devel
Requires:       ros-noetic-roscpp-devel
Requires:       ros-noetic-rostest-devel
Requires:       ros-noetic-tf2-devel
Requires:       ros-noetic-tf2_geometry_msgs-devel
Requires:       ros-noetic-tf2_ros-devel

Provides: ros-noetic-image_rotate-devel = 1.15.3-2
Obsoletes: ros-noetic-image_rotate-devel < 1.15.3-2
Obsoletes: ros-kinetic-image_rotate-devel < 1.15.3-2


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
  --pkg image_rotate




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,local_setup*,setup*,env.sh}

touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig,share/image_rotate/cmake} \
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
* Tue Feb 23 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.15.3-2
- Modernize python shebang replacement
* Wed Feb 17 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.15.3-1
- Update to latest release
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.15.2-1
- Upgrade to noetic
* Tue Feb 04 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.14.0-1
- Update to latest release
* Mon Jul 22 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.13.0-3
- Remove obsolete python2 dependencies
* Sun Jul 21 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.13.0-2
- Switch to python3
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.13.0-1
- Update to ROS melodic release
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.23-3
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.23-2
- devel also requires: the devel package of each run dependency
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.23-1
- Also add upstream's exec_depend as Requires:
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.22-5
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.22-4
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.22-3
- Add Recommends: for all BRs to the devel subpackage
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.22-2
- Split devel package
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.22-1
- Split devel package
* Thu Nov 23 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.12.21-2
- Build against system opencv3 instead of ros-kinetic-opencv
* Sun Nov 19 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.12.21-1
- Update to latest release
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.12.20-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.12.20-1
- Update auto-generated Spec file
