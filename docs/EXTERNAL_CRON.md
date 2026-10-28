# External cron trigger for the daily edition

## Current status (update this when anything changes)
| Item | Value |
| --- | --- |
| Service | cron-job.org (account settings: https://console.cron-job.org/settings) |
| Set up by / on | repository owner, 2026-10-28 |
| Jobs | daily 08:00 and 08:20, time zone America/New_York, POST to the `daily.yml` dispatch endpoint with `{"ref":"main"}` |
| Token | fine-grained PAT, `Sukonik/goldbrief` only, Actions: read/write |
| Token expires | _fill in: ____ (set a reminder 2 weeks earlier)_ |
| First confirmed run | _fill in after the first 08:00 ET run appears in the Actions tab as `workflow_dispatch` from the token owner_ |
| Backup triggers | five GitHub schedules in `daily.yml` (12:07, 12:37, 13:07, 13:37, 14:07 UTC) |

## Runbook: what to check when the news looks stale
1. Open the repository **Actions** tab, workflow "GoldBrief Daily News". Is there a run today?
2. **No run at all:** check cron-job.org's job history. A 401 means the token expired or was revoked (rotate it, below). A 404 usually means a wrong URL. Anything other than 204 is a failure.
3. **Run exists but skipped quickly ("No new edition due"):** expected after the first success of the day, or outside the 8-10 AM ET window.
4. **Run failed:** read its log. A push rejection is retried automatically; a feed outage keeps the previous edition and shows the stale notice on the site.
5. To publish immediately: Actions -> "GoldBrief Daily News" -> Run workflow -> tick **force**.
6. The site shows the edition date and collection time on the news pages. `data/daily.json` has `actual_run_et`.

## Rotation checklist (before the token expires)
1. GitHub -> Settings -> Developer settings -> Fine-grained tokens: generate a new token with the same single-repo, Actions read/write scope.
2. In cron-job.org, edit **both** jobs and replace the `Authorization: Bearer ...` header.
3. Use cron-job.org's "Test run" and confirm a `workflow_dispatch` run appears in Actions.
4. Delete the old token. Update the "Token expires" row above.

GitHub's own scheduler is best-effort and skipped the 2026-10-28 morning run. A free external cron service can call GitHub's workflow-dispatch API instead. This is a second, independent trigger: the five GitHub schedules stay in place as backups.

**Why it is safe to ping more than once.** A dispatch with no inputs is *not* forced. `scripts/daily_update.py` publishes only inside the 8–10 AM America/New_York window and only once per ET day; every other ping exits in seconds without committing. To recollect on demand, dispatch with `force=true`.

## 1. Create a fine-grained GitHub token (you do this; do not paste it into chat)
GitHub → Settings → Developer settings → Personal access tokens → **Fine-grained tokens** → Generate new token.
- **Repository access:** *Only select repositories* → `Sukonik/goldbrief`.
- **Permissions → Repository → Actions: Read and write.** Nothing else.
- **Expiration:** the longest allowed (up to 1 year). Put a calendar reminder two weeks before it expires.
- Copy the token once; it is shown only once.

## 2. Create the cron jobs on cron-job.org (free)
Create an account at https://cron-job.org, then **Create cronjob** twice (one backup is cheap insurance):

| Setting | Job A | Job B |
| --- | --- | --- |
| Title | GoldBrief daily 8:00 ET | GoldBrief daily 8:20 ET |
| URL | `https://api.github.com/repos/Sukonik/goldbrief/actions/workflows/daily.yml/dispatches` | same |
| Schedule | every day at **08:00** | every day at **08:20** |
| Time zone | **America/New_York** (so daylight saving is handled for you) | same |
| Advanced → Request method | **POST** | **POST** |
| Advanced → Request body | `{"ref":"main"}` | same |
| Advanced → Headers | see below | same |
| Notifications | notify on failure | notify on failure |

Headers (add each as a separate header):
```
Authorization: Bearer <YOUR_TOKEN>
Accept: application/vnd.github+json
X-GitHub-Api-Version: 2022-11-28
Content-Type: application/json
```
Paste the token directly into cron-job.org, never into a repository file, issue or chat. A successful dispatch returns **HTTP 204**; enable "treat other status as failure" so errors alert you.

Start at 08:00 ET rather than 08:30 so the run (about a minute) finishes with margin before 8:30.

## 3. Test it
From any terminal (token in an environment variable, not typed into history):
```bash
curl -i -X POST \
  -H "Authorization: Bearer $GOLDBRIEF_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/Sukonik/goldbrief/actions/workflows/daily.yml/dispatches \
  -d '{"ref":"main"}'
```
Expect `HTTP/2 204`. Then open the repository's **Actions** tab: a new "GoldBrief Daily News" run should appear with event *workflow_dispatch*. Outside the 8–10 AM ET window, or after today's edition exists, it finishes in seconds with "No new edition due". Inside the window with no edition yet, it publishes.

## 4. Monitoring
- The news pages show the edition date and a notice if today's edition has not published.
- cron-job.org emails you if the call fails (for example an expired token returns 401).
- `data/daily.json` records `actual_run_et`, the real publish time.

## Rotation and revocation
Create a new token before the old one expires, update both jobs' `Authorization` header, then delete the old token. If a token is ever exposed, revoke it immediately in GitHub settings; it can only trigger workflows in this one repository.
