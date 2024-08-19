package := 'fastlife'
default_unittest_suite := 'tests/unittests'
default_functest_suite := 'tests/functionals'

export PW_TEST_CONNECT_WS_ENDPOINT := "ws://127.0.0.1:3000"

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

buildicons:
    poetry run scripts/build_heroicon_tags.py


unittest test_suite=default_unittest_suite:
    poetry run pytest -sxv {{test_suite}}

lf:
    poetry run pytest -sxvvv --lf

cov test_suite=default_unittest_suite:
    rm -f .coverage
    rm -rf htmlcov
    poetry run pytest --cov-report=html --cov={{package}} {{test_suite}}
    xdg-open htmlcov/index.html

# start the playwright server in a docker container
# to honnort PW_TEST_CONNECT_WS_ENDPOINT for functional tests
playwrightserver:
    docker run -p 3000:3000 --rm --init -it mcr.microsoft.com/playwright:v1.41.0-jammy /bin/sh -c "cd /home/pwuser && npx -y playwright@1.41.0 run-server --port 3000 --host 0.0.0.0"

functest test_suite=default_functest_suite:
    poetry run behave --tags=-dev --tags=-icons --no-capture {{test_suite}}


funcdevtest:
    poetry run behave --tags=dev --no-capture tests/functionals/

showicons:
    poetry run behave --tags=icons --no-capture tests/functionals/

mypy:
    poetry run mypy src/ tests/

black:
    poetry run isort .
    poetry run black .

gh-pages:
    # poetry export --with dev -f requirements.txt -o docs/requirements.txt --without-hashes
    echo "No docs built"

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
