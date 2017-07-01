#! /bin/sh
#
# make_noarch.sh
# Copyright (C) 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de>
#
# Distributed under terms of the MIT license.
#


echo "noarch: true" >> cfg/${1}.yaml
./generate_ros_spec_file.py $1
rpmbuild -bs specs/ros-kinetic-$1.spec

