# Hidden notes (100 pts)

Hacker has left the picture, maybe you can find information about his plans from the picture?
![hacker_picture](files/checklist.jpg)
File: [checklist.jpg](files/checklist.jpg)

First idea what to do with pictures is to look if there is some text hidden in the image.  
So I used command:
```
strings checklist.jpg | less
vExif
PASSWORD is hacker
#*%%*525EE\
#*%%*525EE\
$3br
```

This shows that there is password hidden inside image, usually if you find some phrase, it is a good chance that there is something else embedded inside the picture with program called steghide.  
Steghide uses password to hide things into images.  
Lets try to see if there is something indeed hidden.
```
steghide extract -sf checklist.jpg -p hacker
# -sf is for source_file and -p is for password
# we can see that it successfully got some file out from it.
wrote extracted data to "hiddentext.txt".
cat hiddentext.txt
# contents of the hiddentext.txt file:
Hospital checklist:
Hack the doors
Plant ransomware
Hack the pumps
The Flag is: 65b74946-b604-4783-b282-0d20443fd946
```

And there we have it!