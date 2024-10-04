resource "google_pubsub_topic" "succeededjob" {
  provider = google-beta
  name     = "topic-succeeded-job"
  project  = var.project
}

resource "google_pubsub_subscription" "succeededjob" {
  provider             = google-beta
  project              = var.project
  name                 = "sub-topic-succeeded-job"
  topic                = google_pubsub_topic.succeededjob.id
  ack_deadline_seconds = 600
}

resource "google_storage_notification" "notification" {
  bucket         = google_storage_bucket.servier_buckets["servierdataextract"].name
  payload_format = "JSON_API_V1"
  topic          = google_pubsub_topic.succeededjob.id
  event_types    = ["OBJECT_FINALIZE", "OBJECT_METADATA_UPDATE"]
  
  depends_on = [google_pubsub_topic_iam_binding.topic_iam_binding]
}
