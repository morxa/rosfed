Name:           ros-catkin
Version:        noetic.0.8.10
Release:        1%{?dist}
Summary:        ROS package catkin

License:        BSD
URL:            http://wiki.ros.org/catkin

Source0:        https://github.com/ros-gbp/catkin-release/archive/release/noetic/catkin/0.8.10-1.tar.gz#/ros-noetic-catkin-0.8.10-source0.tar.gz

Patch0: ros-kinetic-catkin.python-path-in-templates.patch
Patch1: ros-catkin.python3.patch

BuildArch: noarch

# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel
BuildRequires:  python-unversioned-command

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gmock-devel
BuildRequires:  gtest-devel
BuildRequires:  python3
BuildRequires:  python3-catkin_pkg
BuildRequires:  python3-empy
BuildRequires:  python3-mock
BuildRequires:  python3-nose
BuildRequires:  python3-pyparsing
BuildRequires:  python3-setuptools

Requires:       python3
Requires:       python3-catkin_pkg
Requires:       python3-empy
Requires:       python3-pyparsing

Provides:  ros-noetic-catkin = 0.8.10-1
Obsoletes: ros-noetic-catkin < 0.8.10-1
Obsoletes: ros-kinetic-catkin < 0.8.10-1


Obsoletes: ros-kdl_parser_py < melodic.1.13.1-4
Obsoletes: ros-orocos_kdl < melodic.1.4.0-4
Obsoletes: ros-python_orocos_kdl < melodic.1.4.0-6

%description
Low-level build system macros and infrastructure for ROS.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       cmake
Requires:       gmock-devel
Requires:       gtest-devel
Requires:       python3-nose
Requires:       python3-setuptools
Requires:       gcc-c++
Requires:       python3
Requires:       python3-catkin_pkg
Requires:       python3-empy
Requires:       python3-mock
Requires:       python3-pyparsing

Provides: ros-noetic-catkin-devel = 0.8.10-1
Obsoletes: ros-noetic-catkin-devel < 0.8.10-1
Obsoletes: ros-kinetic-catkin-devel < 0.8.10-1

Obsoletes: ros-kdl_parser_py-devel < melodic.1.13.1-4
Obsoletes: ros-orocos_kdl-devel < melodic.1.4.0-4
Obsoletes: ros-python_orocos_kdl-devel < melodic.1.4.0-6

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.



%prep

%setup -c -T
tar --strip-components=1 -xf %{SOURCE0}
%patch0 -p1
%patch1 -p1

%build
# nothing to do here


%install

PYTHONUNBUFFERED=1 ; export PYTHONUNBUFFERED

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
FFLAGS="${FFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FFLAGS ; \
FCFLAGS="${FCFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FCFLAGS ; \
%{?__global_ldflags:LDFLAGS="${LDFLAGS:-%__global_ldflags}" ; export LDFLAGS ;} \


# substitute shebang before install block because we run the local catkin script
%py3_shebang_fix .

DESTDIR=%{buildroot} ; export DESTDIR

./bin/catkin_make_isolated \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCATKIN_ENABLE_TESTING=OFF \
  --source . \
  --install \
  --install-space %{_libdir}/ros/ \
  --pkg catkin


touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files_devel.list

find %{buildroot}/%{_libdir}/ros -maxdepth 1 \
  -name .catkin -o -name .rosinstall \
  -o -name "_setup*" -o -name "setup.*" -o -name "local_setup.*" -o -name env.sh \
  | sed -e "s:%{buildroot}/::" -e "s:.py$:.py{,o,c}:" >> files.list

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
* Mon May 17 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.8.10-1
- Update to latest release
* Tue Feb 23 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.8.9-2
- Modernize python shebang replacement
* Mon Nov 02 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.8.9-1
- Update to latest release
* Sat Aug 08 2020 Nicolas Limpert - noetic.0.8.8-1
- Update to latest release
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.8.5-2
- Obsolete old packages
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.0.8.5-1
- Upgrade to noetic
* Wed Mar 04 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.7.23-1
- Update to latest release
* Tue Feb 04 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.7.20-1
- Update to latest release
* Thu Oct 24 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.7.19-2
- Replace python shebang macros
* Thu Oct 24 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.7.19-1
- Update to latest release
* Fri Aug 16 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.7.17-4
- Add patch to enforce python3 as interpreter
* Mon Jul 22 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.7.17-3
- Remove obsolete python2 dependencies
* Sun Jul 21 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.7.17-2
- Switch to python3
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.7.17-1
- Update to ROS melodic release
* Fri Jul 12 2019 Till Hofmann <thofmann@fedoraproject.org> - 0.7.18-2
- Remove ROS distro from package name
* Fri Jul 12 2019 Till Hofmann <thofmann@fedoraproject.org> - 0.7.18-1
- Update to latest release
* Wed Nov 07 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.7.14-1
- Update to latest release
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.7.11-8
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.7.11-7
- devel also requires: the devel package of each run dependency
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.7.11-6
- Also add upstream's exec_depend as Requires:
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.7.11-5
- Add corresponding devel Requires: for the package's BRs and Rs
* Mon May 14 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.7.11-4
- Add missing Requires: on python2-pyparsing
* Mon May 14 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.7.11-3
- Replace unversioned python shebangs by versioned shebangs
* Mon May 14 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.7.11-2
- Add missing BR on pyparsing, fix python2 deprecation warning
* Mon May 14 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.7.11-1
- Update to latest release, rebuild for F28
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.7.8-6
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.7.8-5
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.7.8-4
- Add Recommends: for all BRs to the devel subpackage
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.7.8-3
- Split devel package
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.7.8-2
- Split devel package
* Sun Nov 19 2017 Till Hofmann <thofmann@fedoraproject.org> - 0.7.8-1
- Update to latest release
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.7.6-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.7.6-1
- Update auto-generated Spec file
