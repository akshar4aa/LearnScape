import sys
import os

# Ensure the root directory is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    try:
        from src.engine.game import Game
        game = Game()
        game.run()
    except Exception as e:
        import traceback
        # Save error log
        with open("error_log.txt", "w") as f:
            traceback.print_exc(file=f)
        print("An error occurred during execution:")
        traceback.print_exc()
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
