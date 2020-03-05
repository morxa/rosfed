Name:           ros-diff_drive_controller
Version:        melodic.0.15.0
Release:        3%{?dist}
Summary:        ROS package diff_drive_controller

License:        BSD
URL:            https://github.com/ros-controls/ros_controllers/wiki

Source0:        https://github.com/ros-gbp/ros_controllers-release/archive/release/melodic/diff_drive_controller/0.15.0-0.tar.gz#/ros-melodic-diff_drive_controller-0.15.0-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel

BuildRequires:  ros-melodic-catkin-devel
BuildRequires:  ros-melodic-control_msgs-devel
BuildRequires:  ros-melodic-controller_interface-devel
BuildRequires:  ros-melodic-controller_manager-devel
BuildRequires:  ros-melodic-dynamic_reconfigure-devel
BuildRequires:  ros-melodic-nav_msgs-devel
BuildRequires:  ros-melodic-realtime_tools-devel
BuildRequires:  ros-melodic-rosgraph_msgs-devel
BuildRequires:  ros-melodic-rostest-devel
BuildRequires:  ros-melodic-std_srvs-devel
BuildRequires:  ros-melodic-tf-devel
BuildRequires:  ros-melodic-urdf-devel
BuildRequires:  ros-melodic-xacro-devel

Requires:       ros-melodic-control_msgs
Requires:       ros-melodic-controller_interface
Requires:       ros-melodic-dynamic_reconfigure
Requires:       ros-melodic-nav_msgs
Requires:       ros-melodic-realtime_tools
Requires:       ros-melodic-tf
Requires:       ros-melodic-urdf

Provides:  ros-melodic-diff_drive_controller = 0.15.0-3
Obsoletes: ros-melodic-diff_drive_controller < 0.15.0-3
Obsoletes: ros-kinetic-diff_drive_controller < 0.15.0-3


%description
Controller for a differential drive mobile base.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-melodic-catkin-devel
Requires:       ros-melodic-control_msgs-devel
Requires:       ros-melodic-controller_interface-devel
Requires:       ros-melodic-controller_manager-devel
Requires:       ros-melodic-dynamic_reconfigure-devel
Requires:       ros-melodic-nav_msgs-devel
Requires:       ros-melodic-realtime_tools-devel
Requires:       ros-melodic-rosgraph_msgs-devel
Requires:       ros-melodic-rostest-devel
Requires:       ros-melodic-std_srvs-devel
Requires:       ros-melodic-tf-devel
Requires:       ros-melodic-urdf-devel
Requires:       ros-melodic-xacro-devel

Provides: ros-melodic-diff_drive_controller-devel = 0.15.0-3
Obsoletes: ros-melodic-diff_drive_controller-devel < 0.15.0-3
Obsoletes: ros-kinetic-diff_drive_controller-devel < 0.15.0-3

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
  --pkg diff_drive_controller




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
* Mon Jul 22 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.15.0-3
- Remove obsolete python2 dependencies
* Sun Jul 21 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.15.0-2
- Switch to python3
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.15.0-1
- Update to ROS melodic release
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.15.0-1
- Update to ROS melodic release
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.15.0-1
- Update to ROS melodic release
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.15.0-1
- Update to ROS melodic release
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.15.0-1
- Update to ROS melodic release
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.0.15.0-1
- Update to ROS melodic release
