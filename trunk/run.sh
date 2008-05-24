rm -rf dist build
python2.5 setup.py build_ext
sed s/:from/:From/ lib/ytnef.py > tmp.py
mv tmp.py lib/ytnef.py
python2.5 setup.py install --force
python2.5 ./test/ytnef.py
