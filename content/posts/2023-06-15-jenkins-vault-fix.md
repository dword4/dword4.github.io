Title: AWS Account Switching with Vault in Jenkins
Date: 2023-06-15
Category: programming
Slug: aws-switch-vault-jenkins
Authors: dword4
Summary: A workaround for AWS Account Switching with Vault in Jenkins

## Problem

I ran into an issue recently where some of my automation that cycles through AWS accounts and runs code
against each accounts resources broke. It would become sticky to the account that we intially connected
to Vault and never switch when using `vault read aws/something/else. We worked on trying to use curl calls
and other various workarounds but nothing seemed to work.

## Eventual Solution

After a few days of working on things off and on I decided to just hammer out a custom function in Groovy
that would handle the account switching for us. Fastforward like 100+ commits and Jenkins runs later and I 
finally got something that worked for switching.

```
def vaultAWS(account_level, account_team) {
    def vaultQuery = "aws/$account_level/$account_team/sts/admin"
    print "testing: $vaultQuery"
    try {
        def vaultOutput = sh(returnStdout: true, script: "vault read $vaultQuery").trim()
        def keyValuePairs = [:]
        vaultOutput.split('\n').each { line ->
            def (key, value) = line.split(' ', 2).collect { it.trim() }
            if ( key == 'access_key' || key == 'secret_key' || key == 'security_token'){
                keyValuePairs[key] = value
            }
        }
        // set env variables
        env.AWS_ACCESS_KEY_ID = keyValuePairs['access_key']
        env.AWS_SECRET_ACCESS_KEY = keyValuePairs['secret_key']
        env.AWS_SESSION_TOKEN = keyValuePairs['security_token']
    } catch (Exception e) {
        println "Something went wrong"
    }
    
}
```

This let me loop through our lists of accounts and run a basic test to make sure I could actually
see the resources in the AWS account. Unfortunately I found additional problems (like an entire set
of accounts were simply *poof* gone) but the code worked exactly as I had hoped. Further research lead
me to the use of @Grab to pull from git repos for code so ideally this can be pulled remotely instead
of manually pasted into every single Jenkins job we end up using it in. Of course by the time I get all
that worked out we are going to start the joyful process of moving out automated jobs from Jenkins to 
Gitlab CI/CD
