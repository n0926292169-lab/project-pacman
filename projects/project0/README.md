# Project 0

## Deliverables

You are requested to deliver
- A `bfs.py` file containing your implementation of the BFS algorithm, based on the `pacmanagent.py` template.
- A `astar.py` file containing your implementation of A\* algorithm, based on the `pacmanagent.py` template.

## Instructions

You can download the [archive](../project0.zip?raw=true) of the project into a directory of your choice. In this first part of the project, only food dots, capsules and Pacman are in the maze. Your task is to design an intelligent agent based on search algorithms (see [Lecture 2]) for **maximizing** the score. You are asked to implement the **breadth-first search (BFS)** and **A\*** algorithms. We recommend to implement them in this order. It is mandatory to use only the [API](..#api) to retrieve game information.

To help you, we provide an implementation of the DFS algorithm in the `dfs.py` file. However, the `key` function is not finished. Once you have activated your Pacman environment (see [installation](..#installation)), you can test the DFS algorithm using the following commands:
```console
$ python run.py --agentfile dfs.py  --layout medium
```
If you want to test one of your implementation, just replace the script parameter `dfs` by the name (without the extension) of the agent file you want to test. Refer to the [usage section](..#usage) for more details about the options.

## Evaluation

Each of your agents will be evaluated against new mazes, some being designed to test common pitfalls. Passing the public tests does not mean that your code is correct. Do your own tests. Follows the criteria for this project:

- **BFS** (20%): If implemented correctly, your implementation should return the same score as ours and expand roughly the same amount of nodes.
- **A\*** (75%): A well-implemented A\* algorithm should return the optimal solution no matter the maze structure. The number of expanded nodes needed to find an optimal solution depends on the quality of the heuristic. For this algorithm, we check whether the returned solution is optimal for all mazes. The number of expanded nodes is also taken into account (the lower the better) in the grade.
- **Code style** (5%): No points are awarded if your code is not PEP-8 compliant.

## สิ่งที่ต้องส่ง (Deliverables)

คุณจะต้องส่งไฟล์ต่อไปนี้:
- ไฟล์ `bfs.py` ที่มีการติดตั้งอัลกอริทึม BFS ตามแม่แบบ `pacmanagent.py`
- ไฟล์ `astar.py` ที่มีการติดตั้งอัลกอริทึม A* ตามแม่แบบ `pacmanagent.py`

## คำแนะนำ (Instructions)

คุณสามารถดาวน์โหลด [ไฟล์โครงการ](../project0.zip?raw=true) ไปยังโฟลเดอร์ที่คุณต้องการ ในส่วนแรกของโครงการนี้ ภายในเขาวงกต (maze) จะมีเพียงจุดอาหาร (food dots), แคปซูล (capsules) และ Pacman เท่านั้น  
**ภารกิจของคุณ** คือ การออกแบบตัวแทนอัจฉริยะ (intelligent agent) โดยใช้อัลกอริทึมค้นหา (search algorithms) (ดู [Lecture 2])  
โดยมีเป้าหมายเพื่อ **เพิ่มคะแนน (score) ให้ได้มากที่สุด**

คุณจะต้องติดตั้งอัลกอริทึม:
- **Breadth-First Search (BFS)**
- **A\* Search**

เราแนะนำให้คุณเริ่มจาก BFS ก่อนแล้วจึงไปทำ A\*

**ข้อกำหนดสำคัญ**  
คุณจะต้องใช้งานเฉพาะ [API](..#api) เท่านั้นในการดึงข้อมูลสถานะของเกม  

เพื่อช่วยคุณเริ่มต้น เราได้เตรียมตัวอย่างการติดตั้งอัลกอริทึม DFS ไว้ในไฟล์ `dfs.py` แล้ว  
อย่างไรก็ตาม ฟังก์ชัน `key` ในไฟล์นี้ยังไม่เสร็จสมบูรณ์  

เมื่อคุณได้เปิดใช้งานสภาพแวดล้อม Pacman เรียบร้อยแล้ว (ดู [installation](..#installation))  
คุณสามารถทดสอบอัลกอริทึม DFS ได้ด้วยคำสั่งต่อไปนี้:

```console
$ python run.py --agentfile dfs.py --layout medium

**การประเมินผล (Evaluation)**

ตัวแทนของคุณแต่ละตัวจะถูกประเมินบนเขาวงกตใหม่ๆ ซึ่งบางแบบถูกออกแบบมาเพื่อทดสอบข้อผิดพลาดที่พบบ่อย
หมายเหตุ: ผ่านการทดสอบสาธารณะ (public tests) ไม่ได้แปลว่าโค้ดของคุณถูกต้องสมบูรณ์
คุณควรเขียนการทดสอบของคุณเองเพิ่มเติม

เกณฑ์การให้คะแนนมีดังนี้:
	•	BFS (20%)
ถ้าติดตั้งถูกต้อง ผลลัพธ์ควรได้คะแนนเท่ากับของเรา และขยายจำนวน node ใกล้เคียงกับของเรา
	•	A* (75%)
อัลกอริทึม A* ที่ติดตั้งดีควรสามารถหาผลลัพธ์ที่ดีที่สุด (optimal solution) ได้ในทุกเขาวงกต
จำนวน node ที่ถูกขยายขึ้นอยู่กับคุณภาพของ heuristic
สำหรับอัลกอริทึมนี้ เราจะตรวจสอบว่าเส้นทางที่ได้ เป็นเส้นทางที่ดีที่สุด สำหรับเขาวงกตทุกแบบหรือไม่
และจำนวน node ที่ขยายจะถูกนำมาพิจารณาด้วย (ยิ่งน้อยยิ่งดี)
	•	รูปแบบการเขียนโค้ด (Code style) (5%)
จะไม่ได้คะแนนถ้าโค้ดของคุณไม่เป็นไปตามมาตรฐาน PEP-8