Name:           ros-kdl_conversions
Version:        noetic.1.13.2
Release:        4%{?dist}
Summary:        ROS package kdl_conversions

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/geometry-release/archive/release/noetic/kdl_conversions/1.13.2-1.tar.gz#/ros-noetic-kdl_conversions-1.13.2-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel
BuildRequires:  python-unversioned-command

BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  orocos-kdl-devel
BuildRequires:  ros-noetic-catkin-devel
BuildRequires:  ros-noetic-cpp_common-devel
BuildRequires:  ros-noetic-geometry_msgs-devel
BuildRequires:  ros-noetic-roscpp_serialization-devel

Requires:       orocos-kdl
Requires:       ros-noetic-geometry_msgs

Provides:  ros-noetic-kdl_conversions = 1.13.2-4
Obsoletes: ros-noetic-kdl_conversions < 1.13.2-4
Obsoletes: ros-kinetic-kdl_conversions < 1.13.2-4



%description
Conversion functions between KDL and geometry_msgs types.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       orocos-kdl-devel
Requires:       ros-noetic-catkin-devel
Requires:       boost-devel
Requires:       console-bridge-devel
Requires:       ros-noetic-cpp_common-devel
Requires:       ros-noetic-geometry_msgs-devel
Requires:       ros-noetic-roscpp_serialization-devel

Provides: ros-noetic-kdl_conversions-devel = 1.13.2-4
Obsoletes: ros-noetic-kdl_conversions-devel < 1.13.2-4
Obsoletes: ros-kinetic-kdl_conversions-devel < 1.13.2-4


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
  --pkg kdl_conversions




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,local_setup*,setup*,env.sh}

touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig,share/kdl_conversions/cmake} \
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
* Mon Jun 06 2022 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.13.2-4
- Rebuild for orocos-kdl-1.5
* Thu Oct 14 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.13.2-3
- Rebuild to pull in updated dependencies
* Tue Feb 23 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.13.2-2
- Modernize python shebang replacement
* Mon Aug 10 2020 Nicolas Limpert <limpert@fh-aachen.de> - noetic.1.13.2-1
- Update to latest release
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.13.1-1
- Upgrade to noetic
* Fri Apr 17 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.12.1-1
- Update to latest release
* Mon Jul 22 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.12.0-3
- Remove obsolete python2 dependencies
* Sun Jul 21 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.12.0-2
- Switch to python3
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.12.0-1
- Update to ROS melodic release
* Fri Jul 12 2019 Till Hofmann <thofmann@fedoraproject.org> - 1.11.9-13
- Remove ROS distro from package name
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.9-12
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.9-11
- devel also requires: the devel package of each run dependency
* Wed May 16 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.9-10
- Add missing build dependency on roscpp_serialization
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.9-9
- Also add upstream's exec_depend as Requires:
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.9-8
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.9-7
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.9-6
- Add Recommends: for all BRs to the devel subpackage
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.9-5
- Split devel package
* Mon Nov 20 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.11.9-4
- Add missing BR on console-bridge-devel
* Mon Nov 20 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.11.9-3
- Add missing BR on boost-devel
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.11.9-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.11.9-1
- Update auto-generated Spec file
