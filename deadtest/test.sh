#!/bin/bash


function _test() {
    #
    # run server in background with address localhost:8000 (load current dir to server)
    # ls: test.sh, test.html
    #
    python -m SimpleHTTPServer &
    # wait server
    sleep 2
    # 127.0.0.1
    ifcon=($(ifconfig|awk '{print $2}'|grep -i '\w\W\w\W'))
    # http://127.0.0.1/test.html
    data=($(curl "$ifcon:8000/test.html"|grep -i "var data = {"))
    # var data = {'k': 1, 'i': 9, 'r': 9, 'a': 7}¬
    echo "GOT DATA: ${data[@]}"
    # kill python server
    kill "$!"
}


_test
