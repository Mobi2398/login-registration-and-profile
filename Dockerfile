FROM python:3.10.8-buster
RUN apt-get update &&\
    /usr/local/bin/python3 -m pip install --upgrade pip &&\
    /usr/local/bin/python3 -m pip install --upgrade setuptools &&\
    adduser myuser
ENV PATH="/home/myuser/.local/bin:${PATH}"
ENV FLASK_APP=wsgi.py
ENV FLASK_RUN_PORT=8080
ENV PORT=8080
ENV QR_CODE_IMAGE_DIRECTORY='static'
ENV QR_CODE_DEFAULT_URL='https://www.njit.edu'
ENV QR_CODE_DEFAULT_FILE_NAME='default.png'
WORKDIR /home/myuser
RUN pip3 install -r requirements.txt
COPY --chown=myuser:myuser . .
CMD ["./production.sh"]

# CMD ["runuser", "-u", "myuser", "--", "python", "-m", "flask", "run", "--host=0.0.0.0"]