Name:           ros-theora_image_transport
Version:        noetic.1.14.0
Release:        2%{?dist}
Summary:        ROS package theora_image_transport

License:        BSD
URL:            http://www.ros.org/wiki/image_transport_plugins

Source0:        https://github.com/ros-gbp/image_transport_plugins-release/archive/release/noetic/theora_image_transport/1.14.0-1.tar.gz#/ros-noetic-theora_image_transport-1.14.0-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel
BuildRequires:  python-unversioned-command

BuildRequires:  libogg-devel
BuildRequires:  libtheora-devel
BuildRequires:  lz4-devel
BuildRequires:  opencv-devel
BuildRequires:  poco-devel
BuildRequires:  tinyxml-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  ros-noetic-catkin-devel
BuildRequires:  ros-noetic-cv_bridge-devel
BuildRequires:  ros-noetic-dynamic_reconfigure-devel
BuildRequires:  ros-noetic-image_transport-devel
BuildRequires:  ros-noetic-message_generation-devel
BuildRequires:  ros-noetic-pluginlib-devel
BuildRequires:  ros-noetic-rosbag-devel
BuildRequires:  ros-noetic-std_msgs-devel

Requires:       ros-noetic-cv_bridge
Requires:       ros-noetic-dynamic_reconfigure
Requires:       ros-noetic-image_transport
Requires:       ros-noetic-message_runtime
Requires:       ros-noetic-pluginlib
Requires:       ros-noetic-rosbag
Requires:       ros-noetic-std_msgs

Provides:  ros-noetic-theora_image_transport = 1.14.0-2
Obsoletes: ros-noetic-theora_image_transport < 1.14.0-2
Obsoletes: ros-kinetic-theora_image_transport < 1.14.0-2



%description
Theora_image_transport provides a plugin to image_transport for
transparently sending an image stream encoded with the Theora codec.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-noetic-catkin-devel
Requires:       libogg-devel
Requires:       libtheora-devel
Requires:       lz4-devel
Requires:       opencv-devel
Requires:       poco-devel
Requires:       tinyxml-devel
Requires:       tinyxml2-devel
Requires:       ros-noetic-cv_bridge-devel
Requires:       ros-noetic-dynamic_reconfigure-devel
Requires:       ros-noetic-image_transport-devel
Requires:       ros-noetic-message_generation-devel
Requires:       ros-noetic-pluginlib-devel
Requires:       ros-noetic-rosbag-devel
Requires:       ros-noetic-std_msgs-devel
Requires:       ros-noetic-message_runtime-devel

Provides: ros-noetic-theora_image_transport-devel = 1.14.0-2
Obsoletes: ros-noetic-theora_image_transport-devel < 1.14.0-2
Obsoletes: ros-kinetic-theora_image_transport-devel < 1.14.0-2


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
%py3_shebang_fix .

DESTDIR=%{buildroot} ; export DESTDIR


catkin_make_isolated \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCATKIN_ENABLE_TESTING=OFF \
  -DPYTHON_VERSION=%{python3_version} \
  -DPYTHON_VERSION_NODOTS=%{python3_version_nodots} \
  --source . \
  --install \
  --install-space %{_libdir}/ros/ \
  --pkg theora_image_transport




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,local_setup*,setup*,env.sh}

touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig,share/theora_image_transport/cmake} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files_devel.list

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
* Tue Feb 23 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.14.0-2
- Modernize python shebang replacement
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.14.0-1
- Upgrade to noetic
* Mon Jul 22 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.9.5-13
- Remove obsolete python2 dependencies
* Sun Jul 21 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.9.5-12
- Switch to python3
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.9.5-11
- Update to ROS melodic release
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.9.5-10
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.9.5-9
- devel also requires: the devel package of each run dependency
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.9.5-8
- Also add upstream's exec_depend as Requires:
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.9.5-7
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.9.5-6
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.9.5-5
- Add Recommends: for all BRs to the devel subpackage
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.9.5-4
- Split devel package
* Thu Nov 23 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.9.5-3
- Build against system opencv3 instead of ros-kinetic-opencv
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.9.5-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.9.5-1
- Update auto-generated Spec file
