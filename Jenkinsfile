pipeline {
    agent any
    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                sh 'cd ${WORKSPACE} && docker-compose build'
            }
        }
        stage('Deploy') {
            steps {
                sh 'cd ${WORKSPACE} && docker-compose up -d'
            }
        }
    }
    post {
        success {
            echo 'App deployed successfully at http://localhost:5000'
        }
        failure {
            echo 'Build or deploy failed.'
        }
    }
}
