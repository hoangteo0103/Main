from rarCracker import RarCracker, LocalBreakPoint
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='RAR Cracker')
    parser.add_argument('--file_path', type=str, required=True, help='Path to the RAR file')
    parser.add_argument('--charset', type=str, required=True, help='Charset to use for cracking')
    parser.add_argument('--min_char', type=int, required=True, help='Minimum number of characters in the password')
    parser.add_argument('--max_char', type=int, required=True, help='Maximum number of characters in the password')
    parser.add_argument('--workers', type=int, default=4, help='Number of worker threads')
    return parser.parse_args()

def main():
    args = parse_args()
    
    def callback(msg):
        pass
    
    cracker = RarCracker(
        file_path=args.file_path,
        start=args.min_char,
        stop=args.max_char,
        charset=args.charset,
        workers=args.workers,
        break_point=LocalBreakPoint(breakpoint_count=1)
    )
    
    result = cracker.crack(callback)
    if result:
        print(f'Password found: {result}')
    else:
        print('Password not found')

if __name__ == '__main__':
    main()