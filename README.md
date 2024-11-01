# DEPRECATION NOTICE

This version of `rosfed` only supports ROS1. There is a [fork that supports ROS2](https://github.com/TarikViehmann/rosfed), but this repository will not be updated. Alternatively, you can use the [official RHEL packages](https://docs.ros.org/en/jazzy/Installation/RHEL-Install-RPMs.html).

# rosfed
This repository contains scripts and configurations to generate ROS packages
for Fedora.

If you just want to install ROS, please go to the [ROS COPR](https://copr.fedorainfracloud.org/coprs/thofmann/ros/).

## The Generator

The `rosfed.py` script works as follows:

1. It fetches package information about the upstream ROS package with the
   `rosinstall_generator`. This includes dependencies, license, sources, and
   the version.

   **Note:** It is important to have an updated rosdep database. You can update it
   by executing `rosdep update`.
2. With this information, it generates a SPEC file using the template in
   `./templates/`. The generic template in `./templates/pkg.spec.j2` works for
   most packages. For some packages, the template needs to be modified, in
   which case you can find the per-package template in
   `./templates/$pkgname.spec.j2`. Note that all package-specific templates
   extend the generic base template in `./templates/pkg.spec.j2`.
3. Additional modifications can be done by adding a config file to
   `cfg/$pkgname.yaml`. This allows to add missing build and runtime
   dependencies, filter out some dependencies, add build flags, and make a
   package noarch.
4. Optionally, the package is built in a COPR. The module `copr_build` supports
   building dependency chains.

The `rosfed.py` script uses a default ROS distro, which usually is the latest
one but it may be falling behind in some cases. To know the default ROS distro
the `./rosfed.py --help` command can be used.

A `--distro` option allows to choose a different ROS distro than the default.

### How to add a new package

In the simplest case, run `./rosfed.py $pkgname`, or
`./rosfed.py -r $pkgname` if you want to generate SPEC files
for all dependencies of the given package.

You may need to do the following modifications to the config in
`./cfg/$pkgname.yaml`:

* Make the package noarch by adding `noarch: true`.
* Add dependencies, e.g., a system build dependency to `qt5-qtbase-devel`:

      dependencies:
        build:
          system:
            - qt5-qtbase-devel

* Removing dependencies, e.g., opencv should not require ffmpeg:

      dependencies:
        exclude_run:
          system:
            - ffmpeg
            - ffmpeg-devel

* Add build flags by adding `buildflags: <build_flags>` to the config file.
  Example from opencv:

      build_flags: "--cmake-args -DENABLE_PRECOMPILED_HEADERS=OFF -DWITH_FFMPEG=OFF"

* To build a package with all its missing dependencies (i.e., the package is not
  updated if it already exists), run:

      $ ./rosfed.py -b --copr-owner thofmann --copr-project ros --chroot fedora-rawhide-x86_64 -c Initial package --only-new -r moveit

* To build a single package, run:

      $ ./rosfed.py -b --copr-owner thofmann --copr-project ros --chroot fedora-rawhide-x86_64 moveit_ros_manipulation

* To build the desktop_full stack, run:

      $ ./rosfed.py -b --copr-owner thofmann --copr-project ros --chroot fedora-rawhide-x86_64 -r desktop_full

Additionally, you may need to modify the template by providing a
package-specific template in `./templates/$pkgname.spec.j2`. Have a look at the
existing templates for examples.

It should always be possible to regenerate the SPEC file. Thus, do not modify
the generated SPEC file but instead modify the config and/or template as
necessary. If you need to do a modification that is not possible, please file
an issue.

