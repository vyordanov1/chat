pipeline {
    agent any

    stages {
        stage('Transfer to Prod') {
            steps {
                script {
                    sh 'ssh root@chat.vasil.com \'cd /root/chat; docker compose down; git pull; docker compose up -d\''
                }
            }
        }
        stage('Check CTs Are UP') {
            steps {
                script {
                    def ctStatus = sh(script: 'ssh root@chat.vasil.com \'docker ps | grep Up | wc -l\'', returnStdout: true).trim()
                    echo "Docker Containers Status: ${ctStatus}"
                    if (ctStatus != "3") {
                        currentBuild.result = 'FAILURE'
                        error("Not all Docker CTs are Up! Check the detailed view !!!")
                        sh 'ssh root@chat.vasil.com \'cd /root/chat/; docker ps\''
                    }
                }
            }
        }
    }
}
