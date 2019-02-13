# Create a source distribution in gztar format
sources:
	python setup.py sdist --formats=gztar
	cp dist/*.gz .

# Install everything from build directory
install:
	python setup.py install

# Create an RPM distribution
rpm:
	python setup.py bdist_rpm

# Clean up temporary files from 'build' command
clean:
	python setup.py clean
	rm -rf *.gz dist ec2sys_autotune.egg-info build
