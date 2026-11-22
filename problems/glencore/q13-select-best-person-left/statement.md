You are a recruiter working for an organization of superhumans. You got some results of a test on which many applicants participated. They consist in a correspondance between the candidate's name and the final score.

You would like to hire the person with the best score, but your test results are a bit outdated. All the superhumans with a score strictly above a given threshold were already recruited by the X-Hens (a rival organization). So, you must filter your results before selecting the person with the best score.

All the scores and the threshold are positive or zero.

The answer is guaranteed to be unique. After filtering, there will always be exactly one person with the best score.

### Detailed Example

In the first test case, there are 5 superhumans. Here are their names and associated score:

- Quicksnail: 140
- Grey Widow: 246
- Magnetoast: 228
- Pyro Girl: 157
- Captain Confetti: 87

The given treshold is 200. So, there are 3 superhumans left:

- Quicksnail: 140
- Pyro Girl: 157
- Captain Confetti: 87

The one with the highest score is "Pyro Girl". Your code must return the string `Pyro Girl`.

### Implementation

**Function** — Implement the function `select_best_person_left`.

**Parameters**

| Name | Type | Description |
|---|---|---|
| `test_result` | dict | The score corresponding to each superhuman. |
| `threshold` | int | The score threshold above which superhumans should be ignored. |

**Return value**

| Name | Type | Description |
|---|---|---|
| `output` | str | The name of the person to hire. |

**Constraints**

- 0 <= threshold
- Available RAM: 512MB
- Timeout: 6 seconds

### Tests

- **Example** — parameters `{Quicksnail: 140, Grey Widow: 246, Magnetoast: 228, ...}, 200` → `Pyro Girl`
- **No need to filter**
- **Same scores, except the filtered best**
