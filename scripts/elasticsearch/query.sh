#!/bin/bash
curl localhost:29200/$1/_search | jq
