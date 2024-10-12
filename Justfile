package := 'fastlife'
default_unittest_suite := 'tests/unittests'
default_functest_suite := 'tests/functionals'

export PW_TEST_CONNECT_WS_ENDPOINT := "ws://127.0.0.1:3000"
export CLICOLOR_FORCE := "1"

install:
    poetry install --with dev --with doc

doc:
    cd docs && poetry run make html
    xdg-open docs/build/html/index.html

cleandoc:
    cd docs && poetry run make clean
    rm -rf docs/source/components
    rm -rf docs/source/develop

lint:
    FORCE_COLOR=1 poetry run ruff check .

test: lint mypy unittest functest

buildcss:
    poetry run tailwindcss \
        -i tests/fastlife_app/assets/styles/main.css \
        -o tests/fastlife_app/static/css/main.css

buildiconcss:
    poetry run tailwindcss \
        -c docs/source/iconswall/tailwind.config.js \
        -i docs/source/iconswall/main.css \
        -o docs/source/iconswall/iconwall.css
    echo "<style>" > docs/source/iconswall/IconsCss.jinja
    cat docs/source/iconswall/iconwall.css >> docs/source/iconswall/IconsCss.jinja
    echo "</style>" >> docs/source/iconswall/IconsCss.jinja

buildicons:
    poetry run scripts/build_heroicon_tags.py


compiletestlocales:
    poetry run pybabel extract \
        --output tests/fastlife_app/locales/fastlife_test.pot \
        --mapping=tests/fastlife_app/locales/extraction.ini \
        .

    poetry run pybabel update \
        --domain fastlife_test \
        --input-file tests/fastlife_app/locales/fastlife_test.pot \
        --output-dir tests/fastlife_app/locales \
        --previous \
        tests/fastlife_app

    poetry run pybabel compile \
        --domain fastlife_test \
        --directory tests/fastlife_app/locales


    poetry run pybabel update \
        --domain form_error \
        --input-file tests/fastlife_app/locales/form_error.pot \
        --output-dir tests/fastlife_app/locales \
        --previous \
        tests/fastlife_app

    poetry run pybabel compile \
        --domain form_error \
        --directory tests/fastlife_app/locales


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

wip:
    poetry run behave --tags=wip --no-capture tests/functionals/

funcdevtest:
    poetry run behave --tags=dev --no-capture tests/functionals/

showicons:
    poetry run behave --tags=icons --no-capture tests/functionals/

showopenapi:
    poetry run behave --tags=openapi --no-capture tests/functionals/

mypy:
    poetry run mypy src/ tests/

fmt:
    poetry run ruff check --fix .
    poetry run ruff format src tests

black: fmt
    echo "$(tput setaf 3)Warning: Use 'just fmt' instead$(tput setaf 7)"

gh-pages:
    poetry export --with doc -f requirements.txt -o docs/requirements.txt --without-hashes

release major_minor_patch: test gh-pages && changelog
    poetry version {{major_minor_patch}}
    poetry install

changelog:
    poetry run python scripts/write_changelog.py
    cat CHANGELOG.md >> CHANGELOG.md.new
    rm CHANGELOG.md
    mv CHANGELOG.md.new CHANGELOG.md
    $EDITOR CHANGELOG.md

publish:
    git commit -am "Release $(poetry version -s)"
    poetry build
    poetry publish
    git push
    git tag "$(poetry version -s)"
    git push origin "$(poetry version -s)"
