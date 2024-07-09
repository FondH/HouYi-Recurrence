~~~bash
├─HouYi
│  │  ablatate.py	--------------------- 消融实验
│  │  context_infer.py
│  │  demo.py		--------------------- HouYi 推理框架具体实现
│  │  iterative_prompt_optimization.py
│  │  requirements.txt
│  │  test.py	-------------------------- 验证实验
│  │  test_answer_analyze.py
│  ├─example_apps
│  │  │  english_trainer.py
│  │  │  finance_assistant.py
│  │  │  travel_planner.py
│  │  │  write_sonic.py
│  │
│  ├─harness
│  │  │  analyze_harness.py
│  │  │  answer_harness.py
│  │  │  base_harness.py
│  │  │  demo_translator_harness.py
│  │
│  ├─intention
│  │  │  base_intention.py
│  │  │  content_manipulation.py
│  │  │  information_gathering.py
│  │  │  prompt_leakage.py
│  │  │  spam_generation.py
│  │  │  write_code.py
│  │
│  ├─strategy
│  │  │  disruptor_generation.py
│  │  │  framework_generation.py
│  │  │  separator_generation.py
│  │  │  __init__.py
│  │
│  ├─util
│  │  │  fitness_ranking.py
│  │  │  mutation.py
│  │  │	 ...
├─logs -------------------- 日志
│  └─Ablation
│
└─result
    ├─Ablation ----------- 消融实验结果
    ├─Alblation-7
    └─answer_analyze
   	....  ---------------- 验证实验结果

~~~

