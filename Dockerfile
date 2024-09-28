FROM python:3.12-bookworm

RUN export DEBIAN_FRONTEND=noninteractive && apt-get update && apt-get -y install git curl wget vim tmux
RUN wget https://www.arnaudmorin.fr/tmux.conf -O /root/.tmux.conf
RUN pip3 install poetry

#RUN git clone https://github.com/arnaudmorin/notification-queue.git /opt/notification-queue
COPY . /opt/notification-queue/
RUN cd /opt/notification-queue/ && poetry install

EXPOSE 8082

CMD ["/opt/notification-queue/start.sh"]
