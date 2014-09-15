#!/usr/bin/env python

from nd import User, Privilege, current_session
import sys
import argparse


def main():
    arg_parser = argparse.ArgumentParser(description="Send mail to members")

    arg_parser.add_argument('-f', '--file', required=True, dest='mail_file')
    arg_parser.add_argument('-s', '--subject', required=True, dest='subject')
    args = arg_parser.parse_args()

    if User.myself() not in Privilege("memberinfo").member:
        print "you're not in the memberinfo group, \
            so this script isn't going to work"
        sys.exit(1)

    # for each current member
    for u in User.search(tcdnetsoc_membership_year=current_session()):
        u.sendmail(args.mail_file,
                   From='Netsoc PRO <pro@netsoc.tcd.ie>',
                   Subject="[Netsoc] %s" % args.subject)

if __name__ == "__main__":
    main()
