#!/bin/sh
cd /HOME/nscc-gz_jiangli/virtualenv/config/redis

../../3.2.4/bin/redis-cli -p 26379 shutdown

sleep 5
#last_conf=`ls -t cn*.sentinel.conf | head -n 1`
#cp $last_conf $HOSTNAME.sentinel.conf
#cp sentinel.conf.part $HOSTNAME.sentinel.conf
#grep "^sentinel monitor " $last_conf >> $HOSTNAME.sentinel.conf
#cat "sentinel config-epoch mymaster 1" >> $HOSTNAME.sentinel.conf

cp sentinel.conf $HOSTNAME.sentinel.conf
../../3.2.4/bin/redis-sentinel $HOSTNAME.sentinel.conf

#../../3.2.4/bin/redis-sentinel $HOSTNAME.sentinel.conf &> log.$HOSTNAME.sentinel 




