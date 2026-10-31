# SN Branch Result Portal: how it is updated

The published page is one static HTML file. `template.html` holds the design and logic, and `tests.json` holds one entry per test. The page is rebuilt by replacing `/*__DATA__*/[]` in the template with the contents of `tests.json`, then republishing the same artifact.

## Adding a new test (done in chat)
Share these four files for the new test:
1. Compiled result PDF (all branches, used for overall rank)
2. Question-wise analysis PDF (SN students only: answers, key, SN rank)
3. Question to topic mapping Excel (Q no, Subject, JEE Main Chapter, Topic, Subtopic)
4. Question paper PDF (reference)

Then append a test object to `tests.json` and republish.

## Test object format
```
{ "id": "jm-rev-4", "name": "JM Revision Test 4", "date": "YYYY-MM-DD",
  "max": 300, "mc": 4, "mw": -1, "overallCount": 73,
  "key": ["C","D", ...],                 // one entry per question
  "q": [["Physics","Chapter","Topic","Subtopic"], ...],
  "students": [ { "name": "...", "roll": "1002", "cls": "12A",
                  "rankSN": 11, "rankAll": 46,
                  "r": ["D","","A", ...] } ] }   // marked answer, "" = not attempted
```

## Rules used
- Only branch SN students are included. Students are matched across tests by name.
- Marking: +4 right, -1 wrong, 0 not attempted (as printed on the paper).
- rankSN is the rank printed in the question-wise analysis (dense ranking among SN students). rankAll is the rank in the compiled result (competition ranking among all 73).
- Chapter status: Strong 70% or more right, Revise 40 to 69%, Weak below 40%.
- Checks done for Test 3: key identical across all 24 students; every student's per-question marks, subject scores and total match the compiled result; Q-to-subject mapping matches the analysis.

## Tests loaded
- JM Revision Test 3, 31 Oct 2026: 24 SN students, 75 questions.
