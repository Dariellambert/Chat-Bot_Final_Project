to use in local:
1. clone the repo
2. install library from requirements.txt
3. open app.py with any IDE
4. open the terminal and run: python app.py
5. test connection with curl:
   curl -X POST http://127.0.0.1:5000/chat \
   -H "Content-Type: application/json" \
   -d '{"message": "Who is the founder of Microsoft?"}

6. in project folder open terminal or powershell and run:
   streamlit run streamlit_app.py
