# โปรเจกต์ 1

## สิ่งที่ต้องส่งมอบ

โปรดส่ง
- ไฟล์ `minimax.py` ที่เป็นการนำอัลกอริทึม Minimax ไปใช้ โดยอ้างอิงจากเทมเพลต `pacmanagent.py`
- ไฟล์ `hminimax.py` ที่เป็นการนำอัลกอริทึม H-Minimax ไปใช้ โดยอ้างอิงจากเทมเพลต `pacmanagent.py`

## คำแนะนำ

ใน [โปรเจกต์ 0](../project0) แพคแมนสามารถเดินเล่นในเขาวงกตได้อย่างสงบ ตอนนี้เขาจำเป็นต้องหลีกเลี่ยง “ผีที่เดินได้” ซึ่งจะฆ่าเขาหากมันไปถึงตำแหน่งของเขา แพคแมน **ไม่รู้กลยุทธ์ของผี** แต่สามารถเข้าถึงชุด “การกระทำที่อนุญาต” ของผีผ่าน API ได้ โดยเฉพาะอย่างยิ่ง ผีสามารถเดินหน้า เลี้ยวซ้าย หรือเลี้ยวขวา แต่ **ไม่สามารถกลับหลังหัน 180 องศา (half-turn)** ได้ เว้นแต่จะไม่มีทางเลือกอื่น

