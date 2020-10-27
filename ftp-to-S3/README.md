# Home Assistant Add-on: FTP To S3

Automatically move files to S3 from your FTP destination folder

## About

Built this addon because I needed a way to store my surveillance camera recordings. Many cameras allows uploading of files via FTP, so only the last step was left, which is moving them to S3.
This addon will automatically recursively upload anything you put inside the folder "/backup" to the Amazon S3 bucket of your choice and will optionally upload existing recordings if they are not found in S3.

My setup currently is using the official FTP addon to upload from the cameras then this addons take care of the rest.
