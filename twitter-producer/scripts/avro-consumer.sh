#!/bin/bash
confluent local consume $1 -- --value-format avro --from-beginning --property print.key=true


