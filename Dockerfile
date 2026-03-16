FROM ubuntu
RUN apt update && apt install python3 -y
copy app.py .
CMD ["python3", "app.py"]
