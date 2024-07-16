#!/bin/bash

wait_for () {
    echo "waiting for $1:$2"
    for _ in `seq 0 100`; do
        (echo > /dev/tcp/$1/$2) >/dev/null 2>&1
        if [[ $? -eq 0 ]]; then
            echo "$1:$2 accepts connections"
            break
        fi
        sleep 1
    done
}

wait_for_mongo() {
  wait_for "${MONGO_HOST}" "${MONGO_PORT}"
}

update_python_path() {
  export PYTHONPATH="$PYTHONPATH:/src/app"
}


case "$ENV" in
"LINT")
    echo '===RUN MYPY===' && mypy .
    echo '===RUN RUFF===' && ruff check --config ./ruff.toml
    echo '===RUN BANDIT===' && bandit .
    echo '===RUN SAFETY CHECK===' && safety check --full-report --ignore 70612
    ;;
"TEST")
    wait_for_mongo
    pytest .
    ;;
"DEV")
    update_python_path
    wait_for_mongo
    uvicorn app.main:main_app --reload --host 0.0.0.0 --port 8000
    ;;
"PRODUCTION")
    update_python_path
    wait_for_mongo
    gunicorn --config gunicorn.conf.py app.main:main_app --reload --capture-output --log-level info --access-logfile -
    ;;
*)
    echo "NO ENV SPECIFIED!"
    exit 1
    ;;
esac