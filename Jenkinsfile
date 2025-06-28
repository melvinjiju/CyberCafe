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
                    sh 'pwd'  // Show current directory
                    sh 'ls -la'  // List all files to confirm docker-compose.yml is present
                    sh 'docker-compose --version || echo "Docker Compose not found"'  // Check if Docker Compose is available
                    sh 'docker-compose -f ${WORKSPACE}/docker-compose.yml build'  // Use absolute path
                }
            }
        }
        stage('Deploy') {
            steps {
                dir("${WORKSPACE}") {
                    sh 'docker-compose -f ${WORKSPACE}/docker-compose.yml up -d'
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
