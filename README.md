Worker Tracker
=======================

Currently running on workertracker.herokuapp.com

Summary
=====================
The app tracks the worker that workers on amazon's mechanical turk does and syncronously updates their performance on gold standard tasks. It constantly checks for new hits that automatically approves good work. If does not reject bad work automatically but waits for a predefined window of hits. If the worker's performance over the gold standard tasks in the window of hits is below our acceptance standard, the window of hits are rejected.

Feedback
=====================
By evaluating workers over a window, we allow workers to receive feedback every single hit. We send them a detailed email informing them of the quality of their work for EVERY single hit.
The app also allows you to switch this functionality off, so you can choose to send feedback or not.

Improving over time
=====================
The system will only judge workers on a window of their last hits. If worker's find that their work has been rejected, they don't have to worry about having all of their future work rejected. Instead, they can try to improve their score by performing better on future hits. Since we consider only a window of their past hits, a worker who used to perform poorly can improve over time by doing better work. 

