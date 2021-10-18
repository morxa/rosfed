Name:           ros-mbf_costmap_core
Version:        noetic.0.3.4
Release:        3%{?dist}
Summary:        ROS package mbf_costmap_core

License:        BSD-3
URL:            http://www.ros.org/

Source0:        https://github.com/uos-gbp/move_base_flex-release/archive/release/noetic/mbf_costmap_core/0.3.4-1.tar.gz#/ros-noetic-mbf_costmap_core-0.3.4-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel
BuildRequires:  python-unversioned-command

BuildRequires:  ros-noetic-catkin-devel
BuildRequires:  ros-noetic-costmap_2d-devel
BuildRequires:  ros-noetic-geometry_msgs-devel
BuildRequires:  ros-noetic-mbf_abstract_core-devel
BuildRequires:  ros-noetic-mbf_utility-devel
BuildRequires:  ros-noetic-nav_core-devel
BuildRequires:  ros-noetic-std_msgs-devel
BuildRequires:  ros-noetic-tf-devel

Requires:       ros-noetic-costmap_2d
Requires:       ros-noetic-geometry_msgs
Requires:       ros-noetic-mbf_abstract_core
Requires:       ros-noetic-mbf_utility
Requires:       ros-noetic-nav_core
Requires:       ros-noetic-std_msgs
Requires:       ros-noetic-tf

Provides:  ros-noetic-mbf_costmap_core = 0.3.4-3
Obsoletes: ros-noetic-mbf_costmap_core < 0.3.4-3
Obsoletes: ros-kinetic-mbf_costmap_core < 0.3.4-3



%description
This package provides common interfaces for navigation specific robot
actions. It contains the CostmapPlanner, CostmapController and
CostmapRecovery interfaces. The interfaces have to be implemented by
the plugins to make them available for Move Base Flex using the
mbf_costmap_nav navigation implementation. That implementation
inherits the mbf_abstract_nav implementation and binds the system to a
local and a global costmap.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-noetic-catkin-devel
Requires:       ros-noetic-costmap_2d-devel
Requires:       ros-noetic-geometry_msgs-devel
Requires:       ros-noetic-mbf_abstract_core-devel
Requires:       ros-noetic-mbf_utility-devel
Requires:       ros-noetic-nav_core-devel
Requires:       ros-noetic-std_msgs-devel
Requires:       ros-noetic-tf-devel

Provides: ros-noetic-mbf_costmap_core-devel = 0.3.4-3
Obsoletes: ros-noetic-mbf_costmap_core-devel < 0.3.4-3
Obsoletes: ros-kinetic-mbf_costmap_core-devel < 0.3.4-3


%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.


%global debug_package %{nil}

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
  --pkg mbf_costmap_core




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,local_setup*,setup*,env.sh}

touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig,share/mbf_costmap_core/cmake} \
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
* Thu Oct 14 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.3.4-3
- Rebuild to pull in updated dependencies
* Tue Feb 23 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.3.4-2
- Modernize python shebang replacement
* Wed Feb 17 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.3.4-1
- Update to latest release
* Fri Nov 20 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.3.3-1
- Update to latest release
* Thu Jun 11 2020 Nicolas Limpert - noetic.0.3.2-1
- Update to latest release
* Fri Mar 13 2020 Nicolas Limpert - melodic.0.2.5-1
- Initial package
