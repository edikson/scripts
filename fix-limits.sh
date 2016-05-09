#!/bin/bash

grep -E "^\*\s+soft\s+nofile" /etc/security/limits.conf > /dev/null || \
  sudo sh -c 'echo "* soft nofile 50000" >> /etc/security/limits.conf'
grep -E "^\*\s+hard\s+nofile" /etc/security/limits.conf > /dev/null || \
  sudo sh -c 'echo "* hard nofile 50000" >> /etc/security/limits.conf'

