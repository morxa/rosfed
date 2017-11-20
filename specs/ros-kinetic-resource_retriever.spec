Name:           ros-kinetic-resource_retriever
Version:        1.12.3
Release:        3%{?dist}
Summary:        ROS package resource_retriever

License:        BSD
URL:            http://ros.org/wiki/resource_retriever

Source0:        https://github.com/ros-gbp/resource_retriever-release/archive/release/kinetic/resource_retriever/1.12.3-0.tar.gz#/ros-kinetic-resource_retriever-1.12.3-source0.tar.gz



BuildRequires:  gtest-devel
BuildRequires:  libcurl-devel curl
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-rosconsole
BuildRequires:  ros-kinetic-roslib

Requires:       python-rospkg
Requires:       ros-kinetic-rosconsole
Requires:       ros-kinetic-roslib

%description
This package retrieves data from url-format files such as http://,
ftp://, package:// file://, etc., and loads the data into memory. The
package:// url for ros packages is translated into a local file://
url. The resourse retriever was initially designed to load mesh files
into memory, but it can be used for any type of data. The resource
retriever is based on the the libcurl library.


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
  --pkg resource_retriever

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
* Mon Nov 20 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.12.3-3
- Add missing BR on gtest-devel
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.12.3-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.12.3-1
- Update auto-generated Spec file
