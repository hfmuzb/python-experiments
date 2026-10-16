# Publish checklist: article 1

## 1. Regenerate the figures
```bash
uv run make-figures 01
```
This writes `out/architecture.png`, `out/dh-frames.png` and `out/budget.png`.

## 2. Upload the media (admin → /admin/media)
Upload all three files and copy each URL.

## 3. Create the post (admin → /admin/posts/new)
| Field | Value |
|---|---|
| Title | building a $500 6-dof robot arm: the plan |
| Slug | robot-arm-01-the-plan |
| Summary | A six-axis robot arm I design, print, wire and program myself for $500: requirements, architecture, Denavit–Hartenberg geometry and the budget. Part 1 of a series. |
| Tags | robotics, robot-arm, python, kinematics, 3d-printing |
| Cover image | the uploaded `dh-frames.png` URL |
| Content | `article.mdx`, with the three `REPLACE_ME/…` sources replaced by the uploaded URLs |
| Published | off at first |

## 4. Preview (`/blog/preview/<id>`)
- [ ] All three figures load
- [ ] The DH matrix and the DH table (KaTeX array) render; no red KaTeX errors
- [ ] Dollar amounts show as `$500`, not as math
- [ ] The code block has highlighting and the copy button works
- [ ] The GitHub link opens python-experiments

## 5. Publish
Turn on Published and save. The post page revalidates on save.
