# Mandatory assignment 1 

Inf-2200 at UiT The Arctic University of Norway in fall 2021.

This is a group assignment, to be done in groups of two. You need to select a partner in your colloquium group.

The design review times, and hand-in time are in Canvas.

## Detailed description

In this first assignment you will compare your assembly coding skills against a compiler. To do this you will implement a microbenchmark in C and x86 assembly, and then compare their performance. 

Your first task is to **select a program to create microbenchmark**. A microbenchmark is a simplified version of a larger program, often containing only the main loop. It should however be realistic and therefore represent a real program. It should also be relevant, and stress in this case the CPU. The microbenchmark should therefore be CPU-bound, and not I/O bound. It should also be repeatable. Two executions should produce the same results. To simplify the assignment, you should select a single-threaded microbenchmark, and you do not want to use floating point operations. Note that you must also get or create a realistic dataset for your microbenchmark.

Second, **identify the main hotspot** in the microbenchmark. This will be the portion of the code you will implement in assembly. A hotspot is where in the benchmark most of the execution time is spent. It is likely to be the main loop in the program. It can also be a function called from the main loop. You may want to re-implement a simplified version of the main loop in C to make the following steps easier. You may want to use a profiler to find the hotspot.

Third, **implement the main loop in assembly**. Also write C-code to necessary data structures for your function, call your function, and test the results of your function for correctness.

Fourth, **estimate the theoretical time for execution of your microbenchmark**.

Fifth, **present your microbenchmark and experiment methodology** in a mandatory design review.
 
Sixth, **measure the time for your assembly function and C function**.

Finally, **summarize your findings in a written report**.

## Design review
The design review is mandatory. You will meet your TA for a 15-minute discussion. Before the meeting you should prepare an informal presentation where you describe your microbenchmark and input data. In addition, you should present your experiment methodology including how you plan to measure the execution time, and how you will setup the experiment (input data size, number of experiment repeated measurements, main loop iterations, etc).

## Deliverables and report

You should use the pre-code in GitHub as a starting point. We will provide you with a link to the assignment that will create a repository for your group. You will also hand in the report by committing it to your GitHub repository before the deadline. The final repository should contain:
1. Code
  1. In a directory named “src”, containing code, Makefiles, READMEs etc
  2. NO compiled files. Delete executables etc before you hand in.
  3. README must contain how to compile and run the code
2. Written report that enables an expert reader to reproduce your results.
   1. In a directory named “doc”, containing report.pdf
   2. Maximum 6 pages
   3. One report per group
3. A file named “abc001-def002-P1/”
   1. Where abc001 and def002 are your UiT usernames

The report should have the following sections
1. Cover page: your names, emails, GitHub usernames, and your GitHub repository.
1.	Introduction: description of your benchmark. Why did you choose this benchmark? What does it do? Where is it used?
2.	Implementation: describe your assembly (and C) implementation of the microbenchmark. Do not include full code in report, but describe the most relevant or interesting aspects, such as expensive assembly instructions.
3. Methodology, where you describe:
   1. How you measured hotspots
   2. The computer(s) you used for the experiments.
   3. How you measured the execution time for the benchmark, including the resolution of your timer. 
   4.	Experiment parameters such as input data content and size, number of iterations, number of repeated experiment executions, and so on.
4. Results: where you estimate the best theoretical execution time for your benchmark on your computer, and then compare it to the assembly code execution time, and the reference C code execution time.
5. Discussion: where you discuss your results and summarize lessons learned.

The code should:
1. Compile without errors and warnings. 
2. Be structured and clean.
3. Be well commented, such that we understand what your code is doing, and to show that you know what your code is doing.


## Cheating

Som student plikter du å sette deg inn i reglene som gjelder for bruk av hjelpemiddel ved eksamen samt regler for kildebruk og sitering. Ved brudd på disse reglene kan du bli mistenkt for fusk eller forsøk på fusk. Fusk på eksamen og plagiering i skriftlige arbeider innebærer at man bryter med det man kaller akademisk redelighet. Akademisk redelighet dreier seg om å være tydelig i forhold til hvilke tanker og refleksjoner som er ens egne og hvilke som er hentet fra andres arbeider, slik at arbeidet kan etterprøves. Fusk er alvorlig og straffes med annullering av eksamen og/eller utestenging fra universitetet. Bruk tid på å sette deg inn hva som regnes som plagiering eller fusk. Instituttets web-side [Kildebruk, plagiering og fusk på eksamen / obligatoriske oppgaver](https://uit.instructure.com/courses/327/pages/kildebruk-plagiering-og-fusk-pa-eksamen-slash-obligatoriske-oppgaver) er en god start for å lære mer om dette.

### English
As a student at UiT, you are obliged to familiarize yourself with the current rules that apply to the use of aids during exams, as well as rules for source use and citation. In the case of violation of these rules, you may be suspected of cheating, or attempt at cheating. Cheating on an exam is considered a violation of academic integrity. Academic integrity(honesty) is about being clear in relation to which thoughts/reflection and work are one's own, and which are taken from other's work. Cheating is punishable by cancellation of exams and/or exclusion from university.

You can read more about plagiarism and cheating on: https://en.uit.no/sensor/art?p_document_id=684332

