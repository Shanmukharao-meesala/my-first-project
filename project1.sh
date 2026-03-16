#!/bin/bash
date_now=$(date)
current_folder=$(pwd)


echo "CURRENT DATE: $date_now"
echo "CURRENT FOLDER: $current_folder"
echo "SYSTEM IS RUNNING"

mkdir -p logs

echo "current date: $date_now" > logs/system.log
echo "current folder: $current_folder" >> logs/system.log
echo "system is running" >> logs/system.log


