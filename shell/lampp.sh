#!/bin/bash
#
# Author : Electron (Suraj Nath) | htttps://www.github.com/electron0zero
# what the hell is this : this script install LAMP stack with php and configures a folder vhost in home dir.
# and after that you can put you files in ' ~/vhost ' insted of ' /var/www/html '.
# usage : sudo /bin/bash lampp.sh
# in my case lampp.sh is file name replace it with your file name
# i am expacteing that you have basic knowlege of installation in linux
#
echo
echo "########## LAMP Stack with phpmyadmin Installation ##############";
echo
if [ "`lsb_release -is`" == "Ubuntu" ]
then
	cd ~
	echo
	echo "########### updateing system #################";
	echo
	sudo apt-get update
	echo
	echo "########### fixing misssing packages #################";
	echo
	sudo apt-get update --fix-missing
	echo
	echo "########### removeing extara packages #########";
	sudo apt-get autoremove
	echo
	echo "#### if your system updated without any error then type 'y' otherwise resolve the update issue and then run this ####";
	echo
	read -p "response : " -n 1 -r
	echo    # (optional) move to a new line
	if [[ $REPLY =~ ^[Yy]$ ]]
	then
    	echo "OK, let's do this";
	fi
	echo
	echo "########### installing apache2 ##############";
	sudo apt-get install apache2
	echo
	echo "########### installing mysql server ##########";
	sudo apt-get install mysql-server
	echo
	echo "#### is your mysql-server installed without any problems if yes the say 'y' ####";
	echo
	read -p "response : " -n 1 -r
	echo    # (optional) move to a new line
	if [[ $REPLY =~ ^[Yy]$ ]]
	then
    	echo "OK, moveing on ";
	fi
	echo
	echo "########### installing php5 and apachelib for php5 ##########";
	echo
	sudo apt-get install php5 libapache2-mod-php5
	echo
	echo "########### restarting mysql server ##########";
	echo
	sudo /etc/init.d/apache2 restart
	echo
	echo "#### go to browser and type ' localhost ' if you see a default page or it works type then type 'y' if you don't see that response then do a internet search ####";
	echo
	read -p "response : " -n 1 -r
	echo    # (optional) move to a new line
	if [[ $REPLY =~ ^[Yy]$ ]]
	then
    	echo " Here we go ";
	fi
	echo
	echo "########### verifying php install ##########";
	echo
	php -r 'echo "\n\nYour PHP installation is working fine.\n\n\n";'

	echo "#### type 'y' if these things are OK,
	1.your mysql-server server is insatalled and you know it's root password
	2.your webserver is running normally ####";
	read -p "response : " -n 1 -r
	echo    # (optional) move to a new line
	if [[ $REPLY =~ ^[Yy]$ ]]
	then
    	echo " Almost done ";
	fi
	echo
	echo "########### installing phpmyadmin ##########";
	sudo apt-get install phpmyadmin
	echo
	echo "############# setting symlink for phpmyadmin ##############";
	sudo ln -s /usr/share/phpmyadmin /var/www/html/
	echo
	echo "####### restarting webserver #############";
	sudo service apache2 reload
	echo
	echo "###### setting up vhost directory in home folder ##########";
	echo
	cd ~
	mkdir vhost
	sudo ln -s ~/vhost /var/www/html/
	cd ~/vhost/
	echo
	echo " ######### putting a test index.html file in vhost so we can test that vhost is properly configured ###########";
	echo
	echo "
<!DOCTYPE html>
<html>
<head>
<title>vhost</title>
</head>
<body>

<h1>virtual host is working</h1>
<p>this is vhost in my webserver if you seeing this page means your server is running and you can put your projects in vhost folder by default located in ~/vhost/ </p>

</body>
</html>" >> index.html
	echo
	echo "#### go to ' localhost/vhost ' in your browser and if you se vhost is working then we are good to go###### ";
	echo
	echo "######## KbyeTnx ##############";
fi
