# Google download collection
User authorized automatic official Google download collection into the existing combined admin screen.
- Reuse private Google service-account credential already stored server-side; obtain the verified Play report bucket URI from the official console, never guess it from the developer ID.
- Read only country-dimension monthly installation CSVs with devstorage.read_only. Decode UTF-16, validate package/date/count and prevent duplicate dimension counting. Missing reports remain null; auth/permission/schema errors are distinct.
- Run a private Edge Function on a dedicated secret-authenticated twice-daily database schedule. Never expose keys or raw reports to the frontend. Update existing owner-only google_downloads runtime, separate execution/setup status, preserve manual release state. No finance or publication access.
- Add parser/aggregation failure tests first, implement, validate and deploy. If bucket or permission unavailable, deploy an honest setup-required state; do not report data-connected before authenticated GCS access succeeds. Prepare the exact service-account read grant for user confirmation if required.
