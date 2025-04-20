rm -r dist/
rm -r src/pygcp.egg-info/
python3 -m build
python3 -m twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ --no-deps pygcp==1.2.2 --break-system- --force-reinstall