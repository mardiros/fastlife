package := 'fastlife'
default_unittest_suite := 'tests/unittests'
default_functest_suite := 'tests/functionals'

# export PW_TEST_CONNECT_WS_ENDPOINT := "ws://127.0.0.1:3000"
export CLICOLOR_FORCE := "1"
export RUST_BACKTRACE := "1"
export RUST_LOG := "xcore=warn"

install:
    uv sync --group dev

update:
    uv sync --all-groups

upgrade:
    uv sync --all-groups --upgrade


doc:
    uv sync --group dev --group doc
    cd docs && uv run make html
    xdg-open docs/build/html/index.html

cleandoc:
    cd docs && uv run make clean
    rm -rf docs/source/components
    rm -rf docs/source/develop

lint:
    uv run ruff check .

test: lint typecheck unittest functest

buildcss:
    uv run tailwindcss \
      -i src/fastlife/assets/source.css \
      -o src/fastlife/assets/dist.css
    uv run tailwindcss \
        -i tests/fastlife_app/assets/styles/main.css \
        -o tests/fastlife_app/static/css/main.css

buildiconcss:
    uv run tailwindcss \
        -c docs/source/iconswall/tailwind.config.js \
        -i docs/source/iconswall/main.css \
        -o docs/source/iconswall/iconwall.css
    echo "<style>" > docs/source/iconswall/IconsCss.jinja
    cat docs/source/iconswall/iconwall.css >> docs/source/iconswall/IconsCss.jinja
    echo "</style>" >> docs/source/iconswall/IconsCss.jinja

buildicons:
    uv run scripts/build_heroicon_tags.py


compiletestlocales:
    uv run pybabel extract \
        --keyword dpgettext:2c,3 --keyword dnpgettext:2c,3,4 \
        --output tests/fastlife_app/locales/messages-py.pot \
        --mapping=tests/fastlife_app/locales/extraction.ini \
        .

    uv run pybabel extract \
        --keyword dpgettext:2c,3 --keyword dnpgettext:2c,3,4 \
        --output tests/fastlife_app/locales/messages-xcomponent.pot \
        --mapping=tests/fastlife_app/locales/extraction_xcomponent.ini \
        .

    msgcat tests/fastlife_app/locales/messages-py.pot \
    tests/fastlife_app/locales/messages-xcomponent.pot \
    -o tests/fastlife_app/locales/fastlife_test.pot

    rm tests/fastlife_app/locales/messages-py.pot
    rm tests/fastlife_app/locales/messages-xcomponent.pot

    uv run pybabel update \
        --domain fastlife_test \
        --input-file tests/fastlife_app/locales/fastlife_test.pot \
        --output-dir tests/fastlife_app/locales \
        --previous \
        tests/fastlife_app

    uv run pybabel compile \
        --domain fastlife_test \
        --directory tests/fastlife_app/locales


unittest test_suite=default_unittest_suite:
    uv run pytest -sxv {{test_suite}}

lf:
    uv run pytest -sxvvv --lf -m "not dev"

cov test_suite=default_unittest_suite:
    rm -f .coverage
    rm -rf htmlcov
    uv run pytest --cov-report=html --cov={{package}} {{test_suite}}
    xdg-open htmlcov/index.html

# start the playwright server in a docker container
# to honnort PW_TEST_CONNECT_WS_ENDPOINT for functional tests
# playwrightserver:
#     docker run -p 3000:3000 --rm --init -it mcr.microsoft.com/playwright:v1.41.0-jammy /bin/sh -c "cd /home/pwuser && npx -y playwright@1.41.0 run-server --port 3000 --host 0.0.0.0"

functest test_suite=default_functest_suite:
    uv run pytest -m "not dev" --browser chromium  -sxv tests/functionals/

wip:
    uv run pytest -m "wip" --headed --browser chromium  -sxv tests/functionals/

funcdevtest:
    uv run pytest -m "experiment" --headed --browser chromium  -sxvvv tests/functionals/

showicons:
    uv run pytest -m "icons" --headed --browser chromium  -sxv tests/functionals/

showopenapi:
    uv run pytest -m "openapi" --headed --browser chromium  -sxv tests/functionals/

typecheck:
    uv run mypy src/ tests/

fmt:
    uv run ruff check --fix .
    uv run ruff format src tests

black: fmt
    echo "$(tput setaf 3)Warning: Use 'just fmt' instead$(tput setaf 7)"

release major_minor_patch: buildcss test && changelog
    uvx --with=pdm,pdm-bump --python-preference system pdm bump {{major_minor_patch}}
    uv sync --frozen --group dev

changelog:
    uv run python scripts/write_changelog.py
    cat CHANGELOG.md >> CHANGELOG.md.new
    rm CHANGELOG.md
    mv CHANGELOG.md.new CHANGELOG.md
    $EDITOR CHANGELOG.md

publish:
    git commit -am "Release $(uv run scripts/get_version.py)"
    git tag "v$(uv run scripts/get_version.py)"
    git push
    git push origin "v$(uv run scripts/get_version.py)"
