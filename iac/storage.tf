resource "google_storage_bucket" "servier_buckets" {
  for_each = {
    servierconfigs     = "servierconfigs"
    servierdataextract = "servierdataextract"
    tfdeploy           = "gcs-terraform-deploy"
  }
  provider                    = google-beta
  project                     = var.project
  name                        = each.value
  location                    = "EU"
  force_destroy               = each.key == "servierconfigs" ? true : false
  uniform_bucket_level_access = false
  public_access_prevention    = each.key == "servierconfigs" ? "enforced" : null
}

resource "google_storage_bucket_object" "object" {
  name   = "index.zip"
  bucket = google_storage_bucket.servier_buckets["tfdeploy"].name
  source = "../modules/data_extractor.zip"
}
