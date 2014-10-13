#!/usr/bin/env python

from nd.nd import User, Privilege, current_session
from nd.sendmail import sendmail
import sys
import argparse
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

default_template_location =\
    os.path.abspath(os.path.dirname(__file__)) + "/messages"


def main():
    arg_parser = argparse.ArgumentParser(description="Send mail to members")

    arg_parser.add_argument('-t', '--text_file', required=True,
                            dest='text_file')
    arg_parser.add_argument('-s', '--subject', required=True, dest='subject')
    arg_parser.add_argument('-H', '--html_file', dest='html_file')
    arg_parser.add_argument("-u", '--single_user', dest='user')

    args = arg_parser.parse_args()
    if args.text_file[0] != "/":
        try:
            txtmsg = open(default_template_location +
                          "/" + args.text_file, "r").read()
        except Exception:
            txtmsg = open(args.text_file, "r").read()
    else:
        txtmsg = open(file, "r").read()
    if args.html_file:

        if args.html_file[0] != "/":
            try:
                htmlmsg = open(default_template_location +
                               "/" + args.html_file, "r").read()
            except Exception:
                htmlmsg = open(args.html_file, "r").read()
        else:
            htmlmsg = open(file, "r").read()

    if User.myself() not in Privilege("memberinfo").member:
        print "You're not in the memberinfo group, "\
            "so you don't have permission to send mail to members"
        sys.exit(1)
    msg = MIMEMultipart('alternative')
    msg.attach(MIMEText(txtmsg, 'plain'))
    if htmlmsg is not None:
        msg.attach(MIMEText(htmlmsg, 'html'))
    # for each current member
    if args.user is None:
        for u in User.search(tcdnetsoc_membership_year=current_session()):
            print "sending to %s" % u
#            u.sendmail(msg,
#                       From='Netsoc PRO <pro@netsoc.tcd.ie>',
#                       Subject="[Netsoc] %s" % args.subject)
    else:
        sendmail(msg,
                 From='Netsoc PRO <pro@netsoc.tcd.ie>',
                 To=args.user,
                 Subject="[Netsoc] %s" % args.subject)

if __name__ == "__main__":
    main()
