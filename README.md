# animevost.org
```
# *Firefox driver runs if you have Firefox browser (i think)*
# driver/* -> drivers in base 64x
#
# shscript is dead!!! (just nah tried after updating)
# pyscript still alive bcz of selenium.webdriver
# 
# url was changed:
#     from: http://file.aniland.org/720/2147397125.mp4
#     to:   http://file.aniland.org/720/2147397125.mp4?md5=_VaMjhmg3xUOeaB2ydrB4g&time=1542204358
#
# ./animevost.sh [url]        |   download series with bash script
#                             |   animevost.sh -> deadscr.sh

python3 animevost.py [url]    |   download series with python3 script

Exampli gratia:
    $ python3 animevost.py http://animevost.org/tip/tv/239-danshi-koukousei-no-nichijou.html
    NAME: Повседневная жизнь старшеклассников
    100% [......................................................................] ??? / ???

    with verbose [-v]:
        $ python3 animevost.py http://animevost.org/tip/ova/85-yondemasu-yo-azazel-san-ova1.html -v
        [08:14:54] --INFO-- FUNC @first_run           :Move geckodriver* to executable path if exists
        [08:14:54] --INFO-- FUNC @get_folder_name     :Creating new directory and changing dir to it
        NAME: Явись, Азазель ОВА
        [08:15:06] --INFO-- FUNC @run_driver          :FORpage /tip/ova/85-yondemasu-yo-azazel-san-ova1.html
        [08:15:19] --INFO-- FUNC @get_page_source     :Entry pointer, make series_id readable
        [08:15:19] --INFO-- FUNC @get_series_url      :Parsing webpage for getting HD and SD
        [08:15:25] --INFO-- FUNC @get_multiprocessing :First run for downloading HD, second for SD format
        [08:15:26] --INFO-- FUNC @get_multiprocessing :First run for downloading HD, second for SD format
        100% [......................................................................] 114488467 / 114488467
        [08:16:13] --INFO-- FUNC @remove_log          :Removing logfile that creating geckodriver
        [08:16:13] --INFO-- FUNC @get_data            :Parsing webpage for getting data of series_id
```
