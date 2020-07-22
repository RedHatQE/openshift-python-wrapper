#!/bin/bash -e

python=python3

main() {
    TARGET="$0"
    TARGET="${TARGET#./}"
    TARGET="${TARGET%.*}"
    TARGET="${TARGET#*.}"
    echo "TARGET=$TARGET"

    export PATH="$PATH:/usr/local/bin"

    case "${TARGET}" in
        "check" )
            check
            ;;
        * )
            echo "Unknown target"
            exit 1
            ;;
        esac
}

check() {
    $python -m pip install tox
    make check
}


[[ "${BASH_SOURCE[0]}" == "$0" ]] && main "$@"
