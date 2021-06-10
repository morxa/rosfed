Name:           ros-eigenpy
Version:        noetic.2.6.3
Release:        1%{?dist}
Summary:        ROS package eigenpy

License:        BSD
URL:            https://github.com/stack-of-tasks/eigenpy

Source0:        https://github.com/ipab-slmc/eigenpy_catkin-release/archive/release/noetic/eigenpy/2.6.3-1.tar.gz#/ros-noetic-eigenpy-2.6.3-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel
BuildRequires:  python-unversioned-command

BuildRequires:  boost-devel
BuildRequires:  boost-python3-devel
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  eigen3-devel
BuildRequires:  git
BuildRequires:  python3-devel
BuildRequires:  python3-numpy
BuildRequires:  python3dist(numpy)
BuildRequires:  ros-noetic-catkin-devel

Requires:       doxygen
Requires:       python3-numpy
Requires:       python3dist(numpy)
Requires:       ros-noetic-catkin

Provides:  ros-noetic-eigenpy = 2.6.3-1
Obsoletes: ros-noetic-eigenpy < 2.6.3-1
Obsoletes: ros-kinetic-eigenpy < 2.6.3-1



%description
Bindings between Numpy and Eigen using Boost.Python

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       cmake
Requires:       boost-devel
Requires:       boost-python3-devel
Requires:       doxygen
Requires:       eigen3-devel
Requires:       git
Requires:       python3-devel
Requires:       python3-numpy
Requires:       python3dist(numpy)
Requires:       ros-noetic-catkin-devel

Provides: ros-noetic-eigenpy-devel = 2.6.3-1
Obsoletes: ros-noetic-eigenpy-devel < 2.6.3-1
Obsoletes: ros-kinetic-eigenpy-devel < 2.6.3-1


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
  --pkg eigenpy




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,local_setup*,setup*,env.sh}

touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig,share/eigenpy/cmake} \
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
* Wed May 26 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.2.6.3-1
- Update to latest release
* Fri Apr 17 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.2.3.1-1
- Update to latest release
* Tue Feb 04 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.6.9-1
- Update to latest release
* Wed Jul 24 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.5.1-1
- Update to latest release
