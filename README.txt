CS408 Computer Science Project - 2016 Spring
PROJECT: Progressive Chalkboard Recorder (PCR)
TEAMNAME: Thevelopers
MEMBERS: Byeonggyu Bak(Leader), Minkyu Kim, Yihan Kim, Onesphore Ndayishimiye

0. Objectives & Description
 - It can be cumbersome for students to take notes while listening to the instructor(in class where chalkboards are used)
 " Many students in chalkboard-based-class experience difficulties in taking notes while listening to the instructor(Multi-tasking problem)"
 - So we made a software that captures (picture) writings on a chalkboard. 
 " So we wanted to make a program that does note-taking instead of those students"
 - It captures those notes automatically. The instructor is removed in the pictures by using "Background Extraction" technique. Pictures with a pdf that includes them are zipped and then uploaded to our central server.
 "- Our project automatically captures the chalkboard without instructor(Background Extraction), and upload the images files & pdf file to our web server."
 - Students can easily access the pictures via this website, "https://cs408.pikachu.io". They can also download the pdf file that contains those pictures on the same website. 
 "- Students can easily watch the pictures of the writings on chalkboard, via website(https://cs408.pikachu.io). Also they are available to download the pdf file consists of those pictures."

1. Requirements:
 - Webcam, or pre-taken video
 - Python 2.7.9
 - Python packages: opencv 2.4.9, reportlab 3.3.0, numpy, zipfile, requests

2. Files:
 - imagedelta.py : Main module. Processes image with opencv
 - chalkboard.py : Module that offers methods about local maximum
 - to_pdf.py : Module that offers methods about making pdf file with captured frame files(.jpg)

3. Run
 - py imagedelta.py
