---
dataset_info:
  features:
  - name: model_id
    dtype: large_string
  - name: dataset_id
    dtype: large_string
  - name: problem_id
    dtype: large_string
  - name: original_problem
    dtype: large_string
  - name: permutation_type
    dtype: large_string
  - name: permutation_source
    dtype: large_string
  - name: base_accuracy
    dtype: float64
  - name: permuted_accuracy
    dtype: float64
  - name: absolute_accuracy_decay
    dtype: float64
  - name: relative_accuracy_decay
    dtype: float64
  - name: n_base_predictions
    dtype: int64
  - name: n_permuted_predictions
    dtype: int64
  - name: n_detrimental_permutations
    dtype: int64
  - name: permutations_causing_decay
    dtype: large_string
  splits:
  - name: validation
    num_bytes: 722559
    num_examples: 558
  download_size: 94757
  dataset_size: 722559
configs:
- config_name: default
  data_files:
  - split: validation
    path: data/validation-*
---
