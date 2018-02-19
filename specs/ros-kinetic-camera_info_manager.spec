Name:           ros-kinetic-camera_info_manager
Version:        1.11.13
Release:        3%{?dist}
Summary:        ROS package camera_info_manager

License:        BSD
URL:            http://ros.org/wiki/camera_info_manager

Source0:        https://github.com/ros-gbp/image_common-release/archive/release/kinetic/camera_info_manager/1.11.13-0.tar.gz#/ros-kinetic-camera_info_manager-1.11.13-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  boost-devel
BuildRequires:  gtest-devel
BuildRequires:  poco-devel
BuildRequires:  tinyxml-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  ros-kinetic-camera_calibration_parsers-devel
BuildRequires:  ros-kinetic-catkin-devel
BuildRequires:  ros-kinetic-image_transport-devel
BuildRequires:  ros-kinetic-roscpp-devel
BuildRequires:  ros-kinetic-roslib-devel
BuildRequires:  ros-kinetic-rostest-devel
BuildRequires:  ros-kinetic-sensor_msgs-devel

Requires:       ros-kinetic-camera_calibration_parsers
Requires:       ros-kinetic-image_transport
Requires:       ros-kinetic-roscpp
Requires:       ros-kinetic-roslib
Requires:       ros-kinetic-sensor_msgs


%description
This package provides a C++ interface for camera calibration
information. It provides CameraInfo, and handles SetCameraInfo service
requests, saving and restoring the camera calibration data.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-kinetic-catkin

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
  --pkg camera_info_manager




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


echo "This is a package automatically generated with rosfed." >> README_FEDORA
echo "See https://pagure.io/ros for more information." >> README_FEDORA
install -p -D -t %{buildroot}/%{_docdir}/%{name} README_FEDORA
echo %{_docdir}/%{name} >> files.list
install -p -D -t %{buildroot}/%{_docdir}/%{name}-devel README_FEDORA
echo %{_docdir}/%{name}-devel >> files_devel.list


%files -f files.list
%files devel -f files_devel.list


%changelog
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.13-3
- Split devel package
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.11.13-2
- Split devel package
* Sun Nov 19 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.11.13-1
- Update to latest release
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.11.12-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.11.12-1
- Update auto-generated Spec file
