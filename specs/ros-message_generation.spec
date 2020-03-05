Name:           ros-message_generation
Version:        melodic.0.4.1
Release:        1%{?dist}
Summary:        ROS package message_generation

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/message_generation-release/archive/release/melodic/message_generation/0.4.1-1.tar.gz#/ros-melodic-message_generation-0.4.1-source0.tar.gz


BuildArch: noarch

# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel

BuildRequires:  ros-melodic-catkin-devel

Requires:       ros-melodic-gencpp
Requires:       ros-melodic-geneus
Requires:       ros-melodic-genlisp
Requires:       ros-melodic-genmsg
Requires:       ros-melodic-gennodejs
Requires:       ros-melodic-genpy

Provides:  ros-melodic-message_generation = 0.4.1-1
Obsoletes: ros-melodic-message_generation < 0.4.1-1
Obsoletes: ros-kinetic-message_generation < 0.4.1-1


%description
Package modeling the build-time dependencies for generating language
bindings of messages.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       ros-melodic-catkin-devel
Requires:       ros-melodic-gencpp-devel
Requires:       ros-melodic-geneus-devel
Requires:       ros-melodic-genlisp-devel
Requires:       ros-melodic-genmsg-devel
Requires:       ros-melodic-gennodejs-devel
Requires:       ros-melodic-genpy-devel

Provides: ros-melodic-message_generation-devel = 0.4.1-1
Obsoletes: ros-melodic-message_generation-devel < 0.4.1-1
Obsoletes: ros-kinetic-message_generation-devel < 0.4.1-1

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
for f in $(grep -rl python .) ; do
  sed -i.orig '/^#!.*python\s*$/ { s/python/python3/ }' $f
  touch -r $f.orig $f
  rm $f.orig
done

DESTDIR=%{buildroot} ; export DESTDIR


catkin_make_isolated \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCATKIN_ENABLE_TESTING=OFF \
  -DPYTHON_VERSION=%{python3_version} \
  -DPYTHON_VERSION_NODOTS=%{python3_version_nodots} \
  --source . \
  --install \
  --install-space %{_libdir}/ros/ \
  --pkg message_generation




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,local_setup*,setup*,env.sh}

touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files_devel.list

find . -maxdepth 1 -type f -iname "*readme*" | sed "s:^:%%doc :" >> files.list
find . -maxdepth 1 -type f -iname "*license*" | sed "s:^:%%license :" >> files.list



# replace cmake python macro in shebang
for file in $(grep -rIl '^#!.*@PYTHON_EXECUTABLE@*$' %{buildroot}) ; do
  sed -i.orig 's:^#!\s*@PYTHON_EXECUTABLE@\s*:%{__python3}:' $file
  touch -r $file.orig $file
  rm $file.orig
done

# replace unversioned python shebang
for file in $(grep -rIl '^#!.*python\s*$' %{buildroot}) ; do
  sed -i.orig '/^#!.*python\s*$/ { s/python/python3/ }' $file
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
install -m 0644 -p -D -t %{buildroot}/%{_docdir}/%{name} README_FEDORA
echo %{_docdir}/%{name} >> files.list
install -m 0644 -p -D -t %{buildroot}/%{_docdir}/%{name}-devel README_FEDORA
echo %{_docdir}/%{name}-devel >> files_devel.list


%files -f files.list
%files devel -f files_devel.list


%changelog
* Wed Mar 04 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.4.1-1
- Update to latest release
* Mon Jul 22 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.4.0-3
- Remove obsolete python2 dependencies
* Sun Jul 21 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.4.0-2
- Switch to python3
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.4.0-1
- Update to ROS melodic release
* Fri Jul 12 2019 Till Hofmann <thofmann@fedoraproject.org> - 0.4.0-12
- Remove ROS distro from package name
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.0-11
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.0-10
- devel also requires: the devel package of each run dependency
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.0-9
- Also add upstream's exec_depend as Requires:
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.0-8
- Add corresponding devel Requires: for the package's BRs and Rs
* Mon May 14 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.0-7
- Update to latest release, rebuild for F28
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.0-6
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.0-5
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.0-4
- Add Recommends: for all BRs to the devel subpackage
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.4.0-3
- Split devel package
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.4.0-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.4.0-1
- Update auto-generated Spec file
