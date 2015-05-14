import vim
import subprocess

python_format = '/home/ekern/python_format/python_format.py'

if __name__ == '__main__':
    start = vim.current.range.start
    end = vim.current.range.end
    buf = vim.current.buffer

    while buf[end].rstrip().endswith('\\'):
        end += 1

    while (start >= 0) and buf[start - 1].rstrip().endswith('\\'):
        start -= 1

    text = ''.join([l + '\n' for l in buf[start : end + 1]])

    p = subprocess.Popen(['python', python_format], stdout = subprocess.PIPE,
        stderr = subprocess.PIPE, stdin = subprocess.PIPE)

    stdout, stderr = p.communicate(input = text)

    if not stdout:
        print('No output from python_format')
    elif stdout != text:
        lines = stdout.splitlines()

        vim.command('%d,%ds/%s/%s/g' %
            (start + 1, end + 1, '^.*\\n' * (end - start + 1),
            '\\r' * len(lines)))    

        for i, line in enumerate(lines):
            buf[start + i] = line

