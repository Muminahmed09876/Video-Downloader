import yt_dlp
import os
import sys

# --- প্রগ্রেস দেখানোর কাস্টম ফাংশন ---
def progress_hook(d):
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
        downloaded = d.get('downloaded_bytes', 0)
        speed = d.get('speed', 0)
        percent = d.get('_percent_str', ' 0%').strip()
        
        total_mb = total / (1024 * 1024)
        downloaded_mb = downloaded / (1024 * 1024)
        speed_mb = speed / (1024 * 1024) if speed else 0
        
        # ক্লিন এবং ফিক্সড আউটপুট
        msg = (f"\r\033[K[TA HD] {downloaded_mb:>5.1f}/{total_mb:<5.1f} MB | "
               f"{percent:>5} | Spd: {speed_mb:>5.2f} MB/s")
        sys.stdout.write(msg)
        sys.stdout.flush()
    
    elif d['status'] == 'finished':
        # ডাউনলোড শেষ, এখন মার্জিং শুরু হবে
        sys.stdout.write("\n\n[TA HD] 100% Downloaded. Merging files (Please wait)...\n")
        sys.stdout.flush()

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def download_video():
    while True:
        print("\n" + "★"*45)
        print("      TA HD YOU TUBE VIDEO DOWNLOADER      ")
        print("★"*45)
        
        url = input("\nEnter YouTube URL (or 'e' to exit): ").strip()
        
        if url.lower() in ['e', 'exit']:
            print("Goodbye!")
            break

        print("\nSelect Quality:")
        print("0. Best Quality (Auto)  4. 480p (Medium)    7. 144p (Lowest)")
        print("1. 1080p (Full HD)      5. 360p (Standard)  8. Only Audio (MP3)")
        print("2. 720p (HD)           6. 240p (Low)       c. Cancel")
        print("3. 560p (Custom)")
        
        choice = input("\nChoice (0-8/c): ").lower().strip()
        
        if choice == 'c': 
            clear_screen()
            continue
        
        quality_map = {
            '0': 'best', '1': '1080', '2': '720', '3': '560', 
            '4': '480', '5': '360', '6': '240', '7': '144'
        }
        
        if choice == '8':
            format_str = 'bestaudio/best'
        elif choice in quality_map:
            res = quality_map[choice]
            if choice == '0':
                format_str = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            else:
                format_str = f'bestvideo[height<={res}][ext=mp4]+bestaudio[ext=m4a]/best[height<={res}][ext=mp4]/best'
        else:
            format_str = 'best'

        # বেসিক অপশন
        ydl_opts = {
            'format': format_str,
            'outtmpl': '/sdcard/Download/%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'noprogress': True,
            'progress_hooks': [progress_hook],
            'concurrent_fragment_downloads': 4, # স্পিড বাড়ানোর জন্য
        }

        if choice == '8':
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        try:
            print("\n[TA HD] Checking & Processing...")
            
            # ১. ইনফো সংগ্রহ (একবারই)
            # আমরা এখানে temp অবজেক্ট ব্যবহার করব না, মেইন অবজেক্টই ব্যবহার করব
            ydl = yt_dlp.YoutubeDL(ydl_opts)
            info = ydl.extract_info(url, download=False)
            
            # ফাইলের নাম প্রস্তুত করা
            filename = ydl.prepare_filename(info)
            if choice == '8':
                base, _ = os.path.splitext(filename)
                filename = base + ".mp3"

            # ২. কনফ্লিক্ট চেক
            final_start_download = True
            
            if os.path.exists(filename):
                print(f"\n[!] File exists: {os.path.basename(filename)}")
                ask = input("Rename file? (Enter = Yes [Auto Rename] / n = No [Overwrite]): ").strip().lower()
                
                if ask == '' or ask == 'y':
                    base, ext = os.path.splitext(filename)
                    counter = 1
                    new_filename = f"{base} ({counter:02d}){ext}"
                    while os.path.exists(new_filename):
                        counter += 1
                        new_filename = f"{base} ({counter:02d}){ext}"
                    
                    # নাম পরিবর্তন হলে অপশন আপডেট করতে হবে
                    ydl_opts['outtmpl'] = new_filename
                    print(f"-> Renaming to: {os.path.basename(new_filename)}")
                    
                    # অপশন আপডেটের পর নতুন অবজেক্ট তৈরি করা জরুরি
                    ydl = yt_dlp.YoutubeDL(ydl_opts)
                else:
                    print("-> Overwriting...")

            # ৩. ফাস্ট ডাউনলোড (Direct Processing)
            # info আমরা আগেই নামিয়েছি, তাই আবার url দিয়ে ডাউনলোড না করে
            # সরাসরি info প্রসেস করব। এতে দ্বিতীয়বার লোডিং হবে না।
            try:
                ydl.process_ie_result(info, download=True)
            except AttributeError:
                # যদি কোনো কারণে process_ie_result কাজ না করে, তবে সাধারণ পদ্ধতি
                ydl.download([url])
                
            print("\n✅ Download Completed!")

        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        input("\nPress Enter to clear and continue...")
        clear_screen()

if __name__ == "__main__":
    if not os.path.exists("/sdcard/Download"):
        print("Please run 'termux-setup-storage'!")
    else:
        clear_screen()
        download_video()
