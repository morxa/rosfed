Name:           ros-map_server
Version:        noetic.1.17.2
Release:        1%{?dist}
Summary:        ROS package map_server

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/navigation-release/archive/release/noetic/map_server/1.17.2-1.tar.gz#/ros-noetic-map_server-1.17.2-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel
BuildRequires:  python-unversioned-command

BuildRequires:  bullet-devel
BuildRequires:  SDL-devel
BuildRequires:  SDL_image-devel
BuildRequires:  yaml-cpp-devel
BuildRequires:  ros-noetic-catkin-devel
BuildRequires:  ros-noetic-nav_msgs-devel
BuildRequires:  ros-noetic-roscpp-devel
BuildRequires:  ros-noetic-roslib-devel
BuildRequires:  ros-noetic-rospy-devel
BuildRequires:  ros-noetic-rostest-devel
BuildRequires:  ros-noetic-rosunit-devel
BuildRequires:  ros-noetic-tf2-devel

Requires:       ros-noetic-nav_msgs
Requires:       ros-noetic-roscpp
Requires:       ros-noetic-tf2

Provides:  ros-noetic-map_server = 1.17.2-1
Obsoletes: ros-noetic-map_server < 1.17.2-1
Obsoletes: ros-kinetic-map_server < 1.17.2-1



%description
map_server provides the

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-noetic-catkin-devel
Requires:       bullet-devel
Requires:       SDL-devel
Requires:       SDL_image-devel
Requires:       yaml-cpp-devel
Requires:       ros-noetic-nav_msgs-devel
Requires:       ros-noetic-roscpp-devel
Requires:       ros-noetic-roslib-devel
Requires:       ros-noetic-rospy-devel
Requires:       ros-noetic-rostest-devel
Requires:       ros-noetic-rosunit-devel
Requires:       ros-noetic-tf2-devel

Provides: ros-noetic-map_server-devel = 1.17.2-1
Obsoletes: ros-noetic-map_server-devel < 1.17.2-1
Obsoletes: ros-kinetic-map_server-devel < 1.17.2-1


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
  --pkg map_server




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,local_setup*,setup*,env.sh}

touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig,share/map_server/cmake} \
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
* Tue Jun 28 2022 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.17.2-1
- Update to latest release
* Thu Oct 14 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.17.1-3
- Rebuild to pull in updated dependencies
* Tue Feb 23 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.17.1-2
- Modernize python shebang replacement
* Mon Nov 02 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.17.1-1
- Update to latest release
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.17.0-1
- Upgrade to noetic
* Fri Apr 17 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.16.6-1
- Update to latest release
* Wed Mar 18 2020 Nicolas Limpert - melodic.1.16.5-1
- Update to latest release
* Thu Mar 05 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.16.4-1
- Update to latest release
* Tue Feb 04 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.16.3-1
- Update to latest release
* Wed Jul 24 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.16.2-1
- Update to latest release
* Tue Jun 26 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.14.4-1
- Update to latest release
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.14.3-5
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.14.3-4
- devel also requires: the devel package of each run dependency
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.14.3-3
- Also add upstream's exec_depend as Requires:
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.14.3-2
- Add corresponding devel Requires: for the package's BRs and Rs
* Mon May 14 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.14.3-1
- Update to latest release, rebuild for F28
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.14.2-5
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.14.2-4
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.14.2-3
- Add Recommends: for all BRs to the devel subpackage
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.14.2-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.14.2-1
- Update auto-generated Spec file
