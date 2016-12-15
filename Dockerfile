FROM pypy:2-onbuild
ENTRYPOINT [ "pypy", "./dokcer" ]
