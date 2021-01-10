#!/bin/sh

aws lambda update-function-configuration \
           --function-name lambda-homecontrol-dev \
           --environment "Variables={PASSWD=${1?Usage: $0 <passwd>}}" \
           | jq .Environment
