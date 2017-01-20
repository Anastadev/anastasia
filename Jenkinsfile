node {
    stage ("notify") {
        try{
              sshagent (credentials: ['privateserver']) {
                //sh 'ssh-add -l' 
                sh 'env'
                sh 'ssh root@vps110163.vps.ovh.ca "cd /; pwd"'
                sh 'ls -la'
                sh 'exit'
              }
        }
        catch (Exception err) {
            sh "echo coucou"
            githubNotify account: 'Anastadev', credentialsId: 'githubwithkey', description: 'This is an example', repo: 'anastasia', sha: 'd26e004c09966008a9fd7db510c04eaf4448ab1b' , status: 'FAILURE'
            sh "exit 1"
        }
    }
}
