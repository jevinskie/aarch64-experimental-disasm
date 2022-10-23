#!/usr/bin/env sh

mkdir -p mra-2022-09
pushd mra-2022-09
wget -c https://archive.org/download/isa-a-64-xml-a-profile-2022-09.tar.gz/ISA_A64_xml_A_profile-2022-09.tar.gz
tar xzf ISA_A64_xml_A_profile-2022-09.tar.gz
popd
ln -s mra-2022-09/ISA_A64_xml_A_profile-2022-09_OPT mra-a64-xml
