Name:           ros-kinetic-moveit_ros_perception
Version:        0.9.15
Release:        1%{?dist}
Summary:        ROS package moveit_ros_perception

License:        BSD
URL:            http://moveit.ros.org

Source0:        https://github.com/ros-gbp/moveit-release/archive/release/kinetic/moveit_ros_perception/0.9.15-0.tar.gz#/ros-kinetic-moveit_ros_perception-0.9.15-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  eigen3-devel
BuildRequires:  fcl-devel
BuildRequires:  freeglut-devel
BuildRequires:  glew-devel
BuildRequires:  mesa-libGL-devel mesa-libGLU-devel
BuildRequires:  opencv-devel
BuildRequires:  poco-devel
BuildRequires:  tinyxml-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  urdfdom-devel
BuildRequires:  ros-kinetic-catkin-devel
BuildRequires:  ros-kinetic-cv_bridge-devel
BuildRequires:  ros-kinetic-image_transport-devel
BuildRequires:  ros-kinetic-message_filters-devel
BuildRequires:  ros-kinetic-moveit_core-devel
BuildRequires:  ros-kinetic-moveit_msgs-devel
BuildRequires:  ros-kinetic-octomap-devel
BuildRequires:  ros-kinetic-pluginlib-devel
BuildRequires:  ros-kinetic-rosconsole-devel
BuildRequires:  ros-kinetic-roscpp-devel
BuildRequires:  ros-kinetic-sensor_msgs-devel
BuildRequires:  ros-kinetic-tf-devel
BuildRequires:  ros-kinetic-tf_conversions-devel
BuildRequires:  ros-kinetic-urdf-devel

Requires:       ros-kinetic-cv_bridge
Requires:       ros-kinetic-image_transport
Requires:       ros-kinetic-message_filters
Requires:       ros-kinetic-moveit_core
Requires:       ros-kinetic-moveit_msgs
Requires:       ros-kinetic-octomap
Requires:       ros-kinetic-pluginlib
Requires:       ros-kinetic-rosconsole
Requires:       ros-kinetic-roscpp
Requires:       ros-kinetic-sensor_msgs
Requires:       ros-kinetic-tf
Requires:       ros-kinetic-tf_conversions
Requires:       ros-kinetic-urdf


%description
Components of MoveIt! connecting to perception

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-kinetic-catkin-devel
Requires:       eigen3-devel
Requires:       fcl-devel
Requires:       freeglut-devel
Requires:       glew-devel
Requires:       mesa-libGL-devel mesa-libGLU-devel
Requires:       opencv-devel
Requires:       poco-devel
Requires:       tinyxml-devel
Requires:       tinyxml2-devel
Requires:       urdfdom-devel
Requires:       ros-kinetic-cv_bridge-devel
Requires:       ros-kinetic-image_transport-devel
Requires:       ros-kinetic-message_filters-devel
Requires:       ros-kinetic-moveit_core-devel
Requires:       ros-kinetic-moveit_msgs-devel
Requires:       ros-kinetic-octomap-devel
Requires:       ros-kinetic-pluginlib-devel
Requires:       ros-kinetic-rosconsole-devel
Requires:       ros-kinetic-roscpp-devel
Requires:       ros-kinetic-sensor_msgs-devel
Requires:       ros-kinetic-tf-devel
Requires:       ros-kinetic-tf_conversions-devel
Requires:       ros-kinetic-urdf-devel

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
  --pkg moveit_ros_perception




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
* Wed Nov 07 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.9.15-1
- Update to latest release
* Wed May 30 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.9.12-1
- Update to latest release
* Thu Jan 18 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.9.11-1
- Initial package
