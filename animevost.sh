#!/bin/bash

_base_url="http://file.aniland.org/"
_log_urls="used.log"
_folder_name=""
_give_me_name=()
_give_me_seri=()


#
# GET URL, GET NAME FOR DIR,
# MAKE DIR, CHANGE DIR,
# IF DIR NOT EMPTY,
# COUNT DOWNLOADED SERIES,
# DOWNLOAD NOT EXIST SERIES
#


function _check_exists() {
    #
    # MP4 FILES IN CURRENT DIR
    #
    series=($(find -maxdepth 1 -type f -name '*.mp4'))
    echo "${#series[@]}"
}

# _check_exists


function _log_downloaded_urls() {
    #
    # ANIME_NAME: ARRAY(IDS)
    # $1 -> $anime_name
    # $2 -> array of anime series
    #
    echo "$1:$2" >> $_log_urls
}


function _make_folder() {
    #
    # MAKE DIRECTORY LIKE ANIME NAME
    #
    read -p "NAME: " anime_name 

    if [ ! -d "$anime_name" ];
    then
        mkdir "$anime_name" && cd "$anime_name";
    else
        cd "$anime_name"
    fi;
    _folder_name="$anime_name"
}


function _rename_ids() {
    #
    # RENAME ID.MP4 TO NAME.MP4
    #
    idnx=0
    for item in "${_give_me_seri[@]}"
    do
        echo "$item.mp4"
        # rename "$item.mp4" "${_give_me_name[idnx]}.mp4"
        echo "${_give_me_name[idnx]}.mp4"
        idnx=$[ $idnx + 1 ]
    done
}


function _download_series() {
    #
    # DOWNLOAD SERIES LIKE PARALLEL
    #
    sl=0 
    for seri in $@
    do
        if [ $sl -lt 3 ]; then
            wget "http://file.aniland.org/$seri.mp4" &
            sl=$[ $sl + 1 ]
        else
            sleep 3
            wget "http://file.aniland.org/$seri.mp4" &
            sl=0
        fi
    done
}


function _split_data() {
    #
    # SPLIT DATA TO NAME AND ID
    #
    #curl "$1" | grep -i "var data = {" > series.txt
    #data=($(cat series.txt))
    indx=0
    name=()
    seri=()
    ntim=0
    for item in "${data[@]}"
    do
        if [ $indx -gt 2 ]; then
            if [ $ntim -lt 1 ]; then
                name+=("$item")
                ntim=$[ $ntim + 1 ]
            else
                seri+=("$item")
                ntim=0
            fi
        else
            indx=$[ $indx + 1 ]
        fi
    done

    nmn=$(echo ${name[@]}|tr ':' ' '|tr "'" " "|tr '\{' " ")
    _give_me_name=$(echo $nmn|awk "{print $1}")

    srs=$(echo ${seri[@]}|tr ',' ' '|tr '}' " ")
    _give_me_seri=$(echo $srs|awk "{print $1}")
}

# _split_data "$1"
# _make_folder
# _download_series
# _rename_ids
# _log_downloaded_urls















# array = ()
# array+=('fii')
# 
# array[0]
# 
# 
# foo="hello"
# foo="$foo word"
# a
# b
# c=$a$b
# 
