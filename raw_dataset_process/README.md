# Raw dataset processing scripts

1. File Structure
    
    We assume the raw dataset file structure is as follows -
    ```
    person_name
        |- front
            |- sessions_id.mp4
        |- kinect
            |- sessions_id.mkv
        |- sides
            |- Corel MultiCam Capture X
                |- Records
                    |- sessions_id
                        |- Camera1.mov
                        |- Camera2.mov
        |- timestamps
            |- sessions_id.txt
    ```
    If you have a different structure then change the `config.py` file accordingly.
    
    !!!Note- We are assuming all `person_name`s are unique because it is used as the primary key.

2. Subject recording details

    The `subject_recording_details.csv` should contain the following attributes-
    * person_name
    * subject_id
    * front_perspective
    * kinect_perspective
    * left_perspective
    * right_perspective

    !!!Note- We are assuming that for a person/subject the perspective/camera view was not changed throughout all sessions.

3. Word tags

    The words are tagged with alpha-numeric values for easier data processing

    The `word_tags.csv` should contain the following attributes- 
    * word
    * tags

    !!!Note- We are assuming all `word`s are unique because it is used as the primary key.


