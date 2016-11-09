#!/bin/bash

if [ $TRAVIS_BRANCH = "master" ]
then
        curl http://mth.epac.to:5000/deploy_master/
fi
if [ $TRAVIS_BRANCH = "dev" ]
then
        curl http://mth.epac.to:5000/deploy_dev/
fi