งานของคุณคือออกแบบเอเจนต์อัจฉริยะโดยใช้อัลกอริทึมการค้นหาแบบปะทะ/แข่งขัน (adversarial search) (ดู [Lecture 3](https://github.com/aofphy/SCI193611_ARTIFICIAL_INTELLIGENCE/blob/main/slide/lecture3_th.pdf)) เพื่อ **ทำคะแนนของแพคแมนให้มากที่สุด** โดยให้คุณนำอัลกอริทึม **Minimax** และ **H-Minimax** ไปใช้ โดยถือว่าแพคแมนและผีเป็นผู้เล่นสองฝ่าย แนะนำให้พัฒนาอัลกอริทึมตามลำดับนี้ **กำหนดให้ใช้เฉพาะ [API](..#api)** ในการดึงข้อมูลของเกม เลย์เอาต์ที่มีแคปซูลจะไม่ถูกนำมาพิจารณา แต่หากต้องการ คุณอาจคำนึงถึงไว้ได้ การนำ Minimax ไปใช้ของคุณ **ไม่จำเป็นต้องรันได้** บนเลย์เอาต์ `medium_adv` และ `large_adv`

เริ่มต้นโดยดาวน์โหลดและแตกไฟล์ [archive](../project1.zip?raw=true) ของโปรเจกต์ไปไว้ในไดเรกทอรีที่คุณเลือก ใช้คำสั่งด้านล่างเพื่อรัน Minimax ของคุณแข่งกับผี `dumby` ในเลย์เอาต์ขนาดเล็ก:
```console
$ python run.py --agent minimax --ghost dumby --layout small_adv
```

มีกลยุทธ์ของผีให้เลือกหลายแบบ:
- `dumby` จะหมุนตัวทวนเข็มนาฬิกาอยู่กับที่จนกว่าจะสามารถไปทางซ้ายได้
- `greedy` เลือกการกระทำที่พาไปยังช่องที่อยู่ใกล้แพคแมนที่สุด หากมีหลายทางเลือกที่เทียบเท่ากัน `greedy` จะสุ่มเลือกจากตัวเลือกเหล่านั้น
- `smarty` เลือกการกระทำที่นำไปสู่เส้นทางที่สั้นที่สุดมุ่งหน้าไปหาแพคแมน

คุณสามารถเปลี่ยนค่า seed แบบสุ่มของเกมได้ด้วยออปชัน `--seed` (เช่น `--seed 42`)

## การประเมินผล

โปรเจกต์ของคุณจะถูกประเมินบนทั้งเลย์เอาต์สาธารณะและเลย์เอาต์ส่วนตัว เมื่อส่งโปรเจกต์ คุณจะเห็นผลการทดสอบสาธารณะ ซึ่งทำบนเลย์เอาต์สาธารณะเท่านั้นและจะแจ้งเตือนหากพบปัญหาใหญ่ เช่น โค้ดล่ม หรือมีปัญหาร้ายแรงกับอัลกอริทึมของคุณ คะแนนสุดท้ายของคุณจะคำนวณจากการทดสอบส่วนตัว ซึ่งคุณจะมองไม่เห็นเมื่อส่งงาน การทดสอบเหล่านี้ทำบนเลย์เอาต์ส่วนตัวที่แตกต่างจากเลย์เอาต์สาธารณะ เลย์เอาต์สาธารณะจะมีความพื้นฐานเพื่อทดสอบประสิทธิภาพโดยรวมของอัลกอริทึม ในขณะที่เลย์เอาต์ส่วนตัวถูกออกแบบมาให้เอเจนต์ของคุณ “พัง” หากมีข้อผิดพลาดในการนำไปใช้ ดังนั้น **เราสนับสนุนให้คุณสร้างการทดสอบของคุณเอง** เพื่อครอบคลุมกรณีขอบ (edge cases) ที่อาจพบในช่วงการทดสอบส่วนตัว คะแนนที่จัดสรรให้แต่ละส่วนมีดังนี้:

- **Minimax** (45%): ประเมิน “ความเป็นเหมาะที่สุด” ของการนำไปใช้ของคุณบนทั้งเลย์เอาต์สาธารณะและส่วนตัว เลย์เอาต์หนึ่งจะถือว่าผ่าน หากเอเจนต์ของคุณทำคะแนนได้ดีที่สุดเท่าที่เป็นไปได้บนเลย์เอาต์นั้น คะแนนส่วนนี้จะเท่ากับสัดส่วนของเลย์เอาต์ที่ผ่าน
- **H-Minimax** (50%): ประเมินสมรรถนะของการนำไปใช้บนทั้งเลย์เอาต์สาธารณะและส่วนตัว โดยคำนึงถึงทั้ง “คะแนน” และ “จำนวนโหนดที่ถูกขยาย” สำหรับแต่ละเลย์เอาต์ จะกำหนด “เกณฑ์บน” และ “เกณฑ์ล่าง” ทั้งสำหรับคะแนนและจำนวนโหนดที่ขยาย แยกตามผีแต่ละแบบ หากคะแนนต่ำกว่าเกณฑ์ล่าง หรือจำนวนโหนดที่ขยายสูงกว่าเกณฑ์บนสำหรับผีใด ๆ เลย์เอาต์นั้นจะถือว่าล้มเหลวและถูกหักคะแนนสูงสุด ซึ่งหมายความว่า เอเจนต์ของคุณควรทำคะแนนได้ “สมเหตุสมผล” พร้อมทั้งขยายโหนดในจำนวนที่ “สมเหตุสมผล” สำหรับผีทุกแบบ หากผ่านเงื่อนไขดังกล่าวแล้ว คะแนนของคุณสำหรับเลย์เอาต์นั้นจะพิจารณาจากระยะห่างระหว่างคะแนนของคุณกับ “เกณฑ์คะแนนสูง” และระยะห่างระหว่างจำนวนโหนดที่ขยายของคุณกับ “เกณฑ์โหนดต่ำ” สำหรับผีแต่ละแบบ หากเอเจนต์ของคุณทำคะแนนสูงกว่าเกณฑ์คะแนนสูง **และ** ขยายโหนดน้อยกว่าเกณฑ์โหนดต่ำสำหรับผีทุกแบบ คุณจะได้คะแนนเต็มสำหรับเลย์เอาต์นั้น ในการทดสอบสาธารณะ เราจะแจ้งเตือนเฉพาะกรณีที่โค้ดล้มเหลว เอเจนต์ทำคะแนนต่ำกว่าที่คาดมาก หรือขยายโหนดมากเกินไป
- **สไตล์โค้ด** (5%): จะได้คะแนนเต็มหากโค้ดเป็นไปตามมาตรฐาน PEP-8 มิฉะนั้นจะไม่ได้คะแนน การทดสอบนี้เป็นแบบสาธารณะ
----------------------------------------------
# Project 1

## Deliverables

You are requested to deliver
- A `minimax.py` file containing your implementation of the Minimax algorithm, based on the `pacmanagent.py` template.
- A `hminimax.py` file containing your implementation of H-Minimax algorithm, based on the `pacmanagent.py` template.

## Instructions

In [Project 0](../project0), Pacman could wander peacefully in the maze. Now, he needs to avoid a walking ghost that would kill him if it reached his position. Pacman **does not know what is the strategy of the ghost**, but he has access to the ghost's legal actions through the API. In particular, a ghost can go forward, turn left or right, but cannot make a half-turn unless it has no other choice.

Your task is to design an intelligent agent based on adversarial search algorithms (see [Lecture 3](https://github.com/aofphy/SCI193611_ARTIFICIAL_INTELLIGENCE/blob/main/slide/lecture3_th.pdf)) for **maximizing** the score of Pacman. You are asked to implement the **Minimax** and **H-Minimax** algorithms where Pacman and the ghost are the two players. We recommend to implement the algorithms in this order. It is mandatory to use only the [API](..#api) to retrieve game information. Layouts with capsules will not be considered, but you may take them into account if you feel motivated. Your implementation of Minimax does not need to run on the `medium_adv` and `large_adv` layouts.

To get started, download and extract the [archive](../project1.zip?raw=true) of the project in the directory of your choice. Use the following command to run your Minimax implementation against the `dumby` ghost in the small layout:
```console
$ python run.py --agent minimax --ghost dumby --layout small_adv
```

Several strategies are available for the ghost:
- `dumby` rotates on itself counterclockwise until it can go to its left.
- `greedy` selects the action leading to the cell closest to Pacman. If several actions are equivalent, `greedy` chooses randomly among them.
- `smarty` selects the action leading to the shortest path towards Pacman.

The random seed of the game can be changed with the `--seed` option (e.g. `--seed 42`).

## Evaluation

Your project will be evaluated on both public and private layouts. When submitting your project, you will see the results of public tests. Those are made on public layouts only and warn you if big issues are encountered, such as code crashing or severe issues with your algorithm. Your final grade will be computed based on private tests that are invisible to you when submitting your project. Those tests are made on private layouts that differ from public layouts. Public layouts are very basic layouts that are designed to test your algorithm's general performance, while private layouts are designed to make your agent fail if some implementation errors have been made. Therefore, **we encourage you to make your own tests** to test for edge cases that you might encounter during the private testing phase. The points allocated to each part of the project are the following:

- **Minimax** (45%): We evaluate the optimality of your implementation on both public and private layouts. A layout is considered successful if your agent obtains the best possible score on it. Your grade is the proportion of successful layouts.
- **H-Minimax** (50%): We evaluate the performance of your implementation on both public and private layouts. Both the score and the number of expanded nodes are taken into account. For each layout, an upper and lower threshold are set for both the score and the number of expanded nodes for each ghost. If the score is lower than the low threshold or the number of expanded nodes is higher than the high threshold for any ghost, the layout is considered as failed, and the maximum point penalty is applied. This means that your agent should at least obtain a reasonable score with a reasonable number of nodes expanded for all ghosts. If that condition is met, then your grade for that layout is based on the distance between your score and the high score threshold as well as the distance between the amount of expanded nodes of your agent and the low nodes threshold for each ghost. If your agent gets a higher score than the high threshold while expanding a lower amount of nodes than the low nodes threshold for all ghosts, then you obtain the maximal grade for that layout. In the public tests, we only warn you if your code fails, your agent has a score that is way lower than expected, or if your agent expands way too many nodes.
- **Code style** (5%): You are awarded the maximal grade if your code is PEP-8 compliant and no points otherwise. This test is public.
