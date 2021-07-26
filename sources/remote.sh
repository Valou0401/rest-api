#!/bin/bash

PS3='Please enter your choice: '
options=("Create Gitlab project" "Delete Gitlab project" "Create Jenkins project" "Delete Jenkins project" "Build Jenkins job" "Quit")
select opt in "${options[@]}"

do
    case $opt in
        "Create Gitlab project")
            echo "Create Gitlab project"
            echo "Gitlab project name : "
            read projectName
            python3 remote.py -g $projectName master
            echo "Project create! Go to http://172.19.0.4/"
            break
            ;;
        "Delete Gitlab project")
            echo "yDelete Gitlab project"
            echo "Gitlab project name : "
            read projectName
            python3 remote.py --delete-gitlab $projectName master
            echo "Project deleted!"
            break
            ;;
        "Create Jenkins project")
            echo "Create Jenkins project"
            echo "Gitlab project name to construct on Jenkins: "
            read projectName
            python3 remote.py -j $projectName master
            break
            ;;
        "Delete Jenkins project")
            echo "Delete Jenkins project"
            echo "Jenkins project name : "
            read projectName
            python3 remote.py --delete-jenkins $projectName master
            break
            ;;
        "Build Jenkins job")
            echo "Build Jenkins job"
            echo "Jenkins project name : "
            read projectName
            echo "Jenkins branch name : "
            read branchName
            python3 remote.py -b $projectName $branchName
            break
            ;;
        "Quit")
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
done
