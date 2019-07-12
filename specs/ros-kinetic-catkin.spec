Name:           ros-kinetic-catkin
Version:        0.7.18
Release:        1%{?dist}
Summary:        ROS package catkin

License:        BSD
URL:            http://www.ros.org/wiki/catkin

Source0:        https://github.com/ros-gbp/catkin-release/archive/release/kinetic/catkin/0.7.18-1.tar.gz#/ros-kinetic-catkin-0.7.18-source0.tar.gz

Patch0: ros-kinetic-catkin.python-path-in-templates.patch

BuildArch: noarch

# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gmock-devel
BuildRequires:  gtest-devel
BuildRequires:  python
BuildRequires:  python-catkin_pkg
BuildRequires:  python-empy
BuildRequires:  python-mock
BuildRequires:  python-nose
BuildRequires:  python2-pyparsing

Requires:       python
Requires:       python-catkin_pkg
Requires:       python2-pyparsing


%description
Low-level build system macros and infrastructure for ROS.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       cmake
Requires:       gmock-devel
Requires:       gtest-devel
Requires:       python-empy
Requires:       python-nose
Requires:       gcc-c++
Requires:       python
Requires:       python-catkin_pkg
Requires:       python-mock
Requires:       python2-pyparsing

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

# substitute shebang before install block because we run the local catkin script
sed -i.orig '/^#!.*python\s*$/ { s/python/python2/ }' ./bin/catkin_make_isolated
touch -r ./bin/catkin_make_isolated.orig ./bin/catkin_make_isolated
rm ./bin/catkin_make_isolated.orig

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



# replace unversioned python shebang
for file in $(grep -rIl '^#!.*python\s*$') ; do
  sed -i.orig '/^#!.*python\s*$/ { s/python/python2/ }' $file
  touch -r $file.orig $file
  rm $file.orig
done

# replace "/usr/bin/env $interpreter" with "/usr/bin/$interpreter"
for interpreter in bash sh python2 python3 ; do
  for file in $(grep -rIl "^#\!.*${interpreter}" %{buildroot}) ; do
    sed -i.orig "s:^#\!\s*/usr/bin/env\s\+${interpreter}.*:#!/usr/bin/${interpreter}:" $file
    touch -r $file.orig $file
    rm $file.orig
  done
done


echo "This is a package automatically generated with rosfed." >> README_FEDORA
echo "See https://pagure.io/ros for more information." >> README_FEDORA
install -p -D -t %{buildroot}/%{_docdir}/%{name} README_FEDORA
echo %{_docdir}/%{name} >> files.list
install -p -D -t %{buildroot}/%{_docdir}/%{name}-devel README_FEDORA
echo %{_docdir}/%{name}-devel >> files_devel.list


%files -f files.list
%files devel -f files_devel.list


%changelog
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
