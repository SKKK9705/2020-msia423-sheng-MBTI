.PHONY: load_data preprocess_data generate_feature create_db_r create_db_l

load_data:
		python3 run.py load_data

preprocess_data:
		python3 run.py preprocess_data

generate_feature:
		python3 run.py generate_feature

#create local database with rds = False or rds table with rds = True
create_db_r:
		python3 run.py create_db --RDS True

create_db_l:
		python3 run.py create_db --RDS False
