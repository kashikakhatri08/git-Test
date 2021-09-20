pipeline{
    agent any
    stages{
        stage("testing1"){
            steps{
                script{
                    
                    checkout(scm)
                    //println("msggggggg")
                    //env.GIT_COMMIT_MSG = bat (script: 'git log -1', returnStdout: true).trim()
                    //println(env.GIT_COMMIT_MSG)
                    echo "[detached HEAD 550db15] Ignoring the test scripts for A11 AVDXP-7225 Ignoring the test scripts Jira-Id: AVDXP-7227 Domain: OS/BSP Change-Type: Feature Target-Hardware: SDM Target-Variant: Z2"
                    echo "domain."
                    echo "domain."
                    echo "[detached HEAD 550db15] Ignoring the test scripts for A11 AVDXP-7225 Ignoring the test scripts Jira-Id: AVDXP-7227 Domain: HMI Change-Type: Bug Target-Hardware: SDM Target-Variant: Z2"
                    echo "testJob --- /testing_folder/testing_job"
                    build job: 'testing_folder/testing_two/python_script_test_two'
                    env.bld = "${currentBuild.buildVariables}"
                    // echo "${currentBuild.rawBuild.parent.url}"
                    echo "${currentBuild.rawBuild}"
                    echo"${currentBuild.result}"
                    echo "stages --- [prepare:[state:enabled, scripts:[getChangeList, getStackTarget]], build:[state:enabled, scripts:[aospSyncWS, aospBuild]], test:[state:enabled, testStage:T1, testJobWait:true, testJobPropagate:false, scripts:[aospTest]], publish:[state:disabled, scripts:[]], notification:[state:enabled, emailAddress:F_AVDXP_Gerrit_Integration@elektrobit.com, scripts:[aospNotification]], cleanup:[state:enabled, scripts:[aospCleanUpWs]]]"
                    //echo "STAGE_NAME='TX'"
                }
            }
        
        }
        stage("AOSP build"){
            steps{
                script{
                    
                    //checkout(scm)
                    //println("msggggggg")
                    //env.GIT_COMMIT_MSG = bat (script: 'git log -1', returnStdout: true).trim()
                    //println(env.GIT_COMMIT_MSG)
                //   sleep(5)
                   echo "hello"
                   echo 'NODE_NAME=deulm2hu030'
                   echo 'androidVersion --- android9'
                   echo '[2021-09-20T02:28:33.810Z] CHANGELIST_local:\n[2021-09-20T02:28:33.810Z] [AVDXP/vendor/ford/modules/avdxp_common:10096,1]'
                                     
                }
            }
        
        }
    }
    post {
        success {
            script {
                echo "success"
                //  env.BUILD_STATUS = "${currentBuild.currentResult}"
                //  env.Change_sets = "${currentBuild.changeSets}"
                //  echo "${currentBuild.changeSets}"
                //  //env.GIT_COMMIT = bat (script: "git rev-parse HEAD", returnStdout: true).trim()
                //  echo "${env.GIT_COMMIT}"
                 //env.GIT_COMMIT_MSG = bat (script: 'git log -1 --pretty=full ${env.GIT_COMMIT}', returnStdout: true).trim()
                 //echo "${env.GIT_COMMIT_MSG}"
                 //echo "${_scm.GIT_COMMIT}"
                 bat label: '', script: ''' python testing.py --username="kashika" --password="kashika08"'''
                 archiveArtifacts artifacts: '*.json'
            }
        }
        failure {
            script {
                echo "failures"
                bat label: '', script: '''python testing.py --username="kashika" --password="kashika08"'''
                archiveArtifacts artifacts: '*.json'
                
            }
        }
    }
}
