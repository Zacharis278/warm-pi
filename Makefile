.PHONY: all

provision:
	sqlite3 Test.db < create_tables.sql

requirements:
	pip install -r requirements.txt
