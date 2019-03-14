Name:           ros-kinetic-warehouse_ros
Version:        0.9.2
Release:        1%{?dist}
Summary:        ROS package warehouse_ros

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/warehouse_ros-release/archive/release/kinetic/warehouse_ros/0.9.2-0.tar.gz#/ros-kinetic-warehouse_ros-0.9.2-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  gtest-devel
BuildRequires:  ros-kinetic-catkin-devel
BuildRequires:  ros-kinetic-geometry_msgs-devel
BuildRequires:  ros-kinetic-pluginlib-devel
BuildRequires:  ros-kinetic-roscpp-devel
BuildRequires:  ros-kinetic-rostest-devel
BuildRequires:  ros-kinetic-rostime-devel
BuildRequires:  ros-kinetic-std_msgs-devel
BuildRequires:  ros-kinetic-tf-devel

Requires:       ros-kinetic-geometry_msgs
Requires:       ros-kinetic-pluginlib
Requires:       ros-kinetic-roscpp
Requires:       ros-kinetic-rostime
Requires:       ros-kinetic-std_msgs
Requires:       ros-kinetic-tf


%description
Persistent storage of ROS messages

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-kinetic-catkin-devel
Requires:       gtest-devel
Requires:       ros-kinetic-geometry_msgs-devel
Requires:       ros-kinetic-pluginlib-devel
Requires:       ros-kinetic-roscpp-devel
Requires:       ros-kinetic-rostest-devel
Requires:       ros-kinetic-rostime-devel
Requires:       ros-kinetic-std_msgs-devel
Requires:       ros-kinetic-tf-devel

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

DESTDIR=%{buildroot} ; export DESTDIR


catkin_make_isolated \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCATKIN_ENABLE_TESTING=OFF \
  --source . \
  --install \
  --install-space %{_libdir}/ros/ \
  --pkg warehouse_ros




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,setup*,env.sh}

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
* Thu Mar 14 2019 Till Hofmann <thofmann@fedoraproject.org> - 0.9.2-1
- Update to latest release
* Wed Nov 07 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.9.1-1
- Update to latest release
* Thu Jan 18 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.9.0-1
- Initial package
