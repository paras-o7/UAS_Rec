# Challenge
We are given 10 images, and are expected to find the best rescue camp based on the priority score for each person, keeping in mind that each rescue camp has a maximum capacity.

Priority Order for casualties:
- Star - 3 (Child)
- Triangle - 2 (Elder)
- Square - 1 (Adult)

Priority Order for emergency:
- Severe - 3 (Red)
- Mild - 2 (Yellow)
- Safe - 1 (Green)

Priority Score = casualty * emergency
> In case of a tie, the one with the higher emergency score will be given preference.

> Each camp should have the highest possible total priority score.

Max capacity of each camp:
- Pink: 3
- Blue: 4
- Grey: 2