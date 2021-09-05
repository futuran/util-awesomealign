# util-awesomealign

"util-awesomealign" is an util scripts for awesome-align. 

# Quick Start
1. Prepare parallel corpus

1. Clone original awesome-align repository in parent directory.
    - awesome-align : https://github.com/neulab/awesome-align
        ```
         git clone https://github.com/neulab/awesome-align
         cd awesome-align
         pip install -r requirements.txt
         python setup.py install
         cd ..
        ```
1. Clone this repository
    ```
     git clone https://github.com/futuran/util-awesomealign
    ```
1. Run the "awesome-align.sh". You can check options with -h command.
    ```
    mkdir flickr.tkn.align
    cd util-awesomealign
    awesome-align.sh ../flickr.tkn ../flickt.tkn.align
    ```
