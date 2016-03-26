#Python2.7

import os
import hashlib
import csv
import sys
import argparse


def hash_file(file):
    """Calculates file hashes utilizing md5, sha1, & sha256 algorithms

        :param file: Full path of file to be hashed
        :type file:  str
        :returns:    dictionary containing hash type/value pairs
        :rtype:      dict
    """
    hasherOptions = [hashlib.md5(), hashlib.sha1(), hashlib.sha256()]
    hashResults = {}
    for hash in hasherOptions:
        with open(file, 'rb') as afile:
            buf = afile.read(65536)
            while len(buf) > 0:
                hash.update(buf)
                buf = afile.read(65536)
        hashResults[str(hash).split()[0][1:]] = hash.hexdigest()
    return hashResults


def walk_dir(directory):
    """Recursively walks directory returning a file listing

        :param directory: Full path of file to be hashed
        :type directory:  str
        :returns:    full paths for each file under directory
        :rtype:      list
    """
    count = 0
    walkList = []
    print "Walking directory: " + directory
    for dirName, subdirList, fileList in os.walk(directory):
        for fname in fileList:
            walkList.append(os.path.join(dirName, fname))
            count += 1
    print "    Complete: " + str(count) + " files identified"
    return walkList


def progress_bar(iteration, total, prefix='', suffix='', decimals=2, barLength=100):
    """Displays a progress bar on screen while called in a loop

        :param iterations: Current iteration - Required
        :param total:      Total iterations  - Required
        :param prefix:     Prefix to progress bar
        :param suffix:     Suffix to progress bar
        :type iteration:  int
        :type total:       int
        :type prefix:      str
        :type suffix:      str
        :returns:          n/a
        :rtype:            n/a

        :Example:

        testList=[A,B,C,D]
        i=1
        for i in len(testList):
            print i
            progress_bar(i, len(testList), prefix='Print Progress', suffix='Complete', decimals=2, barLength=100)
            i += 1

    """

    filledLength = int(round(barLength * iteration / float(total)))
    percents = round(100.00 * (iteration / float(total)), decimals)
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s [%s] %s%s %s' % (prefix, bar, percents, '%', suffix)),
    sys.stdout.flush()
    if iteration == total:
        print("\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Directory crawler & hahser')
    parser.add_argument('-i', dest='input', help='Directory to be crawled and hashed')
    parser.add_argument('-o', dest='output', help='Output file (CSV)')
    args = parser.parse_args()


    outFile = open(args.output, 'wb')
    outCSV = csv.writer(outFile)
    outCSV.writerow(['File', 'MD5', 'SHA1', 'SHA256'])

    hashingResults = {}
    fileListing = walk_dir(os.path.normpath(args.input))

    print 'Hashing Files'
    listLength = len(fileListing)
    i = 1

    for entry in fileListing:
        progress_bar(i, listLength, prefix = '    Hashing', suffix = 'Complete')
        hashingResults[entry] = hash_file(entry)
        outCSV.writerow(
            [entry, hashingResults[entry]['md5'], hashingResults[entry]['sha1'], hashingResults[entry]['sha256']])
        i += 1
    raw_input('Complete, press any key to exit')

