#!/bin/bash
wget http://repo.continuum.io/miniconda/Miniconda-2.0.3-Linux-x86_64.sh -O /tmp/miniconda.sh
chmod 755 /tmp/miniconda.sh
/tmp/miniconda.sh -b
rm -f /tmp/miniconda.sh
echo "export PATH=\$HOME/anaconda/bin:\$PATH" >> $HOME/.bashrc

