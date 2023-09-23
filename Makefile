BIN=background-gallery-setter
SRC := $(wildcard *.py)

.PHONY: clean

${BIN}: ${SRC}
	python3 -m zipapp src/ -m "main:main" -p "/usr/bin/env python3" -o ${BIN}

install: ${BIN}
	install -m 744 ${BIN} ${HOME}/.local/bin/

clean:
	rm -rf __pycache__ ${BIN}

