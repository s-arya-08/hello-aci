pipeline {
    agent any

    environment {
        ACR_NAME = 'sanskartestacr'                      // e.g. mytestacr
        ACR_LOGIN_SERVER = "sanskartestacr.azurecr.io"   // e.g. mytestacr.azurecr.io
        IMAGE_NAME = 'sample-aci-app'
        IMAGE_TAG = 'v1'
        RESOURCE_GROUP = 'test-rg'        // e.g. test-rg
        ACI_NAME = 'sample-aci'
        LOCATION = 'eastus'                           // pick your region
    }

    stages {
        stage('Build Docker Image') {
            steps {
                sh """
                    echo "Building Docker image..."
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('Push to ACR') {
            steps {
                sh """
                    echo "Login to ACR and push..."
                    az login --use-device-code
                    az acr login --name ${ACR_NAME}
                    docker push ${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('Deploy to ACI') {
            steps {
                sh """
                    echo "Fetching ACR credentials..."
                    USERNAME=\$(az acr credential show --name ${ACR_NAME} --query "username" -o tsv)
                    PASSWORD=\$(az acr credential show --name ${ACR_NAME} --query "passwords[0].value" -o tsv)

                    echo "Deploying container to Azure..."
                    az container create \
                      --resource-group ${RESOURCE_GROUP} \
                      --name ${ACI_NAME} \
                      --image ${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${IMAGE_TAG} \
                      --registry-login-server ${ACR_LOGIN_SERVER} \
                      --registry-username \$USERNAME \
                      --registry-password \$PASSWORD \
                      --dns-name-label ${ACI_NAME}-demo \
                      --ports 80 \
                      --location ${LOCATION} \
                      --restart-policy Always
                """
            }
        }
    }

    post {
        success {
            echo "✅ Deployed successfully. Check your container URL."
        }
        failure {
            echo "❌ Pipeline failed. See logs."
        }
    }
}
