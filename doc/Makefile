# Copyright © 2014-2019 Jakub Wilk <jwilk@jwilk.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

export LC_ALL=C

rst2man = $(notdir $(shell command -v rst2man || echo rst2man.py))
rst2xml = $(notdir $(shell command -v rst2xml || echo rst2xml.py))

exe = anorack

.PHONY: all
all: $(exe).1

$(exe).1: manpage.rst
	$(rst2man) --input-encoding=UTF-8 < $(<) > $(@).tmp
	perl -pi -e '/^[.]BI\b/ and s/\\fP/\\fR/g' $(@).tmp  # work-around for https://bugs.debian.org/806601
	perl -ni -e 'print unless /^[.]\\" vim:/' $(@).tmp
	mv $(@).tmp $(@)

.PHONY: check
check: check-changelog check-rst

.PHONY: check-changelog
check-changelog: changelog
	dpkg-parsechangelog -l$(<) --all 2>&1 >/dev/null | { ! grep .; }

.PHONY: check-rst
check-rst:
	ls README *.rst | xargs -t -I{} $(rst2xml) --input-encoding=UTF-8 --strict {} /dev/null

.PHONY: clean
clean:
	rm -f $(exe).1 *.tmp

.error = GNU make is required

# vim:ts=4 sts=4 sw=4 noet
