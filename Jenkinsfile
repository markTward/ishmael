pipeline {
  agent {
    node {
      label 'k8s'
    }
    
  }
  stages {
    stage('preparation') {
      steps {
        echo 'println "hello moby\''
      }
    }
  }
}