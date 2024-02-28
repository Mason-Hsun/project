import trash_detect
def main():
    num_photos = None
    interval_seconds = 5 
    total_duration_seconds = None
    save_photo_directory = "/home/pi/Desktop/拍攝照片"
    
    if total_duration_seconds is not None:
        num_photos = total_duration_seconds // interval_seconds 
        
    try:
        trash_tracker = trash_detect.TrashTracker(num_photos, save_photo_directory)
        trash_tracker.run()
    except Exception as e:
        print("{}".format(e))
        
if __name__ == "__main__":
    main()