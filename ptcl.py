from router import Router
import argparse
import sys
import configobj


# ptcl = Router(password='ptcl')
my_macs = {"mytab": "5c:2e:59:4d:33:67",
"ahmer": "68:94:23:AC:59:51",
"asad": "A0:32:99:AB:33:31",
"hhp": "44-1C-A8-73-A3-17",
"haris": "64:5A:04:76:C7:9C"
}
ptcl = Router(mask='192.168.10.1', password='123motorcross')
# Defining custom aliases
# config['User-Aliases'] = {
# "mytab": "5c:2e:59:4d:33:67",
# "ahmer": "68:94:23:AC:59:51",
# "asad": "A0:32:99:AB:33:31",
# "hhp": "44-1C-A8-73-A3-17"
# }

def main():
    parser = argparse.ArgumentParser(description="Control PTCL router from command-line.")
    parser.add_argument('-b', '--block', help="Block device.", nargs='?')
    parser.add_argument('-sb', '--blocked_dev', help='Display blocked devices.', action='store_true')
    parser.add_argument('-ub', '--unblock', help="Unblock device.", nargs='?')
    parser.add_argument('-a', '--active-devices', help="Gets number of devices connected to the router.", action='store_true')
    parser.add_argument('-r', '--restart', help="Restart Router.", action='store_true')
    parser.add_argument('-sd', '--show-dhcp', help='Show DHCP Info.', action='store_true')
    parser.add_argument('-s', '--show-active', help='Show Active Devices.', default='.')
    parser.add_argument('--configure', help='Configure router settings.', action='store_true')
    parser.add_argument('-sa', '--set-alias', help='Set custom alias for a device hostname.', action='store_true')
    parser.add_argument('-c', '--cli', help='Silent mode.', nargs='?', default='False')
    args = parser.parse_args()
    # print args

    if args.cli == 'False':
        if args.block:
            # print "Calling blocker Function"
            ptcl.get_sessionkey()
            if args.block in my_macs.iterkeys():
                # print "Calling blocker function - AUTOMATED MODE."
                ptcl.block_dev(my_macs[args.block.lower()])
                print "%s has been blocked." % args.block.capitalize()
                if args.block not in my_macs.iterkeys():
                    print "User not found."
            elif args.block not in my_macs.iterkeys():
                print "User not found."

        elif args.unblock:
            ptcl.get_sessionkey()
            if args.unblock in my_macs.iterkeys():
                # print "Calling unblocker function - AUTOMATED MODE"
                ptcl.unblock_dev(my_macs[args.unblock.lower()])
                print "%s has been unblocked." % args.unblock.capitalize()
            elif args.unblock not in my_macs.iterkeys():
                print "User not found."

        elif args.active_devices:
            # print "Calling Station info Function"
            ptcl.get_stationinfo()
            print "Currently active devices are:", len(ptcl.active_dev)

        elif args.restart:
            # print "Calling restart Function"
            ptcl.get_sessionkey()
            ptcl.reboot_router()

        elif args.show_dhcp:
            # print "Calling DHCP_info Function"
            # ptcl.get_sessionkey()
            ptcl.show_dhcpinfo()

        elif args.blocked_dev:
            ptcl.show_blocked_dev()

        elif args.configure:
            # Creating a config file
            config = configobj.ConfigObj()
            config['User-Aliases'] = {}
            DEFAULT = {'mask': '192.168.1.1', 'username': 'admin', 'password': 'admin'}
            mask = raw_input("Leave empty for default configuration.\nPlease enter router gateway\t(Default 192.168.1.1)\t: ")
            if mask:
                DEFAULT['mask'] = mask
            username = raw_input("Please enter router username\t(Default admin)\t: ")
            if username:
                DEFAULT['username'] = username
            password = raw_input("Please enter router password\t(Default admin)\t: ")
            if password:
                DEFAULT['password'] = password
            config['Router-Auth'] = DEFAULT
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            print '\nConfiguration file Generated.'

        elif args.set_alias:
            pass

        elif args.show_active == '.':
            # print "Calling show_active Function"
            ptcl.show_active_dev()

        else:
            print "Invalid Argument"


    elif not args.cli:
        ptcl.get_sessionkey()
        if not args.block:
            # print "Calling blocker function - CLI MODE."
            name = ptcl.show_active_dev()
            ptcl.host_and_mac = dict(ptcl.host_and_mac)
            dev_mac = int(raw_input("Please Enter Device Number: ")) - 1
            ptcl.block_dev(ptcl.host_and_mac[name[dev_mac]])
            print "%s has been blocked." % name[dev_mac].capitalize()


        elif not args.unblock:
            # print "Calling unblocker function - CLI MODE."
            name = ptcl.show_active_dev()
            ptcl.host_and_mac = dict(ptcl.host_and_mac)
            dev_mac = int(raw_input("Please Enter Device Number: ")) - 1
            ptcl.unblock_dev(ptcl.host_and_mac[name[dev_mac]])
            print "%s has been unblocked." % name[dev_mac].capitalize()


main()
