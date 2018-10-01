FROM ubuntu:latest
RUN apt update -y
RUN apt install -y ircd-irc2

EXPOSE 6667

CMD ["/usr/sbin/ircd", "-t"]
