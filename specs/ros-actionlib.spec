Name:           ros-actionlib
Version:        noetic.1.13.2
Release:        1%{?dist}
Summary:        ROS package actionlib

License:        BSD
URL:            http://www.ros.org/wiki/actionlib

Source0:        https://github.com/ros-gbp/actionlib-release/archive/release/noetic/actionlib/1.13.2-1.tar.gz#/ros-noetic-actionlib-1.13.2-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel

BuildRequires:  boost-devel
BuildRequires:  ros-noetic-actionlib_msgs-devel
BuildRequires:  ros-noetic-catkin-devel
BuildRequires:  ros-noetic-message_generation-devel
BuildRequires:  ros-noetic-roscpp-devel
BuildRequires:  ros-noetic-rosnode-devel
BuildRequires:  ros-noetic-rospy-devel
BuildRequires:  ros-noetic-rostest-devel
BuildRequires:  ros-noetic-rosunit-devel
BuildRequires:  ros-noetic-std_msgs-devel

Requires:       ros-noetic-actionlib_msgs
Requires:       ros-noetic-message_runtime
Requires:       ros-noetic-roscpp
Requires:       ros-noetic-rospy
Requires:       ros-noetic-rostest
Requires:       ros-noetic-std_msgs

Provides:  ros-noetic-actionlib = 1.13.2-1
Obsoletes: ros-noetic-actionlib < 1.13.2-1
Obsoletes: ros-kinetic-actionlib < 1.13.2-1



%description
The actionlib stack provides a standardized interface for interfacing
with preemptable tasks. Examples of this include moving the base to a
target location, performing a laser scan and returning the resulting
point cloud, detecting the handle of a door, etc.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-noetic-catkin-devel
Requires:       boost-devel
Requires:       ros-noetic-actionlib_msgs-devel
Requires:       ros-noetic-message_generation-devel
Requires:       ros-noetic-roscpp-devel
Requires:       ros-noetic-rosnode-devel
Requires:       ros-noetic-rospy-devel
Requires:       ros-noetic-rostest-devel
Requires:       ros-noetic-rosunit-devel
Requires:       ros-noetic-std_msgs-devel
Requires:       ros-noetic-message_runtime-devel

Provides: ros-noetic-actionlib-devel = 1.13.2-1
Obsoletes: ros-noetic-actionlib-devel < 1.13.2-1
Obsoletes: ros-kinetic-actionlib-devel < 1.13.2-1


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
  --pkg actionlib




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
* Thu Sep 10 2020 Nicolas Limpert <limpert@fh-aachen.de> - noetic.1.13.2-1
- Update to latest release
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.13.1-1
- Upgrade to noetic
* Thu Sep 12 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.12.0-1
- Update to latest release
* Tue Jul 23 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.11.13-4
- Fix type conversion in boost::posix_time
* Mon Jul 22 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.11.13-3
- Remove obsolete python2 dependencies
* Sun Jul 21 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.11.13-2
- Switch to python3
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.11.13-1
- Update to ROS melodic release
* Fri Jul 12 2019 Till Hofmann <thofmann@fedoraproject.org> - 1.11.13-7
- Remove ROS distro from package name
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.13-6
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.13-5
- devel also requires: the devel package of each run dependency
* Wed May 16 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.13-4
- Fix dependency on wxpython
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.13-3
- Also add upstream's exec_depend as Requires:
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.13-2
- Add corresponding devel Requires: for the package's BRs and Rs
* Mon May 14 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.13-1
- Update to latest release, rebuild for F28
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.12-4
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.12-3
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.12-2
- Add Recommends: for all BRs to the devel subpackage
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.12-1
- Split devel package
* Sun Nov 19 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.11.11-1
- Update to latest release
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.11.9-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.11.9-1
- Update auto-generated Spec file
