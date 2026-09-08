pipeline {
    agent any

    environment {
        PROJECT_NAME = "devops-monitoring-platform"

        BACKEND_IMAGE  = "localhost/devops-monitoring-backend"
        FRONTEND_IMAGE = "localhost/devops-monitoring-frontend"
        AGENT_IMAGE    = "localhost/devops-monitoring-agent"

        IMAGE_TAG = "${BUILD_NUMBER}"

        K8S_NAMESPACE = "monitoring"

        PYTHONUNBUFFERED = "1"
    }

    options {
        timestamps()

        disableConcurrentBuilds()

        buildDiscarder(
            logRotator(
                numToKeepStr: "10"
            )
        )

        skipDefaultCheckout(true)
    }

    stages {

        stage("Checkout") {
            steps {
                echo "Checking out source code..."

                checkout scm

                sh '''
                    set -eu

                    echo "=============================================="
                    echo "Git Information"
                    echo "=============================================="

                    echo "Commit:"
                    git rev-parse --short HEAD

                    echo "Branch:"
                    git branch --show-current

                    echo "Status:"
                    git status --short || true
                '''
            }
        }

        stage("Project Validation") {
            steps {
                echo "Validating project structure..."

                sh '''
                    set -eu

                    echo "Checking required files..."

                    test -f Jenkinsfile

                    test -f backend/requirements.txt
                    test -f backend/requirements-dev.txt
                    test -f backend/Containerfile
                    test -f backend/pytest.ini

                    test -f backend/tests/conftest.py

                    test -f frontend/package.json
                    test -f frontend/Containerfile
                    test -f frontend/nginx.conf

                    test -f agent/requirements.txt
                    test -f agent/Containerfile

                    test -f podman-compose.yml

                    test -f deployment/kubernetes/namespace.yaml
                    test -f deployment/kubernetes/configmap.yaml
                    test -f deployment/kubernetes/postgres.yaml
                    test -f deployment/kubernetes/backend.yaml
                    test -f deployment/kubernetes/frontend.yaml
                    test -f deployment/kubernetes/agent.yaml
                    test -f deployment/kubernetes/services.yaml
                    test -f deployment/kubernetes/ingress.yaml

                    echo "Project structure validation passed."
                '''
            }
        }

        stage("Environment Verification") {
            steps {
                echo "Verifying Jenkins build environment..."

                sh '''
                    set -eu

                    echo "=============================================="
                    echo "Jenkins"
                    echo "=============================================="

                    echo "User:"
                    whoami

                    echo "Workspace:"
                    echo "$WORKSPACE"

                    echo "=============================================="
                    echo "Python"
                    echo "=============================================="

                    python3 --version
                    command -v python3

                    echo "=============================================="
                    echo "Node.js"
                    echo "=============================================="

                    node --version
                    command -v node

                    NODE_MAJOR=$(node -p "process.versions.node.split('.')[0]")

                    if [ "$NODE_MAJOR" -lt 20 ]; then
                        echo "ERROR: Node.js 20 or newer is required."
                        echo "Current Node.js: $(node --version)"
                        exit 1
                    fi

                    echo "Node.js requirement passed."

                    echo "=============================================="
                    echo "NPM"
                    echo "=============================================="

                    npm --version
                    command -v npm

                    echo "=============================================="
                    echo "Podman"
                    echo "=============================================="

                    podman --version
                    command -v podman

                    echo "=============================================="
                    echo "kubectl"
                    echo "=============================================="

                    kubectl version --client
                    command -v kubectl

                    echo "=============================================="
                    echo "k3s"
                    echo "=============================================="

                    k3s --version
                    command -v k3s

                    echo "=============================================="
                    echo "Kubernetes Node"
                    echo "=============================================="

                    kubectl get nodes

                    echo "=============================================="
                    echo "Monitoring Namespace"
                    echo "=============================================="

                    kubectl get namespace "${K8S_NAMESPACE}" >/dev/null

                    echo "Environment verification passed."
                '''
            }
        }

        stage("CI Database Preparation") {
            steps {
                echo "Preparing isolated SQLite database for CI..."

                sh '''
                    set -eu

                    CI_DB_FILE="$WORKSPACE/.devops-monitoring-ci.db"

                    rm -f "$CI_DB_FILE"

                    touch "$CI_DB_FILE"

                    chmod 600 "$CI_DB_FILE"

                    echo "CI database:"
                    ls -l "$CI_DB_FILE"

                    echo "CI database preparation passed."
                '''
            }
        }

        stage("Backend Tests") {
            steps {
                echo "Running backend tests..."

                sh '''
                    set -eu

                    echo "Creating CI Python virtual environment..."

                    rm -rf "$WORKSPACE/.venv-ci"

                    python3 -m venv "$WORKSPACE/.venv-ci"

                    . "$WORKSPACE/.venv-ci/bin/activate"

                    echo "Python:"
                    python --version

                    echo "Upgrading pip..."

                    python -m pip install --upgrade pip

                    echo "Installing backend test dependencies..."

                    pip install \
                        -r "$WORKSPACE/backend/requirements-dev.txt"

                    export PYTHONPATH="$WORKSPACE/backend"

                    export DATABASE_URL="sqlite:////$WORKSPACE/.devops-monitoring-ci.db"

                    cd "$WORKSPACE/backend"

                    echo "=============================================="
                    echo "Backend Import Test"
                    echo "=============================================="

                    python -c \
                        "from app.main import app; print('Backend import OK')"

                    echo "=============================================="
                    echo "Pytest"
                    echo "=============================================="

                    python -m pytest -v

                    echo "Backend tests passed."
                '''
            }
        }

        stage("Frontend Tests and Build") {
            steps {
                echo "Running frontend tests and build..."

                sh '''
                    set -eu

                    cd "$WORKSPACE/frontend"

                    echo "=============================================="
                    echo "Node.js"
                    echo "=============================================="

                    node --version

                    echo "=============================================="
                    echo "NPM"
                    echo "=============================================="

                    npm --version

                    echo "=============================================="
                    echo "Frontend Dependencies"
                    echo "=============================================="

                    npm install

                    echo "=============================================="
                    echo "Frontend Tests"
                    echo "=============================================="

                    FRONTEND_TEST_FILES=$(
                        find . \
                            -type f \
                            \\( \
                                -name "*.test.js" \
                                -o -name "*.test.jsx" \
                                -o -name "*.test.ts" \
                                -o -name "*.test.tsx" \
                                -o -name "*.spec.js" \
                                -o -name "*.spec.jsx" \
                                -o -name "*.spec.ts" \
                                -o -name "*.spec.tsx" \
                            \\) \
                            -not -path "./node_modules/*" \
                            -not -path "./dist/*" \
                            | head -20
                    )

                    if [ -n "$FRONTEND_TEST_FILES" ]; then
                        echo "Frontend test files found:"
                        echo "$FRONTEND_TEST_FILES"

                        npm run test -- --run
                    else
                        echo "No frontend test files found."
                        echo "Skipping frontend test execution."
                    fi

                    echo "=============================================="
                    echo "Frontend Build"
                    echo "=============================================="

                    npm run build

                    test -d dist
                    test -f dist/index.html

                    echo "Frontend build passed."
                '''
            }
        }

        stage("Security Checks") {
            steps {
                echo "Running security checks..."

                sh '''
                    set -eu

                    echo "=============================================="
                    echo "Private Key Check"
                    echo "=============================================="

                    if find "$WORKSPACE" \
                        -type f \
                        \\( \
                            -name "*.pem" \
                            -o -name "*.key" \
                            -o -name "id_rsa" \
                            -o -name "id_ed25519" \
                        \\) \
                        -not -path "$WORKSPACE/.git/*" \
                        -not -path "$WORKSPACE/.venv-ci/*" \
                        -not -path "$WORKSPACE/frontend/node_modules/*" \
                        | grep -q .; then

                        echo "ERROR: Private key-like file detected."

                        find "$WORKSPACE" \
                            -type f \
                            \\( \
                                -name "*.pem" \
                                -o -name "*.key" \
                                -o -name "id_rsa" \
                                -o -name "id_ed25519" \
                            \\) \
                            -not -path "$WORKSPACE/.git/*" \
                            -not -path "$WORKSPACE/.venv-ci/*" \
                            -not -path "$WORKSPACE/frontend/node_modules/*"

                        exit 1
                    fi

                    echo "No private key files detected."

                    echo "=============================================="
                    echo "Kubernetes Secret Check"
                    echo "=============================================="

                    kubectl get secret monitoring-secret \
                        -n "${K8S_NAMESPACE}" \
                        >/dev/null

                    echo "monitoring-secret exists."

                    echo "Security checks passed."
                '''
            }
        }

        stage("Build Backend Image") {
            steps {
                echo "Building backend container image..."

                sh '''
                    set -eu

                    podman build \
                        --file "$WORKSPACE/backend/Containerfile" \
                        --tag "${BACKEND_IMAGE}:${IMAGE_TAG}" \
                        "$WORKSPACE/backend"

                    podman image exists \
                        "${BACKEND_IMAGE}:${IMAGE_TAG}"

                    echo "Backend image build passed."

                    podman images "${BACKEND_IMAGE}"
                '''
            }
        }

        stage("Build Frontend Image") {
            steps {
                echo "Building frontend container image..."

                sh '''
                    set -eu

                    podman build \
                        --file "$WORKSPACE/frontend/Containerfile" \
                        --tag "${FRONTEND_IMAGE}:${IMAGE_TAG}" \
                        "$WORKSPACE/frontend"

                    podman image exists \
                        "${FRONTEND_IMAGE}:${IMAGE_TAG}"

                    echo "Frontend image build passed."

                    podman images "${FRONTEND_IMAGE}"
                '''
            }
        }

        stage("Build Agent Image") {
            steps {
                echo "Building monitoring agent container image..."

                sh '''
                    set -eu

                    podman build \
                        --file "$WORKSPACE/agent/Containerfile" \
                        --tag "${AGENT_IMAGE}:${IMAGE_TAG}" \
                        "$WORKSPACE/agent"

                    podman image exists \
                        "${AGENT_IMAGE}:${IMAGE_TAG}"

                    echo "Agent image build passed."

                    podman images "${AGENT_IMAGE}"
                '''
            }
        }

        stage("Image Verification") {
            steps {
                echo "Verifying container images..."

                sh '''
                    set -eu

                    echo "Backend:"
                    podman image inspect \
                        "${BACKEND_IMAGE}:${IMAGE_TAG}" \
                        >/dev/null

                    echo "Frontend:"
                    podman image inspect \
                        "${FRONTEND_IMAGE}:${IMAGE_TAG}" \
                        >/dev/null

                    echo "Agent:"
                    podman image inspect \
                        "${AGENT_IMAGE}:${IMAGE_TAG}" \
                        >/dev/null

                    echo "All container images verified."
                '''
            }
        }

        stage("Container Smoke Tests") {
            steps {
                echo "Running container smoke tests..."

                sh '''
                    set -eu

                    echo "=============================================="
                    echo "Backend Smoke Test"
                    echo "=============================================="

                    podman run \
                        --rm \
                        "${BACKEND_IMAGE}:${IMAGE_TAG}" \
                        python --version

                    echo "=============================================="
                    echo "Frontend Smoke Test"
                    echo "=============================================="

                    podman run \
                        --rm \
                        "${FRONTEND_IMAGE}:${IMAGE_TAG}" \
                        nginx -v

                    echo "=============================================="
                    echo "Agent Smoke Test"
                    echo "=============================================="

                    podman run \
                        --rm \
                        "${AGENT_IMAGE}:${IMAGE_TAG}" \
                        python --version

                    echo "Container smoke tests passed."
                '''
            }
        }

        stage("Import Images Into k3s") {
            steps {
                echo "Importing images into k3s/containerd..."

                sh '''
                    set -eu

                    BACKEND_TAR="$WORKSPACE/backend-${IMAGE_TAG}.tar"
                    FRONTEND_TAR="$WORKSPACE/frontend-${IMAGE_TAG}.tar"
                    AGENT_TAR="$WORKSPACE/agent-${IMAGE_TAG}.tar"

                    rm -f "$BACKEND_TAR"
                    rm -f "$FRONTEND_TAR"
                    rm -f "$AGENT_TAR"

                    echo "=============================================="
                    echo "Saving Backend Image"
                    echo "=============================================="

                    podman save \
                        --output "$BACKEND_TAR" \
                        "${BACKEND_IMAGE}:${IMAGE_TAG}"

                    echo "=============================================="
                    echo "Saving Frontend Image"
                    echo "=============================================="

                    podman save \
                        --output "$FRONTEND_TAR" \
                        "${FRONTEND_IMAGE}:${IMAGE_TAG}"

                    echo "=============================================="
                    echo "Saving Agent Image"
                    echo "=============================================="

                    podman save \
                        --output "$AGENT_TAR" \
                        "${AGENT_IMAGE}:${IMAGE_TAG}"

                    echo "=============================================="
                    echo "Importing Backend Image"
                    echo "=============================================="

                    k3s ctr images import "$BACKEND_TAR"

                    echo "=============================================="
                    echo "Importing Frontend Image"
                    echo "=============================================="

                    k3s ctr images import "$FRONTEND_TAR"

                    echo "=============================================="
                    echo "Importing Agent Image"
                    echo "=============================================="

                    k3s ctr images import "$AGENT_TAR"

                    echo "=============================================="
                    echo "Verifying Backend Image"
                    echo "=============================================="

                    k3s ctr images ls | grep \
                        "localhost/devops-monitoring-backend:${IMAGE_TAG}"

                    echo "=============================================="
                    echo "Verifying Frontend Image"
                    echo "=============================================="

                    k3s ctr images ls | grep \
                        "localhost/devops-monitoring-frontend:${IMAGE_TAG}"

                    echo "=============================================="
                    echo "Verifying Agent Image"
                    echo "=============================================="

                    k3s ctr images ls | grep \
                        "localhost/devops-monitoring-agent:${IMAGE_TAG}"

                    echo "k3s image import and verification passed."
                '''
            }
        }

        stage("Update Kubernetes Images") {
            steps {
                echo "Updating Kubernetes manifests with build tag..."

                sh '''
                    set -eu

                    sed -i \
                        "s|image: localhost/devops-monitoring-backend:.*|image: localhost/devops-monitoring-backend:${IMAGE_TAG}|" \
                        "$WORKSPACE/deployment/kubernetes/backend.yaml"

                    sed -i \
                        "s|image: localhost/devops-monitoring-frontend:.*|image: localhost/devops-monitoring-frontend:${IMAGE_TAG}|" \
                        "$WORKSPACE/deployment/kubernetes/frontend.yaml"

                    sed -i \
                        "s|image: localhost/devops-monitoring-agent:.*|image: localhost/devops-monitoring-agent:${IMAGE_TAG}|" \
                        "$WORKSPACE/deployment/kubernetes/agent.yaml"

                    echo "=============================================="
                    echo "Backend Image"
                    echo "=============================================="

                    grep -n "image:" \
                        "$WORKSPACE/deployment/kubernetes/backend.yaml"

                    echo "=============================================="
                    echo "Frontend Image"
                    echo "=============================================="

                    grep -n "image:" \
                        "$WORKSPACE/deployment/kubernetes/frontend.yaml"

                    echo "=============================================="
                    echo "Agent Image"
                    echo "=============================================="

                    grep -n "image:" \
                        "$WORKSPACE/deployment/kubernetes/agent.yaml"

                    echo "Kubernetes image update passed."
                '''
            }
        }

        stage("Kubernetes Validation") {
            steps {
                echo "Validating Kubernetes manifests..."

                sh '''
                    set -eu

                    kubectl apply \
                        --dry-run=server \
                        -f "$WORKSPACE/deployment/kubernetes/namespace.yaml" \
                        -f "$WORKSPACE/deployment/kubernetes/configmap.yaml" \
                        -f "$WORKSPACE/deployment/kubernetes/postgres.yaml" \
                        -f "$WORKSPACE/deployment/kubernetes/backend.yaml" \
                        -f "$WORKSPACE/deployment/kubernetes/frontend.yaml" \
                        -f "$WORKSPACE/deployment/kubernetes/agent.yaml" \
                        -f "$WORKSPACE/deployment/kubernetes/services.yaml" \
                        -f "$WORKSPACE/deployment/kubernetes/ingress.yaml"

                    echo "Kubernetes server-side validation passed."
                '''
            }
        }

        stage("Deploy To Kubernetes") {
            steps {
                echo "Deploying application to Kubernetes..."

                sh '''
                    set -eu

                    kubectl apply \
                        -f "$WORKSPACE/deployment/kubernetes/namespace.yaml" \
                        -f "$WORKSPACE/deployment/kubernetes/configmap.yaml" \
                        -f "$WORKSPACE/deployment/kubernetes/postgres.yaml" \
                        -f "$WORKSPACE/deployment/kubernetes/backend.yaml" \
                        -f "$WORKSPACE/deployment/kubernetes/frontend.yaml" \
                        -f "$WORKSPACE/deployment/kubernetes/agent.yaml" \
                        -f "$WORKSPACE/deployment/kubernetes/services.yaml" \
                        -f "$WORKSPACE/deployment/kubernetes/ingress.yaml"

                    echo "Kubernetes deployment applied successfully."
                '''
            }
        }

        stage("Rollout Verification") {
            steps {
                echo "Waiting for Kubernetes rollouts..."

                sh '''
                    set -eu

                    echo "Postgres rollout..."

                    kubectl rollout status \
                        deployment/postgres \
                        -n "${K8S_NAMESPACE}" \
                        --timeout=180s

                    echo "Backend rollout..."

                    kubectl rollout status \
                        deployment/backend \
                        -n "${K8S_NAMESPACE}" \
                        --timeout=180s

                    echo "Frontend rollout..."

                    kubectl rollout status \
                        deployment/frontend \
                        -n "${K8S_NAMESPACE}" \
                        --timeout=180s

                    echo "Monitoring agent rollout..."

                    kubectl rollout status \
                        deployment/monitoring-agent \
                        -n "${K8S_NAMESPACE}" \
                        --timeout=180s

                    echo "All Kubernetes rollouts completed successfully."
                '''
            }
        }

        stage("Application Verification") {
            steps {
                echo "Verifying deployed application..."

                sh '''
                    set -eu

                    echo "=============================================="
                    echo "Pods"
                    echo "=============================================="

                    kubectl get pods \
                        -n "${K8S_NAMESPACE}" \
                        -o wide

                    echo "=============================================="
                    echo "Services"
                    echo "=============================================="

                    kubectl get svc \
                        -n "${K8S_NAMESPACE}"

                    echo "=============================================="
                    echo "Ingress"
                    echo "=============================================="

                    kubectl get ingress \
                        -n "${K8S_NAMESPACE}"

                    echo "=============================================="
                    echo "Endpoints"
                    echo "=============================================="

                    kubectl get endpoints \
                        -n "${K8S_NAMESPACE}" \
                        backend frontend postgres

                    echo "=============================================="
                    echo "Backend Health"
                    echo "=============================================="

                    HEALTH_RESPONSE=$(kubectl exec \
                        -n "${K8S_NAMESPACE}" \
                        deployment/backend \
                        -- python -c \
                        "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/health').read().decode())")

                    echo "$HEALTH_RESPONSE"

                    echo "$HEALTH_RESPONSE" | grep '"status":"healthy"'
                    echo "$HEALTH_RESPONSE" | grep '"database":"connected"'

                    echo "=============================================="
                    echo "Monitoring Agent Logs"
                    echo "=============================================="

                    kubectl logs \
                        -n "${K8S_NAMESPACE}" \
                        deployment/monitoring-agent \
                        --tail=10

                    echo "Application verification passed."
                '''
            }
        }

        stage("External Application Verification") {
            steps {
                echo "Verifying the public application endpoint..."

                sh '''
                    set -eu

                    echo "=============================================="
                    echo "Frontend"
                    echo "=============================================="

                    FRONTEND_CODE=$(curl \
                        --silent \
                        --output /dev/null \
                        --write-out "%{http_code}" \
                        --max-time 15 \
                        http://127.0.0.1/)

                    echo "Frontend HTTP status: ${FRONTEND_CODE}"

                    if [ "${FRONTEND_CODE}" != "200" ]; then
                        echo "ERROR: Frontend did not return HTTP 200."
                        exit 1
                    fi

                    echo "=============================================="
                    echo "Protected Backend API"
                    echo "=============================================="

                    API_CODE=$(curl \
                        --silent \
                        --output "$WORKSPACE/backend-api-response.txt" \
                        --write-out "%{http_code}" \
                        --max-time 15 \
                        http://127.0.0.1/api/servers)

                    echo "Backend API HTTP status: ${API_CODE}"

                    cat "$WORKSPACE/backend-api-response.txt"

                    echo

                    if [ "${API_CODE}" != "401" ]; then
                        echo "ERROR: Protected backend API should return HTTP 401 without a token."
                        exit 1
                    fi

                    echo "External application verification passed."
                '''
            }
        }

        stage("Final Verification") {
            steps {
                echo "Performing final verification..."

                sh '''
                    set -eu

                    echo "=============================================="
                    echo "Backend Deployed Image"
                    echo "=============================================="

                    kubectl get deployment backend \
                        -n "${K8S_NAMESPACE}" \
                        -o jsonpath='{.spec.template.spec.containers[0].image}'

                    echo

                    echo "=============================================="
                    echo "Frontend Deployed Image"
                    echo "=============================================="

                    kubectl get deployment frontend \
                        -n "${K8S_NAMESPACE}" \
                        -o jsonpath='{.spec.template.spec.containers[0].image}'

                    echo

                    echo "=============================================="
                    echo "Agent Deployed Image"
                    echo "=============================================="

                    kubectl get deployment monitoring-agent \
                        -n "${K8S_NAMESPACE}" \
                        -o jsonpath='{.spec.template.spec.containers[0].image}'

                    echo

                    echo "=============================================="
                    echo "Deployments"
                    echo "=============================================="

                    kubectl get deployments \
                        -n "${K8S_NAMESPACE}"

                    echo "=============================================="
                    echo "Pods"
                    echo "=============================================="

                    kubectl get pods \
                        -n "${K8S_NAMESPACE}"

                    echo "=============================================="
                    echo "Final verification passed."
                    echo "=============================================="
                '''
            }
        }
    }

    post {

        success {
            echo """
============================================================
CI/CD PIPELINE SUCCESSFUL
============================================================

Project:
${PROJECT_NAME}

Build:
${BUILD_NUMBER}

Backend:
${BACKEND_IMAGE}:${IMAGE_TAG}

Frontend:
${FRONTEND_IMAGE}:${IMAGE_TAG}

Agent:
${AGENT_IMAGE}:${IMAGE_TAG}

Kubernetes Namespace:
${K8S_NAMESPACE}

Status:
DEPLOYMENT SUCCESSFUL

============================================================
"""
        }

        failure {
            echo """
============================================================
CI/CD PIPELINE FAILED
============================================================

Project:
${PROJECT_NAME}

Build:
${BUILD_NUMBER}

The pipeline stopped at the first failed stage.

Check the Jenkins console for the exact error.

============================================================
"""
        }

        always {
            sh '''
                set +e

                echo "=============================================="
                echo "CI Cleanup"
                echo "=============================================="

                rm -rf "$WORKSPACE/.venv-ci"

                rm -f "$WORKSPACE/.devops-monitoring-ci.db"

                rm -f "$WORKSPACE/backend-${IMAGE_TAG}.tar"
                rm -f "$WORKSPACE/frontend-${IMAGE_TAG}.tar"
                rm -f "$WORKSPACE/agent-${IMAGE_TAG}.tar"

                rm -f "$WORKSPACE/backend-api-response.txt"

                echo "CI cleanup completed."
            '''
        }
    }
}
