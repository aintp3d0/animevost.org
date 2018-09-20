#!/bin/bash


_720='_720.txt'
_420='_420.txt'
_base_url='http://file.aniland.org'
_give_me_seri=()


function _rename_ids() {
    #
    # RENAME ID.MP4 TO NAME.MP4
    #
    idnx=1
    for item in ${_give_me_seri[@]}
    do
        echo "$item.mp4"
        rename "$item.mp4" "$idnx серия.mp4"
        idnx=$[ $idnx + 1 ]
    done
}


function _download_missing() {
    #
    # DOWNLOAD NOT EXIST 720P SERIES FROM 420P
    #
    echo "Missing series"
    exit 1
}


function _check_exists() {
    #
    # MP4 FILES IN CURRENT DIR
    #
    series=($(find -maxdepth 1 -type f -name '*.mp4'))

    if [ ${#series[@]} -eq 0 ]; then
        _download_urls $_420
    elif [ ${#series[@]} -eq ${#_give_me_seri} ]; then
        _rename_ids
    else
        _download_missing
    fi
}


function _download_urls() {
    #
    # DOWNLOAD PARALLEL 4 SERIES (-j 4)
    # SRC: https://www.youtube.com/watch?v=sHpTywpb4_4
    #
    cat $1|parallel -j 4 wget {}

    _check_exists
}


function _generate_series_url() {
    #
    # DOWNLOAD SERIES LIKE PARALLEL
    #
    sl=0 
    for seri in "${_give_me_seri[@]}"
    do
        echo "$_base_url/720/$seri.mp4" >> "$_720"
        echo "$_base_url/$seri.mp4" >> "$_420"
    done

    _download_urls $_720
}


function _make_folder() {
    #
    # MAKE DIRECTORY LIKE ANIME NAME
    #
    read -p "NAME: " aname
    aname=$(echo $aname|tr '"' '_'|tr ' ' '_')
    echo "WE GAVE HIM: $aname"

    if [ ! -d $aname ]; then
        mkdir $aname && cd $aname;
    else
        cd $aname
    fi;

    _fn=$aname

    _generate_series_url
}


function _split_data() {
    #
    # SPLIT DATA TO NAME AND ID
    # data: 1\n seri\n ID\n ...
    #
    data=($(cat series.txt|grep '\w'|tr ':' ' '|tr ',' ' '|tr 'var data = {' ' '|tr '};' ' '|tr '"' ' '))
    indx=0
    for item in "${data[@]}"
    do
        if [ $indx -eq 0 ]; then
            indx=$[ $indx + 1 ]
        elif [ $indx -eq 1 ]; then
            indx=$[ $indx + 1 ]
        else
            _give_me_seri+=("$item")
            indx=0
        fi
    done

    _make_folder
}


function _get_data() {
    #
    # NEW FUNCTION BCZ IN VAR *_give_me_????* TRYING TO PRINT $1
    #
    curl $1 | grep -i "var data = {" > series.txt

    _split_data
}


_get_data $1
