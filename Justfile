package := 'fastlife'
default_unittest_suite := 'tests/unittests'
default_functest_suite := 'tests/functionals'

install:
    poetry install

doc:
    cd docs && poetry run make html
    xdg-open docs/build/html/index.html

cleandoc:
    cd docs && poetry run make clean

lint:
    poetry run flake8 && echo "$(tput setaf 10)Success: no lint issue$(tput setaf 7)"

test: lint mypy unittest functest

buildcss:
    poetry run tailwindcss \
        -i tests/fastlife_app/assets/styles/main.css \
        -o tests/fastlife_app/static/css/main.css

unittest test_suite=default_unittest_suite:
    poetry run pytest -sxv {{test_suite}}

lf:
    poetry run pytest -sxvvv --lf

cov test_suite=default_unittest_suite:
    rm -f .coverage
    rm -rf htmlcov
    poetry run pytest --cov-report=html --cov={{package}} {{test_suite}}
    xdg-open htmlcov/index.html


functest test_suite=default_functest_suite:
    poetry run behave --tags=-dev --no-capture {{test_suite}}


funcdevtest:
    poetry run behave --tags=dev --no-capture tests/functionals/

mypy:
    poetry run mypy src/ tests/

black:
    poetry run isort .
    poetry run black .

gh-pages:
    poetry export --with dev -f requirements.txt -o docs/requirements.txt --without-hashes

release major_minor_patch: test gh-pages && changelog
    poetry version {{major_minor_patch}}
    poetry install

changelog:
    poetry run python scripts/write_changelog.py
    cat CHANGELOG.rst >> CHANGELOG.rst.new
    rm CHANGELOG.rst
    mv CHANGELOG.rst.new CHANGELOG.rst
    $EDITOR CHANGELOG.rst

publish:
    git commit -am "Release $(poetry version -s)"
    poetry build
    poetry publish
    git push
    git tag "$(poetry version -s)"
    git push origin "$(poetry version -s)"
