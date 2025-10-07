# 100m Dash Time Recorder

## Problem Statement

You are tasked with developing a Python program to assist in recording 100m dash times for an upcoming USAFA track meet.

## Requirements

1. **Input:**
    - Prompt the user for the number of cadets participating.
    - For each cadet, collect:
        - Last name
        - Squadron number
        - 100m dash time (in seconds)

2. **Output:**
    - Display the squadron number and 100m dash time of the cadet with the **fastest** time.
        - If multiple cadets share the fastest time, display the squadron and time of the **last** such cadet entered.
    - Display the **number of cadets** whose 100m dash time was **faster than the average**.

### Example Input and Output

| Name | Squadron Number | 100m Dash Time |
| - | - | - |
| Jones | 22 | 9.9 |

## Additional Notes

- There is **no upper limit** on the number of cadets; however, at least one cadet will be entered.
- Ensure all prompts and outputs are clear and user-friendly.

---

**Example Output:**
```
Fastest: Squadron 23, Time: 11.02
Number of cadets faster than average: 3
```