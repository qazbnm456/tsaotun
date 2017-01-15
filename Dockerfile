FROM pypy:2-onbuild
RUN pypy setup.py install
ENTRYPOINT [ "pypy", "/usr/local/bin/tsaotun" ]
