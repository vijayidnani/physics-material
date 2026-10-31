# SPS Integrated Programme — JEE Test Series Performance Analysis Portal

## Included files
- `portal.html` — responsive portal with Overview, Student Report, Teacher Dashboard and Question Analysis.
- `tests.json` — current supplied dataset, normalised with `branch: "SN"`.

## Deploy
Upload both files into the same GitHub Pages folder. Keep the filename `tests.json` unchanged because the portal fetches `./tests.json`.

## Current data coverage
The supplied files contain SN Branch / JM Revision Test 3 data only. The portal is prepared for branches SN, RN, GN and KE and multiple tests, but it will only display records actually added to `tests.json`.

## Adding future tests and branches
Add another test object to the top-level JSON array. Keep the same fields as the existing object and add:
- `branch`: one of `SN`, `RN`, `GN`, `KE`
- `name`, `id`, `date`, `max`, `mc`, `mw`
- `key`: answer-key array
- `q`: question map array (subject, chapter, topic, subtopic)
- `students`: array of student objects, each with `name`, `roll`, `cls`, optional `section`, `rankSN`, `rankAll`, and `r` (response array).

Each student's `r` array must align position-by-position with `q` and `key`.

## PDF report
Open Student Report, select a student and use “Download / Print PDF”. In the print dialog choose “Save as PDF”.

## Important security note
This is a GitHub Pages static front end. The JSON file is public and anyone who can access the site can inspect its contents. Do not upload identifiable student data to a public repository for real student use. For production student access, connect the portal to an authenticated backend (for example, Supabase Auth + Row Level Security) so students can only retrieve their own records and teachers can retrieve only their authorised cohorts.

## Data integrity notes
- Rank fields are displayed as supplied in the uploaded data.
- Subject names and chapter/topic mapping are taken from the supplied `tests.json`.
- Accuracy is calculated as correct answers divided by attempted answers.
- Attempted questions = correct + incorrect.
- Score uses the supplied marking scheme (`mc` for correct, `mw` for incorrect, zero for unattempted).
- Success rate in Question Analysis = number correct divided by students in the currently selected cohort.
