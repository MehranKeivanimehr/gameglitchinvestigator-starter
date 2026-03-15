# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it? OK, but without a part to say you were correct or not. 
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  a) once you uncheck the hint, you cannot get the hint back by checking it again. It is supposed to bring it back by check mark.
  b) The hint is swapped. When it is "Too High" it is suppose to "Go Lower" and when it is "Too Low" it is supposed to say "Go Higher".
  c) The penalty is on Too High only.
  d) There is not a message that tells you you are wrong. 
  e) Trying with number for a couple of times, use your attempts.
  f) when you press new game, it doesnt start a new game. It should start a new one. 
  g) the hint is wrong sometimes. Like the secret is 81, I entered 34 and hinted out GO LOWER!
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? Copilot and Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

Claude Code suggested moving duplicated game logic functions such as check_guess, parse_guess, get_range_for_difficulty, and update_score out of app.py and importing them from logic_utils.py. 
This suggestion was correct. It improved the code structure by separating core logic from Streamlit UI code.
I reviewed the diff in app.py, confirmed the duplicate functions were removed, checked that the import from logic_utils.py was added, and ran the app and tests to make sure the refactor did not break functionality.


- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

Earlier game behavior allowed the secret value to be converted to a string before calling check_guess on some attempts. This was incorrect or misleading because the comparison logic should consistently use integers. Passing a string could cause incorrect hint behavior or unreliable comparisons. I inspected the relevant code path in app.py, removed the string conversion, and then verified the fix by running pytest and checking that the guess logic behaved correctly in the live app.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I decided a bug was really fixed by checking both the code change and the actual behavior after the change. I reviewed the diff, ran the tests, and confirmed the game produced the correct high/low hints in the live app.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

  One pytest test I ran checked that a guess higher than the secret returns the “Too High” result. This showed that the repaired check_guess logic was working correctly and that the comparison bug was no longer affecting the outcome.

- Did AI help you design or understand any tests? How?

Yes. AI helped me design the regression test by suggesting a simple pytest case focused on the exact bug I fixed. I still reviewed the test myself and used the test results to verify that the fix was correct.
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
