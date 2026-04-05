Simple AI Studio (RapidMiner 12.x) scripts for the Bank Customer Segmentation demo.

Files:
- `custseg_kmeans_simple.rmp` — Simple K-Means segmentation demo. Use macro `data_file` to point to `bank_customer_data.csv` and `n_clusters` to set number of clusters. Outputs `custseg_kmeans_results.csv` with cluster labels.

- `custseg_rfm_simple.rmp` — Simple RFM demo. Creates Recency/Frequency/Monetary attributes, discretizes to 5 bins each and writes `custseg_rfm_results.csv` with `rfm_code` for quick segment grouping.

Instructor notes (MBA audience):
- These processes are deliberately simple and visual. Open in RapidMiner Studio (File → Import Process) and run.
- If Studio shows port warnings after import, connect the ports manually per operator comments and run again.
- Use the generated CSVs for classroom exercises (sorting, pivot tables, or quick visualization in Excel).

Validation:
- These templates are validated with the repository tool: `uv run python Utils/rmp_validator.py <path-to-template.rmp>`.

If you want, I can create step-by-step slides or a short Jupyter notebook explaining the output tables and suggested classroom exercises.