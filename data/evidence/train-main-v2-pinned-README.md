---
license: other
configs:
  - config_name: default
    data_files:
      - split: train
        path: data/train-*.parquet
---

# AIMO Interpretability Challenge train set covering models from the main track

See https://aimo-interp.github.io for details about the competition.

## Features

| feature | type | description |
|---|---|---|
| `model_id` | string | Hugging Face checkpoint. One of five: `Qwen/Qwen3.5-4B`, `Skywork/Skywork-OR1-Math-7B`, `allenai/Olmo-3-7B-Think`, `deepseek-ai/DeepSeek-R1-0528-Qwen3-8B`, `openai/gpt-oss-120b`. |
| `reasoning_effort` | string | Decoding condition: `default` for the four fixed-effort models, `low`, `medium` or `high` for `openai/gpt-oss-120b`. Together with `model_id` it identifies the evaluated configuration. |
| `problem` | string | The original, unperturbed problem statement handed to the model. |
| `is_robust` | bool or null | Robustness label. True when the model's accuracy survives every perturbation type. Null where no label is assigned — see below. |
| `max_drop` | float | Largest accuracy drop across perturbation types, as a fraction. `0.29` means the worst perturbation family cost 29 percentage points against the unperturbed baseline. Negative values may occur (meaning that the perturbation helped). |

## Labels and the unlabelled band

On labelled rows the rule is exact:

- `is_robust = true`  iff `max_drop <= 0.10`
- `is_robust = false` iff `max_drop >= 0.25`

14 rows have `max_drop` strictly between those bounds (0.11 to 0.21). They carry
`is_robust = null`: the measurement is real and is given, but the case is too close to
call and in such cases the labels will also not be assigned in the val/test split. 
Feel free to experiment with different labelling thresholds with your method.

## Contents

94 rows: 59 robust, 21 non-robust, 14 unlabelled, over 36 problems.

| configuration | robust | non-robust | unlabelled |
|---|---:|---:|---:|
| Qwen/Qwen3.5-4B · default | 8 | 4 | 2 |
| Skywork/Skywork-OR1-Math-7B · default | 9 | 3 | 3 |
| allenai/Olmo-3-7B-Think · default | 7 | 2 | 1 |
| deepseek-ai/DeepSeek-R1-0528-Qwen3-8B · default | 7 | 3 | 0 |
| openai/gpt-oss-120b · high | 13 | 2 | 3 |
| openai/gpt-oss-120b · low | 5 | 2 | 1 |
| openai/gpt-oss-120b · medium | 10 | 5 | 4 |

Note the split is 74% robust among labelled rows, whereas the validation set is close to
balanced. Calibrating a decision threshold on this prevalence may not transfer.
