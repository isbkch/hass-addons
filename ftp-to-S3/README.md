# Home Assistant Add-on: FTP To S3

Automatically move files to S3 from your local /backup folder

## About

I Built this add-on because I needed a way to store my surveillance camera recordings on Amazon S3.
Many cameras allow uploading of files via FTP, so only the last step of moving them to S3 was left.

This add-on will automatically and recursively upload anything you put inside the folder "/backup" to the Amazon S3 bucket of your choice and will optionally upload existing files if they are not found in S3.

My setup currently is using the official FTP add-on to enable an FTP server on the Pi running Hass, thus accepting my FTP cameras uploads and then this add-ons take care of the rest.

Although I have a decade of experience in software engineering, I'm not a Python developer, so this awesome add-on was a big inspiration https://github.com/gdrapp/hass-addons

Every contribution is welcome.