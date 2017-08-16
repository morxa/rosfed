Name:           ros-kinetic-diagnostic_analysis
Version:        1.9.2
Release:        1%{?dist}
Summary:        ROS package diagnostic_analysis

License:        BSD
URL:            http://www.ros.org/wiki/diagnostics_analysis

Source0:        https://github.com/ros-gbp/diagnostics-release/archive/release/kinetic/diagnostic_analysis/1.9.2-0.tar.gz#/ros-kinetic-diagnostic_analysis-1.9.2-source0.tar.gz


BuildArch: noarch

BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-diagnostic_msgs
BuildRequires:  ros-kinetic-rosbag
BuildRequires:  ros-kinetic-roslib
BuildRequires:  ros-kinetic-rostest

Requires:       ros-kinetic-diagnostic_msgs
Requires:       ros-kinetic-rosbag
Requires:       ros-kinetic-roslib

%description
The diagnostic_analysis package can convert a log of diagnostics data
into a series of CSV files. Robot logs are recorded with rosbag, and
can be processed offline using the scripts in this package.


%prep

%setup -c -T
tar --strip-components=1 -xf %{SOURCE0}

%build
# nothing to do here


%install
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
FFLAGS="${FFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FFLAGS ; \
FCFLAGS="${FCFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FCFLAGS ; \
%{?__global_ldflags:LDFLAGS="${LDFLAGS:-%__global_ldflags}" ; export LDFLAGS ;} \


source %{_libdir}/ros/setup.bash

DESTDIR=%{buildroot} ; export DESTDIR

catkin_make_isolated \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  --source . \
  --install \
  --install-space %{_libdir}/ros/ \
  --pkg diagnostic_analysis

rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,setup*,env.sh}

find %{buildroot}/%{_libdir}/ros/{bin,etc,include,lib/pkgconfig,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list


find . -maxdepth 1 -type f -iname "*readme*" | sed "s:^:%%doc :" >> files.list
find . -maxdepth 1 -type f -iname "*license*" | sed "s:^:%%license :" >> files.list

%files -f files.list



%changelog
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.9.2-1
- Update auto-generated Spec file
