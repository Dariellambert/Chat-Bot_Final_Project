for live demo production visit this link:
https://chat-botfinalproject-m5wyzjtnbpitqoqsupjwsz.streamlit.app/

to use in local:
1. clone the repo
2. install library from requirements.txt
3. replace app.py and streamlit_app.py in local folder to main folder
4. open app.py with any IDE
5. open the terminal in IDE and run: python app.py
6. test connection with curl:
   curl -X POST http://127.0.0.1:5000/chat \
   -H "Content-Type: application/json" \
   -d '{"message": "Who is the founder of Microsoft?"}
7. in project folder open terminal or powershell and run:
   streamlit run streamlit_app.py
