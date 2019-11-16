#!/usr/bin/python3
import os
import sys
import time
import argparse
import operator
import subprocess

try:
    import thread
except:
    import _thread as thread

from dependencies import logger
from dependencies import threading_control
from dependencies import validation



class dns_warmer:
    def __init__(self, args):
        self.ts_start = time.time()

        self.input = args["input"]
        self.threads = args["threads"]
        self.max_runtime = args["max_runtime"]
        self.max_to_process = args["max_to_process"]


        logger.dump("*** dns_warmer ***", "info")
        logger.dump("input = %s" %(self.input), "debug")
        logger.dump("threads = %d" %(self.threads), "debug")
        logger.dump("max_runtime = %d" %(self.max_runtime), "debug")
        logger.dump("max_to_process = %d" %(self.max_to_process), "debug")
        

        self.ref_tc = threading_control.threading_control(3600 * 24 * 7, max_threads=self.threads)
        self.ref_validation = validation.validation()
        thread.start_new_thread(self.watchdog, ())


    #
    # Watchdog
    #
    def watchdog(self):
        while 1:
            diff = time.time() - self.ts_start
            if diff >= self.max_runtime:
                logger.dump("max worktime %d exceeded by %d, shutting down..." %(self.max_runtime, diff), "warning")
                os._exit(0)
            time.sleep(1)

    #
    # Main run flow
    #
    def run(self):
        freqs = self.parse_log(self.input)
        
        it = 0
        total = len(freqs)
        for freq in freqs:
            if self.ref_tc.can_work() == False:
                logger.dump("Work finished... Exiting.", "critical")
                return True
            
            self.ref_tc.wait_threads()
            
            self.ref_tc.inc_threads()
            hostname = freq[0]
            thread.start_new_thread(self.warm, (hostname,))
            it += 1

            if it % 10 == 0:
                logger.dump("[ %d / %d ] %s" %(it, total, hostname), "debug")


    #
    # Warm UP DNS
    # 
    def warm(self, hostname):
        cmd = [ 
            'timeout',
            '10',
            'host',
            hostname,
        ]

        try:
            p2 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
            stdout, stderr = p2.communicate()
            p2.stdout.close()
            p2.stderr.close()


            logger.dump("Queried %s, got result %s" %(hostname, stdout), "info")
            # print("stdout: %s" %(stdout))
            # print("stderr: %s" %(stderr))

        except:
            logger.dump("Error in quering %s: %s" %(hostname, sys.exc_info()), "critical")

        self.ref_tc.dec_threads()


    #
    # Parse log and extract frequencies
    #
    def parse_log(self, file_loc) -> list:
        out = {}
        
        if os.path.isfile(file_loc) == False:
            logger.dump("file %s does not exist!" %(file_loc), "critical")
            os._exit(1)


        skip_words = [
            "NXDOMAIN",
            "cached",
        ]

        it = 0
        with open(file_loc, "r") as infile:
            for line in infile:
                it += 1

                if it >= 1000000:
                    break
                
                line = line.lower()
                line = line.replace("\r", "")
                line = line.replace("\n", "")
                line = line.replace("\t", "")
                line = line.strip(" ")
                line = line.split("]:")
                if len(line) > 1:
                    line = line[1]
                line = line.strip(" ")


                is_valid = True
                for skip_word in skip_words:
                    if line.find(skip_word) != -1:
                        is_valid = False
                if is_valid == False:
                    continue


                line = line.split(" ")
                if len(line) > 1:
                    line = line[1]
                line = line.strip(" ")

                if line == "":
                    continue


                if self.ref_validation.is_ip(line) == True:
                    logger.dump("%s is IP! skipping" %(line), "warning")
                    continue

                try:
                    out[line] += 1
                except:
                    out[line] = 1

        out_sorted = sorted(out.items(), key=operator.itemgetter(1), reverse=True)
        
        # cut to maximum number to process
        try:
            out_sorted = out_sorted[0:self.max_to_process]
        except:
            pass

        return out_sorted

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="/var/log/pihole.log", required=False, help="location of log")
    parser.add_argument('--threads', type=int, default=3)
    parser.add_argument('--max_runtime', type=int, default=300)
    parser.add_argument('--max_to_process', type=int, default=200)


    args = vars(parser.parse_args())

    d = dns_warmer(args)
    d.run()

