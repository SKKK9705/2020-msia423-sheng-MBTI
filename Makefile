# default/environment variables
posts = "new post!"

.PHONY: load_data preprocess_data generate_feature train_model evaluate_model create_db_r create_db_l ingest_r ingest_l all_pipeline test

#ml pipeline
load_data:
		python3 run.py load_data

preprocess_data:
		python3 run.py preprocess_data

generate_feature:
		python3 run.py generate_feature

train_model:
		python3 run.py train_model

evaluate_model:
		python3 run.py evaluate_model

test:
		py.test


#create local database with rds = False or rds table with rds = True
create_db_r:
		python3 run.py create_db --RDS True

create_db_l:
		python3 run.py create_db --RDS False

ingest_r:
		python3 run.py ingest --posts="${posts}" --RDS True

ingest_l:
		python3 run.py ingest --posts="${posts}" --RDS False

test:
		py.test

all_pipeline: load_data preprocess_data generate_feature train_model evaluate_model
