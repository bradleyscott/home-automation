log=removeOldSecurityRecordings.log
path=/media/bradley/external/security

echo $(date) "Removing files from " $path " greater than 14 days old..." >> $log
find $path -mtime +14 -type f -delete >> $log
echo $(date) "Completed removal of old files" >> $log
