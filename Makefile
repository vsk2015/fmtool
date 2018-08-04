help:
	@echo "  clean       remove artifacts from running python setup.py install"
	@echo "  archive     creates tar.gz of this project"
	@echo "  package     creates a python package for distribution"
	@echo "  deploy      deploys pack on a remote host, requires arguments user=<username>, host=<ip>, port=<port> and folder=</home/user/>"

clean:
	rm -Rf fmcheck.tar.gz && \
	rm -Rf build *.egg-info dist && \
	rm -Rf ChangeLog && \
	rm -Rf AUTHORS

archive:
	make clean && \
	tar -zcvf ./fmcheck.tar.gz --exclude='.git' --exclude='.env' --exclude='.venv' --exclude='docs' --exclude='fmcheck.tar.gz' .

deploy:
	make archive && \
	cat ./fmcheck.tar.gz | ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -p $(port) $(user)@$(host) \
	"tar -zxvf - -C $(folder)"

package:
	make clean && \
	python setup.py sdist bdist_wheel
