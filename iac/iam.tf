data "google_storage_project_service_account" "storage_service_account" {
  project = var.project
}

resource "google_service_account" "service_account" {
  account_id   = "cf-service-account"
  display_name = "Cloud Function Service Account"
  project      = var.project
}

resource "google_pubsub_topic_iam_binding" "topic_iam_binding" {
  topic   = google_pubsub_topic.succeededjob.id
  role    = "roles/pubsub.publisher"
  members = ["serviceAccount:${data.google_storage_project_service_account.storage_service_account.email_address}"]
}

resource "google_project_iam_member" "permissions" {
  for_each = toset(["bigquery.dataEditor", "bigquery.jobUser", "datastore.viewer", "storage.admin"])
  project  = var.project
  role     = "roles/${each.key}"
  member   = "serviceAccount:${google_service_account.service_account.email}"
  provider = google-beta
}
