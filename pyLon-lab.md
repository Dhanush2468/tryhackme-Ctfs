### LAB : Pylon

## {Try Hack Me}
# Description:-
Basically this machine is a combination of reconnaissance, Steganography and Privilege Escalation.
Difficulty level: Medium

### List of tools used:
- **Steghide**
- **Stegcracker**
- **ExifTool**
- A bit of knowledge of privilege escalation.

Let’s start the Machine……..

First of all download the task file given for the 1st task.

after downloading the file, lets have some basic information about the file…

You need to keep this in mind that always start from basic information’s such as what is the file extensions, size of the file, hidden clue’s or texts on the image etc.

Now we will use the tool “exiftool” for the basic information about the file.

```
command: exiftool pepper.jpg
```
![image](https://github.com/user-attachments/assets/b64e637a-eb68-48c6-a529-01eaa654e4e3)

here we can see an URL… when we redirect to this page we can the website opens the site for CyberChef (a web app for encryption, encoding, compression and data analysis).

fine..

Now we need to use the tool Steghide to check weather any file is embedded with it or not.

Use the command:

```
Steghide extract -sf <file_name> i.e steghide extract -sf pepper.jpg
```
![image](https://github.com/user-attachments/assets/d2bdbd11-6c4e-49dd-8e4b-68d79502fe83)

ooohhhhooo…… we need to have password for this to extract..

Now what we can do to crack the password…

In this case we have to use the tool: stegcracker

To install write the command: sudo apt install stegcracker

![image](https://github.com/user-attachments/assets/2e48bd3f-0a23-49d6-b185-dae5b19ca486)

hence we can see that all the contents are stored in the file “pepper.jpg.out”. And the ```password``` for this is :- ```pepper```

Well now we can extract the image file using this passoword. So for extracting the file type the

command:-
```
steghide extract -sf pepper.jpg
```
![image](https://github.com/user-attachments/assets/e6fe12ab-8544-4192-9a24-c382ba2739fb)
![image](https://github.com/user-attachments/assets/38891692-02df-4f56-aa5e-f73b30760cd3)
nahh man…… I think there is something inside this too. Let’s have a look on it. Actually the main thing is that we don’t know about this file. Try to check what is the file type.

command: 
```file <file_name> i.e file lone```
The file contains ASCII code.

now we need to decode it and copy the content to another file.

command:
```base64 -d lone > lone1 {here -d denotes decoding}```
We can see that the file is “gzip compressed data, from Unix, original size modulo 2³² 10240”

Hence we need to extract this too and with this we come up with the conclusion that it is a tar file.

To extract this — — — ->

command: 
```
tar -xvf lone1
```
well its good to know that we found something interesting here.

![image](https://github.com/user-attachments/assets/88c32ece-8baa-423b-9c83-efe4f50b3d2d)

I think that’s enough for us. Now we need to move on to task 2, for this start the machine and scan the ports available using nmap.

command
```
nmap -v -n -sC -sV -p-2500 <IP>
```
On scanning we found a port 222 for ssh. As we know for ssh login we need to have a password for it.

Now for ssh login command: ssh lone@10.10.38.210 -i lone_id -p 222

![image](https://github.com/user-attachments/assets/852dbf4a-79b4-46d4-a53d-7e21ec30d21a)

We need to provide the permission for it ```(600: only the owner of the file has full read and write access to it)```

command: ```chmod 600 line_id```
After that type the same command for the ssh
![image](https://github.com/user-attachments/assets/0980e5c1-0837-4b07-8b88-5704b91ce160)
At this stage I came to know that i was having a password for lone: pepper

But we can use this directly so we need to change it to hex to base85 as we know the link was provided to us in the image.

So after converting we have the password as pepper — ->2_[-I2_[0E2DmEK

Now try to login and try to get the answers for this. Select the options according to the options we need to answer.

### Note: Guys while solving any machine try to save each and every thing we have gathered so that we can use it according to our requirement. Save this into a text file.

We can see the user name and the password for username: lone this is for ssh login.

and the another option is for the First flag.

![image](https://github.com/user-attachments/assets/7947a008-2251-49d9-8bde-c8d9ed9b5b24)

What is Flag 1?
```THM{homebrew_password_manager}``` Correct Answer

Fine let’s try to login with ssh with the password.
![image](https://github.com/user-attachments/assets/976a22fa-c0bd-4c5c-8bf1-352e74e2115e)

fine we have our ```Second answer```

Let’s move on and try to get the next flag…..

![image](https://github.com/user-attachments/assets/eb2be843-1cb5-441a-916a-2f0cfe506cf4)

here we can see a file git, as we know git is also a command too for linux.

![image](https://github.com/user-attachments/assets/01c50838-dc1f-4d77-a6f1-5d9051f34f1a)

well know we need to find this file name as: ```pyLon_pwMan.py```

Let’s have an eye on the logs inside for this
command: ```git log```
we can see the logs so we need to check out all the ID’s.

command: ```git checkout <ID>```

We can see 3 commit Id’s so checkout all the 3.

![image](https://github.com/user-attachments/assets/83c35232-61c4-4cca-bfab-8116713ff076)
now list all the file we can see the file which we were trying to find.

Run this python file using the command: ```python3 pyLon_pwMan.py```

Use the same key here too.

and try to gather the info which we need.

![image](https://github.com/user-attachments/assets/eff6e4eb-765e-42d8-94cd-ed1795f657ec)

As we can see that we saw a file in gpg form ie note from pood i guess…..

and for this we have our password too sot try to extract it

command: ```gpg note_from_pood.gpg```
and after that type the password.

![image](https://github.com/user-attachments/assets/ab508abd-ec6a-48bf-8073-3af64a306ef3)

As of now we have gathered many information’s so with this we have a clear understanding of a ```new user pood```.Well it’s good for us to have these type of information.

Here we can note that there is a password too for the user pood. i.e 
### Password: ```yn0ouE9JLR3h)`=I```

Hence we can see that we have a new user and his password as well, now try to switch the user with
### command: ```su pood```
and type the password… , After this list all the files and directories we have our next flag.
![image](https://github.com/user-attachments/assets/2338f641-af14-47d1-a690-8ebc80a37007)

What is User2 flag?

```THM{homebrew_encryption_lol}```  Correct Answer

Good… Well Done guys.. finally we now need to have the last flag, but we have the most important part of for penetration testing i.e Privilege escalation.
For the flag root.txt we have to be the root user.

command: ```sudo -l and type the password for the pood```

we can see a message…..
![image](https://github.com/user-attachments/assets/d18ef288-487f-461f-a9f8-8bac24251696)

location : ```/opt/openvpn/client.ovpn```
At this part i got stuck for a while as i was not having much idea about vpn configuration so i just typed the same command and i found that i can edit the or we can say that i cam make changes and write codes inside it. So after getting some information’s from the available sources… I came to the conclusion that i can have a reverse shell which i can insert into it for the further process.

## some of the commands i found was
- **script**
- **up ,etc.**
and for more information’s about openvpn you can use the
command: ```man openvpn```
now we need to have a reverse shell and we will store this file in ```/tmp``` file so that it should be for a short period of time.
so go to ```/tmp directory (cd /tmp)```

Now inside this create a bash file with vi type teh reverse shell command.

![image](https://github.com/user-attachments/assets/6216a743-bf24-4ece-8335-bbb3735680a2)

As we can see we have given the permission of 4777(Gives read, write, execute permissions to everybody).

and to exit this type — — escape key , : wq! and hit enter

now we need to put this shell in the openvpn.

so type the command we have found to edit the openvpn.

Hence we need to put this shell so type command as same as it is shown in the image.
![image](https://github.com/user-attachments/assets/13aaaeec-324f-41a1-ad4f-f32baf1998e2)
command: ```sudo openvpn <location> i.e sudo openvpn /opt/opennvpn/client.ovpn```
But we can see a message here that it is not accessed by pood
![image](https://github.com/user-attachments/assets/b1956613-3612-4c7d-bcf4-178bd3ed9771)
So we need to switch the user to lone

now type the command.

Than type the
command : ``./bash -p``
and type ``` whoami```, now you are a root user so list the files and mv to root directory.
![image](https://github.com/user-attachments/assets/b01b8045-6f0c-4575-b93b-5714b8606ee0)
But we can’t open this gpg file as we know that to extract this we need to have password for it.

now we are going to have a small trick, we need to see that am i able to make changes in password file.

so we will change the password of the root i.e the hash form, which is store in ```/etc/shadow```

So we will write the same password of ``pood`` to the root.
![image](https://github.com/user-attachments/assets/55e0e9fb-6a7b-4bf7-8ccc-c4cc33355c81)

### Note: copy the full code of pood including the (.) too.
With this we have made the password of root same as the pood. It directly indicates that pood is also a root user so with pood’s password try to extract the gpg file inside the root.
command: ```gpg -d root.txt.gpg```
and type the password of pood i.e Password: ```yn0ouE9JLR3h)`=I```
![image](https://github.com/user-attachments/assets/36012501-2aca-431d-a443-673f2b0f2228)

What is root's flag?

```ThM{OpenVPN_script_pwn}``` Correct Answer



### Hence we can see the last flag too.
![cats-in](https://github.com/user-attachments/assets/e91c786f-80b4-4bdf-8829-c3834e084186)
![cat-dance-dancing-cat](https://github.com/user-attachments/assets/347157af-e081-452e-8524-43aecc5d0266)





