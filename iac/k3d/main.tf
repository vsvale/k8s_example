provider "kubernetes" {
  config_context_cluster = "k3d-kappa"
  config_path            = "~/.kube/config"
}

resource "kubernetes_namespace" "orchestrator" {
  metadata {
    name = "orchestrator"
  }
}

resource "kubernetes_namespace" "database" {
  metadata {
    name = "database"
  }
}

resource "kubernetes_namespace" "ingestion" {
  metadata {
    name = "ingestion"
  }
}

resource "kubernetes_namespace" "processing" {
  metadata {
    name = "processing"
  }
}

resource "kubernetes_namespace" "datastore" {
  metadata {
    name = "datastore"
  }
}

resource "kubernetes_namespace" "deepstorage" {
  metadata {
    name = "deepstorage"
  }
}

resource "kubernetes_namespace" "tracing" {
  metadata {
    name = "tracing"
  }
}

resource "kubernetes_namespace" "logging" {
  metadata {
    name = "logging"
  }
}

resource "kubernetes_namespace" "monitoring" {
  metadata {
    name = "monitoring"
  }
}

resource "kubernetes_namespace" "viz" {
  metadata {
    name = "viz"
  }
}

resource "kubernetes_namespace" "cicd" {
  metadata {
    name = "cicd"
  }
}

resource "kubernetes_namespace" "security" {
  metadata {
    name = "security"
  }
}

resource "kubernetes_namespace" "app" {
  metadata {
    name = "app"
  }
}

resource "kubernetes_namespace" "cost" {
  metadata {
    name = "cost"
  }
}

resource "kubernetes_namespace" "misc" {
  metadata {
    name = "misc"
  }
}

resource "kubernetes_namespace" "dataops" {
  metadata {
    name = "dataops"
  }
}

resource "kubernetes_namespace" "gateway" {
  metadata {
    name = "gateway"
  }
}

resource "kubernetes_namespace" "gateway" {
  metadata {
    name = "serving"
  }
}