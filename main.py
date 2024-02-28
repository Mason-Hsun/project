import os
import trash_detect
def main():
    save_photo_directory = os.path.join(os.getcwd(), "save")
    
        
    try:
        trash_tracker = trash_detect.TrashTracker(save_photo_directory)
        trash_tracker.run()
    except Exception as e:
        print("{}".format(e))
        
if __name__ == "__main__":
    main()
