start:
	uv run uvicorn app.main:app --reload &
	uv run streamlit run streamlit_app.py &
	wait

stop:
	pkill -f "uvicorn app.main:app"
	pkill -f "streamlit run streamlit_app.py"
