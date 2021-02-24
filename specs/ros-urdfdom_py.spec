Name:           ros-urdfdom_py
Version:        noetic.0.4.5
Release:        2%{?dist}
Summary:        ROS package urdfdom_py

License:        BSD
URL:            http://wiki.ros.org/urdfdom_py

Source0:        https://github.com/ros-gbp/urdfdom_py-release/archive/release/noetic/urdfdom_py/0.4.5-1.tar.gz#/ros-noetic-urdfdom_py-0.4.5-source0.tar.gz


BuildArch: noarch

# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel
BuildRequires:  python-unversioned-command

BuildRequires:  python3-mock
BuildRequires:  python3-setuptools
BuildRequires:  ros-noetic-catkin-devel

Requires:       python3-pyyaml
Requires:       python3dist(pyyaml)
Requires:       ros-noetic-rospy

Provides:  ros-noetic-urdfdom_py = 0.4.5-2
Obsoletes: ros-noetic-urdfdom_py < 0.4.5-2
Obsoletes: ros-kinetic-urdfdom_py < 0.4.5-2



%description
Python implementation of the URDF parser.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       python3-setuptools
Requires:       ros-noetic-catkin-devel
Requires:       python3-mock
Requires:       ros-noetic-rospy-devel

Provides: ros-noetic-urdfdom_py-devel = 0.4.5-2
Obsoletes: ros-noetic-urdfdom_py-devel < 0.4.5-2
Obsoletes: ros-kinetic-urdfdom_py-devel < 0.4.5-2


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
  --pkg urdfdom_py




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,local_setup*,setup*,env.sh}

touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig,share/urdfdom_py/cmake} \
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
* Tue Feb 23 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.4.5-2
- Modernize python shebang replacement
* Wed Feb 17 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.4.5-1
- Update to latest release
* Mon Nov 02 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.4.4-1
- Update to latest release
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.4.3-1
- Upgrade to noetic
* Fri Apr 17 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.4.3-1
- Update to latest release
* Thu Mar 05 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.4.2-2
- Fix dependency on python3-pyyaml
* Tue Feb 04 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.4.2-1
- Update to latest release
* Mon Jul 22 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.4.0-3
- Remove obsolete python2 dependencies
* Sun Jul 21 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.4.0-2
- Switch to python3
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.4.0-1
- Update to ROS melodic release
* Thu Jan 18 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.3.3-1
- Initial package
