import re
import sys

stdin = sys.stdin.read()
print(stdin, file=sys.stderr)
filenames = re.findall(r'copying (build/lib\..*?/_libhfst\..*?\.so)', stdin)
for filename in filenames:
    print(filename)
