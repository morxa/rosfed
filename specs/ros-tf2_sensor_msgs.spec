Name:           ros-tf2_sensor_msgs
Version:        melodic.0.6.5
Release:        1%{?dist}
Summary:        ROS package tf2_sensor_msgs

License:        BSD
URL:            http://www.ros.org/wiki/tf2_ros

Source0:        https://github.com/ros-gbp/geometry2-release/archive/release/melodic/tf2_sensor_msgs/0.6.5-0.tar.gz#/ros-melodic-tf2_sensor_msgs-0.6.5-source0.tar.gz


BuildArch: noarch

# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel

BuildRequires:  eigen3-devel
BuildRequires:  ros-melodic-catkin-devel
BuildRequires:  ros-melodic-cmake_modules-devel
BuildRequires:  ros-melodic-geometry_msgs-devel
BuildRequires:  ros-melodic-rostest-devel
BuildRequires:  ros-melodic-sensor_msgs-devel
BuildRequires:  ros-melodic-tf2-devel
BuildRequires:  ros-melodic-tf2_ros-devel

Requires:       ros-melodic-python_orocos_kdl
Requires:       ros-melodic-rospy
Requires:       ros-melodic-sensor_msgs
Requires:       ros-melodic-tf2
Requires:       ros-melodic-tf2_ros

Provides:  ros-melodic-tf2_sensor_msgs = 0.6.5-1
Obsoletes: ros-melodic-tf2_sensor_msgs < 0.6.5-1
Obsoletes: ros-kinetic-tf2_sensor_msgs < 0.6.5-1


%description
Small lib to transform sensor_msgs with tf. Most notably, PointCloud2

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       eigen3-devel
Requires:       ros-melodic-catkin-devel
Requires:       ros-melodic-cmake_modules-devel
Requires:       ros-melodic-geometry_msgs-devel
Requires:       ros-melodic-rostest-devel
Requires:       ros-melodic-sensor_msgs-devel
Requires:       ros-melodic-tf2-devel
Requires:       ros-melodic-tf2_ros-devel
Requires:       ros-melodic-python_orocos_kdl-devel
Requires:       ros-melodic-rospy-devel

Provides: ros-melodic-tf2_sensor_msgs-devel = 0.6.5-1
Obsoletes: ros-melodic-tf2_sensor_msgs-devel < 0.6.5-1
Obsoletes: ros-kinetic-tf2_sensor_msgs-devel < 0.6.5-1

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
  --pkg tf2_sensor_msgs




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
* Wed Jul 24 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.6.5-1
- Update to latest release
