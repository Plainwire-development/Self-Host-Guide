.PHONY: check site serve test

site:
	python3 scripts/build-site.py

check: site
	python3 scripts/check-docs.py
	python3 -m unittest discover -s tests -v

serve: site
	python3 -m http.server 8000 -d site

test: check
