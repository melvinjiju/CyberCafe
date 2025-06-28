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
                dir("${WORKSPACE}") {
                    sh 'ls -la'
                    sh 'docker-compose --version'
                    sh 'docker-compose -f docker-compose.yml build'
                }
            }
        }
        stage('Deploy') {
            steps {
                dir("${WORKSPACE}") {
                    sh 'docker-compose up -d'
                }
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
